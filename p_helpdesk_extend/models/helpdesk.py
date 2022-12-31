from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    CodeName = fields.Char("Code Name")
    ProjectName = fields.Selection([('New','New')],('Existed','Existed')],string="Project Name")
   
   













