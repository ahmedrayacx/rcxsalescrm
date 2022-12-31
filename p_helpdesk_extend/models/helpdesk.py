from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    CodeName = fields.Char("Code Name")
   
    Voice = fields.Boolean(string="Voice",default=False)
   
   
   













