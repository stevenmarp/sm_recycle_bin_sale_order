# -*- coding: utf-8 -*-
{
    'name': 'Recycle Bin - Sales Order',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Track deleted Sales Orders with user info, IP address, and deletion details',
    'description': '''
        Recycle Bin for Sales Order
        ===========================
        
        This module tracks all deleted Sales Orders and stores:
        - Sales Order data (name, partner, amount, etc.)
        - User who deleted the record
        - IP address of the computer
        - Date and time of deletion
        - Reason for deletion (optional)
        
        Features:
        - View all deleted Sales Orders
        - Track who deleted what and when
        - IP address logging for audit trail
        - Search and filter deleted records
    ''',
    'author': 'Steven Marp',
    'website': 'https://apps.odoo.com/apps/browse?repo_maintainer_id=512936',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/recycle_bin_views.xml',
        'views/menu.xml',
    ],
    'images': [
        'static/description/banner.gif',
        'static/description/menu.jpeg',
        'static/description/list.jpeg',
        'static/description/form.jpeg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 49.99,
    'currency': 'USD',
}
