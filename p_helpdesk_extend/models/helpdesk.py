from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'
    is_IT=fields.Boolean(compute='compute_is_IT')
    codeName = fields.Char("Code Name")
    #project = fields.Selection([('new', 'New'), ('existed', 'Existed')], string='Project')
    ticketType = fields.Selection([('inquery', 'Inquery'), ('requestsolution', 'Request Solution')], string='Ticket Type')
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
    industry= fields.Selection(
        [('travel', 'Travel'), ('printingIT', 'Printing / IT'), ('hotelsresort', 'Hotels/Resort'),('fintech','Fintech'),
        ('medical','Medical'),('education','Education'),('hospitality','Hospitality'),('logistics','Logistics'),
        ('ecommerce','E-Commerce'),('telecom','Telecom'),('elevator','Elevator'),('transportation','Transportation'),
        ('it','IT'),('government','Government'),('fb','F&B'),('entertainment','Entertainment'),('insurance','Insurance'),
        ('wellness','Wellness'),('healthcare','Healthcare'),('retail','Retail'),('automotive','Automotive'),
        ('financial','Financial'),('pastry','Pastry'),('helathtech','Helath Tech'),('publishing','Publishing'),
        ('airline','Airline'),('realestate','Real estate'),('mediaentertainment','Media & Entertainment'),
        ('insurtech','Insurtech'),('technology','Technology'),('shipping','Shipping & Logistics'),('manufacturing','Manufacturing'),
        ('printing','Printing'),('fashion','Fashion'),('consumerelectronics','Consumer Electronics')],string='Industry')
    type_of_service=fields.Selection([('bPO', 'BPO'), ('outboundcampaign', 'Outbound Campaign'),('hro','HRO'),('ito','ITO'),('hosting', 'Hosting')], string='Type of Service')
    solution=fields.Selection([('newsolution', 'New Solution'), ('updatedsolution', 'Updated Solution')], string='Solution')
    presalesstatus=fields.Selection([('new', 'New'), ('inprogress', 'In Progress'),('closed', 'Closed')], string='Presales Status')
    rfp = fields.Boolean("RFP",default=False)
    rfpsubmissiondate=fields.Date(string="RFP Submission Date")
    existingclient = fields.Boolean(string="Existing Client ?",default=False)
    rfpontime = fields.Boolean(string="RFP (On-time)?",default=False)
    date_received=fields.Date(string="Date Received")
    date_closed=fields.Date(string="Date Closed")
    noofFTEs = fields.Char("No Of FTEs")
    
    @api.depends('team_id')
    def compute_is_IT(self):
        for rec in self:
            
            if rec.team_id.name=="IT":
                rec.is_IT=True
            else:
                rec.is_IT=False












