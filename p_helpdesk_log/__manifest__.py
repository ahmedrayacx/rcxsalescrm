# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk EMail Automation',
    'category': 'Helpdesk',
    'sequence': 60,
    'summary': 'Send Mail Notification if any changes in Ticket.',
    'version': '15.0.1',
    'author': "Param Enterprice",
    'depends': [
        'helpdesk', 'mail', 'p_website_helpdesk_extend'
    ],
    'data': [
        'data/email_template.xml',
    ],
    'license': 'LGPL-3'
}