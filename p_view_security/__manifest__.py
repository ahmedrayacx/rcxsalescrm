# -*- coding: utf-8 -*-
# Part of Param Enterprice. See LICENSE file for full copyright and licensing details.
{
    'name': "View Security",
    'version': '15.0.1',
    'author': "Param Enterprice",
    'category': 'Tools',
    'summary': 'View Security',
    'description': 'View Security',
    'depends': [
        'base', 'helpdesk'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/security_role_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
