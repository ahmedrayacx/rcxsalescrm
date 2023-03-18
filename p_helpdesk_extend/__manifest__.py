# -*- coding: utf-8 -*-
# Part of Param Enterprice. See LICENSE file for full copyright and licensing details.
{
    'name': "Helpdesk Extend",
    'version': '15.0.1',
    'author': "Helpdesk Enterprice",
    'category': 'Tools',
    'summary': 'Helpdesk Extend',
    'description': 'Helpdesk Extend',
    'depends': [
        'base',
        'helpdesk',
        'p_contact_extend',
        'p_view_security'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/helpdesk_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
