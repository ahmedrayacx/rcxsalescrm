# -*- coding: utf-8 -*-
{
    'name': 'Portal Support',
    'category': 'Website/Website',
    'sequence': 60,
    'summary': 'Portal Support',
    'version': '15.0.1',
    'author': "Param Enterprice",
    'depends': [
        'website', 'helpdesk', 'p_view_security'
    ],
    'description': """Portal Support""",
    'data': [
        'security/ir.model.access.csv',
        'security/helpdesk_security.xml',
        'views/helpdesk_views.xml',
        'views/helpdesk_menu.xml',
        'views/support_ticket_template.xml',
        'report/helpdesk_ticket_analysis_views.xml',
        'report/helpdesk_sla_report_analysis_views.xml'
    ],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'p_website_helpdesk_extend/static/src/js/portal_support_ticket.js',
            'p_website_helpdesk_extend/static/src/css/support_ticket.scss'
        ]
    }
}
