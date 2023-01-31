import math
from dateutil.relativedelta import relativedelta
from random import randint
from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    is_IT = fields.Boolean(compute='compute_is_IT')
    ticketType = fields.Selection([('inquery', 'Inquery'), ('requestsolution', 'Request Solution')],
                                  string='Ticket Type')
    #voice = fields.Boolean(string="Voice", default=False)
    #chatBot = fields.Boolean(string="ChatBot", default=False)
    #smartIVR = fields.Boolean(string="Smart IVR", default=False)
    #iVRDeflection = fields.Boolean(string="IVR Deflection", default=False)
    # new ivr field
    #ivr = fields.Boolean(string="IVR", default=False)
    transactions = fields.Selection(
        [('inbound', 'Inbound'), ('outbound', 'Outbound'), ('inbound&outbound', 'Inbound-Outbound')],
        string='Transactions')
    numberofLicenses = fields.Char(
        "Number of Licenses / Ports"
    )
    attachment = fields.Binary(string='Attachment')
    #whatsApp = fields.Boolean(string="WhatsApp", default=False)
    #soicalmedia = fields.Boolean(string="Social Media", default=False)
    #webChat = fields.Boolean(string="WebChat", default=False)

    # new fields
    #survey = fields.Boolean(string="Survey", default=False)
    #sms = fields.Boolean(string="SMS", default=False)
    #crm = fields.Boolean(string="CRM", default=False)
    #email = fields.Boolean(string="Email", default=False)
    #dailer = fields.Boolean(string="Dialer", default=False)
    #qms = fields.Boolean(string="QMS", default=False)
    #hosting = fields.Boolean(string="Hosting", default=False)
    #integration = fields.Boolean(string="Integration", default=False)
    
    pendingstage = fields.Selection([('proposal', 'Proposal'), ('integration', 'Integration'), ('sow', 'SOW'),
                                     ('solutiondesign', 'Solution Design'), ('demo', 'Demo'), ('poc', 'POC'),
                                     ('finalized', 'Finalized')], string='Pending Stage')

    industry = fields.Selection(
        [('travel', 'Travel'), ('printingIT', 'Printing / IT'), ('hotelsresort', 'Hotels/Resort'),
         ('fintech', 'Fintech'),
         ('medical', 'Medical'), ('education', 'Education'), ('hospitality', 'Hospitality'), ('logistics', 'Logistics'),
         ('ecommerce', 'E-Commerce'), ('telecom', 'Telecom'), ('elevator', 'Elevator'),
         ('transportation', 'Transportation'),
         ('it', 'IT'), ('government', 'Government'), ('fb', 'F&B'), ('entertainment', 'Entertainment'),
         ('insurance', 'Insurance'),
         ('wellness', 'Wellness'), ('healthcare', 'Healthcare'), ('retail', 'Retail'), ('automotive', 'Automotive'),
         ('financial', 'Financial'), ('pastry', 'Pastry'), ('helathtech', 'Helath Tech'), ('publishing', 'Publishing'),
         ('airline', 'Airline'), ('realestate', 'Real estate'), ('mediaentertainment', 'Media & Entertainment'),
         ('insurtech', 'Insurtech'), ('technology', 'Technology'), ('shipping', 'Shipping & Logistics'),
         ('manufacturing', 'Manufacturing'),
         ('printing', 'Printing'), ('fashion', 'Fashion'), ('consumerelectronics', 'Consumer Electronics')],
        string='Industry')

    solution = fields.Selection([('newsolution', 'New Solution'), ('updatedsolution', 'Updated Solution')],
                                string='Solution')
    presalesstatus = fields.Selection([('new', 'New'), ('inprogress', 'In Progress'), ('closed', 'Closed')],
                                      string='Presales Status')
    rfp = fields.Boolean("RFP", default=False)
    rfpsubmissiondate = fields.Date(string="RFP Submission Date")
    rfpontime = fields.Boolean(string="RFP (On-time)?", default=False)
    date_received = fields.Date(string="Date Received")
    date_closed = fields.Date(string="Date Closed")
    noofFTEs = fields.Char("No Of FTEs")

    codeName = fields.Char("Code Name")
    type_of_service_ids = fields.Many2many('contact.typeofservice', string='Type Of Service')
    market_ids = fields.Many2many('contact.market', string='Market')
    deliverysite_ids = fields.Many2many('contact.deliverysite', string='Delivery Site')
    service_ids = fields.Many2many('helpdesk.service', string='Service')
    existingclient = fields.Boolean(string="Existing Client ?", default=False)

    @api.onchange('codeName')
    def onchange_codename_partner(self):
        for rec in self:
            if rec.codeName:
                partner_id = self.env['res.partner'].search([('codeName', '=', rec.codeName)], limit=1)
                rec.partner_id = partner_id.id

    @api.onchange('partner_id')
    def onchange_partner(self):
        for rec in self:
            if rec.partner_id:
                update_dict = {
                    'type_of_service_ids': [(6, 0, rec.partner_id.type_of_service_ids.ids)],
                    'market_ids': [(6, 0, rec.partner_id.market_ids.ids)],
                    'deliverysite_ids': [(6, 0, rec.partner_id.deliverysite_ids.ids)],
                    'existingclient': rec.partner_id.existingclient
                }
                if rec.partner_id.codeName != rec.codeName:
                    update_dict['codeName'] = rec.partner_id.codeName
            else:
                update_dict = {
                    'type_of_service_ids': [(6, 0, [])],
                    'market_ids': [(6, 0, [])],
                    'deliverysite_ids': [(6, 0, [])],
                    'existingclient': False,
                    'codeName': ''
                }
            rec.update(update_dict)

    @api.depends('team_id')
    def compute_is_IT(self):
        for rec in self:
            if rec.team_id.name == "IT":
                rec.is_IT = True
            else:
                rec.is_IT = False


class HelpdeskService(models.Model):
    _name = 'helpdesk.service'
    _description = 'IT Service'
    _order = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "IT Service name already exists !"),
    ]

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    security_role_ids = fields.Many2many('security.role')