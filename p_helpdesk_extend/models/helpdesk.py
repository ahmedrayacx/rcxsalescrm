from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    CodeName = fields.Char("Code Name")
    Project = fields.Selection([('New','New')],('Existed','Existed')])
   
   













