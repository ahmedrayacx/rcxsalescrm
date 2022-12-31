from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'
    is_IT=fields.Boolean(compute='compute_is_IT')
    codeName = fields.Char("Code Name")
    project = fields.Selection([('new', 'New'), ('existed', 'Existed')], string='Project')
    voice = fields.Boolean(string="Voice",default=False)
    chatBot = fields.Boolean(string="ChatBot",default=False)
    smartIVR = fields.Boolean(string="Smart IVR",default=False)
    iVRDeflection  = fields.Boolean(string="IVR Deflection",default=False)
    transactions = fields.Selection(
        [('inbound', 'Inbound'), ('outbound', 'Outbound'), ('inbound&outbound', 'Inbound-Outbound')],string='Transactions')
    numberofLicenses= fields.Char(
        "Number of Licenses / Ports"
    )
    attachment = fields.Binary(string='Attachment')
    whatsApp = fields.Boolean(string="WhatsApp",default=False)
    facebook = fields.Boolean(string="Facebook",default=False)
    webChat = fields.Boolean(string="WebChat",default=False)
    market=fields.Selection([('egypt', 'Egypt'), ('gcc', 'GCC'),('uae','UAE'),('morroco','Morroco'),('ksa', 'KSA'),
    ('bahrain','Bahrain'),('kuwait','Kuwait'),('australia','Australia'),('mea','MEA'),('usa','USA'),
    ('europeuk','Europe/UK'),('oman','Oman'),('qatar','Qatar')], string='Market')
   
   
    @api.depends('team_id')
    def compute_is_IT(self):
        for rec in self:
            
            if rec.team_id.name=="IT":
                rec.is_IT=True
            else:
                rec.is_IT=False












