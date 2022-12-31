from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'
    is_IT=fields.Boolean(compute='compute_is_IT')
    CodeName = fields.Char("Code Name")
    Project = fields.Selection([('new', 'New'), ('existed', 'Existed')], string='Project')
    Voice = fields.Boolean(string="Voice",default=False)
    ChatBot = fields.Boolean(string="ChatBot",default=False)
    SmartIVR = fields.Boolean(string="Smart IVR",default=False)
    IVRDeflection  = fields.Boolean(string="IVR Deflection",default=False)
    Transactions = fields.Selection(
        [('inbound', 'Inbound'), ('outbound', 'Outbound'), ('inbound&outbound', 'Inbound-Outbound')],string='Transactions')
    NumberofLicenses= fields.Char(
        "Number of Licenses / Ports"
    )
    Attachment = fields.Binary(string='Attachment')
    WhatsApp = fields.Boolean(string="WhatsApp",default=False)
    Facebook = fields.Boolean(string="Facebook",default=False)
    WebChat = fields.Boolean(string="WebChat",default=False)
   
   
   
    @api.depends('team_id')
    def compute_is_IT(self):
        for rec in self:
            
            if rec.team_id.name=="IT":
                rec.is_IT=True
            else:
                rec.is_IT=False












