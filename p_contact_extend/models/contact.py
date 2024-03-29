import math
from dateutil.relativedelta import relativedelta
from random import randint
from odoo import models, fields


class Partner_inherit(models.Model):
    _inherit = 'res.partner'

    codeName = fields.Char("Code Name")
    type_of_service_ids = fields.Many2many('contact.typeofservice', string='Type Of Service')
    market_ids = fields.Many2many('contact.market', string='Market')
    existingclient = fields.Boolean(string="Existing Client ?", default=False)
    deliverysite_ids = fields.Many2many('contact.deliverysite', string='Delivery Site')
    # new fields 5-3-2023
    contract_renewal_date = fields.Date(string='Contract Renewal Date')
    account_launch_date = fields.Date(string='Account Launch Date')
    contract_beginning_date = fields.Date(string='Contract Beginning Date')
    contract_end_date = fields.Date(string='Contract End Date')
    percentage_of_increase = fields.Float(string='Percentage Of Increase %')
    termination_period_inmonth = fields.Float(string='Termination period In Month %')
    payment_lead_time = fields.Datetime(string='Payment Lead Iime')
    penalties = fields.Char('Penalties')
    rewards = fields.Char('Rewards')
    account_headcount = fields.Char('Account Headcount')
    short_number  = fields.Char('Short Number')
    working_hours_from = fields.Datetime('From')
    working_hours_to = fields.Datetime('To')
    wfh = fields.Char('WFH %')
    payment_model = fields.Char('Payment Model')
    currency_id =   fields.Many2one(
        'contact.currency',
        string="Currency"
    )
    power_pi_link = fields.Char('Power PI Link')
    power_pi_user_name = fields.Char('Power User Name')
    gp = fields.Char('GP %')
    eat= fields.Char('EAT %')

    _sql_constraints = [
        ('name_uniq', 'unique (codeName)', "Code Name name already exists !"),
    ]

class ContactTypeOfService(models.Model):
    _name = 'contact.typeofservice'
    _description = 'contact Type Of Service'
    _order = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Service name already exists !"),
    ]


class ContactMarket(models.Model):
    _name = 'contact.market'
    _description = 'Lead Market'
    _order = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Market name already exists !"),
    ]



class ContactDeliverySite(models.Model):
    _name = 'contact.deliverysite'
    _description = 'Lead Delivery Site'
    _order = 'name'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Delivery Site name already exists !"),
    ]
    



class contact_currency(models.Model):
    _name = 'contact.currency'
    _description = "Contact Currency"

    name = fields.Char(
        "Name",
        required=True
    )
    active = fields.Boolean(
        "Active",
        default=True,
    )
