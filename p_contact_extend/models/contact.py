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
    
