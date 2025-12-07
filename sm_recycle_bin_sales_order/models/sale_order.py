# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_client_ip(self):
        """Get client IP address from request
        
        Priority:
        1. X-Forwarded-For (standard proxy header, ngrok uses this)
        2. X-Real-IP (alternative proxy header, nginx commonly uses this)
        3. CF-Connecting-IP (Cloudflare)
        4. True-Client-IP (Akamai, Cloudflare Enterprise)
        5. remote_addr (direct connection fallback)
        """
        try:
            if request and hasattr(request, 'httprequest'):
                headers = request.httprequest.headers
                
                # 1. X-Forwarded-For (most common, ngrok uses this)
                xff = headers.get('X-Forwarded-For')
                if xff:
                    # Can contain multiple IPs: client, proxy1, proxy2...
                    # First one is the real client IP
                    return xff.split(',')[0].strip()
                
                # 2. X-Real-IP (nginx default)
                x_real_ip = headers.get('X-Real-IP')
                if x_real_ip:
                    return x_real_ip.strip()
                
                # 3. CF-Connecting-IP (Cloudflare)
                cf_ip = headers.get('CF-Connecting-IP')
                if cf_ip:
                    return cf_ip.strip()
                
                # 4. True-Client-IP (Akamai, Cloudflare Enterprise)
                true_client_ip = headers.get('True-Client-IP')
                if true_client_ip:
                    return true_client_ip.strip()
                
                # 5. Fallback to direct remote address
                return request.httprequest.remote_addr or 'Unknown'
        except Exception as e:
            _logger.warning(f"Could not get IP address: {e}")
        return 'Unknown'

    def _get_user_agent(self):
        """Get user agent / browser info from request"""
        try:
            if request and hasattr(request, 'httprequest'):
                return request.httprequest.headers.get('User-Agent', 'Unknown')[:255]
        except Exception as e:
            _logger.warning(f"Could not get user agent: {e}")
        return 'Unknown'

    def _prepare_recycle_bin_vals(self):
        """Prepare values to store in recycle bin before deletion"""
        self.ensure_one()
        
        # Prepare order lines summary
        lines_summary = []
        for line in self.order_line:
            lines_summary.append(
                f"- {line.product_id.display_name or 'No Product'}: "
                f"Qty {line.product_uom_qty} x {line.price_unit} = {line.price_subtotal}"
            )
        
        return {
            'so_name': self.name,
            'so_id': self.id,
            'partner_id': self.partner_id.id if self.partner_id else False,
            'partner_name': self.partner_id.display_name if self.partner_id else '',
            'date_order': self.date_order,
            'amount_total': self.amount_total,
            'currency_id': self.currency_id.id if self.currency_id else False,
            'state': dict(self._fields['state'].selection).get(self.state, self.state),
            'company_id': self.company_id.id if self.company_id else False,
            'order_lines_count': len(self.order_line),
            'order_lines_summary': '\n'.join(lines_summary) if lines_summary else 'No order lines',
            'delete_date': fields.Datetime.now(),
            'deleted_by_id': self.env.user.id,
            'deleted_by_name': self.env.user.display_name,
            'ip_address': self._get_client_ip(),
            'user_agent': self._get_user_agent(),
            'note': self.note or '',
        }

    def unlink(self):
        """Override unlink to store deleted SO info in recycle bin"""
        RecycleBin = self.env['sm.recycle.bin.sales.order'].sudo()
        
        for order in self:
            try:
                vals = order._prepare_recycle_bin_vals()
                RecycleBin.create(vals)
                _logger.info(f"Sales Order {order.name} moved to recycle bin by {self.env.user.name} from IP {vals.get('ip_address')}")
            except Exception as e:
                _logger.error(f"Error creating recycle bin entry for SO {order.name}: {e}")
        
        return super(SaleOrder, self).unlink()
