# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SmRecycleBinSalesOrder(models.Model):
    _name = 'sm.recycle.bin.sales.order'
    _description = 'Recycle Bin - Sales Order'
    _order = 'delete_date desc'
    _rec_name = 'so_name'

    # Deleted SO Info
    so_name = fields.Char(string='SO Number', required=True, readonly=True)
    so_id = fields.Integer(string='Original SO ID', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    partner_name = fields.Char(string='Customer Name', readonly=True)
    date_order = fields.Datetime(string='Order Date', readonly=True)
    amount_total = fields.Monetary(string='Total Amount', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    state = fields.Char(string='State (Before Delete)', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    
    # Order Lines Summary
    order_lines_count = fields.Integer(string='Lines Count', readonly=True)
    order_lines_summary = fields.Text(string='Order Lines Summary', readonly=True)
    
    # Deletion Info
    delete_date = fields.Datetime(string='Deleted On', required=True, readonly=True, default=fields.Datetime.now)
    deleted_by_id = fields.Many2one('res.users', string='Deleted By', required=True, readonly=True)
    deleted_by_name = fields.Char(string='User Name', readonly=True)
    ip_address = fields.Char(string='IP Address', readonly=True)
    user_agent = fields.Char(string='User Agent / Browser', readonly=True)
    deletion_reason = fields.Text(string='Reason for Deletion')
    
    # Additional Info
    note = fields.Text(string='Notes', readonly=True)
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.so_name} (Deleted: {record.delete_date.strftime('%Y-%m-%d %H:%M')})"
            result.append((record.id, name))
        return result
