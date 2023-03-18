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
        'security/helpdesk_security.xml',
        'view/helpdesk_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'p_helpdesk_extend/static/src/js/chatter.js',
        ],
        'web.assets_qweb': [
            'p_helpdesk_extend/static/src/xml/*.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
