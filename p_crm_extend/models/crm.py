from odoo import models, fields, api, _


class CRMInherit(models.Model):
    _inherit = 'crm.lead'

    codeName = fields.Char("Code Name")
    type_of_service_ids = fields.Many2many('contact.typeofservice', string='Type Of Service')
    market_ids = fields.Many2many('contact.market', string='Market')
    deliverysite_ids = fields.Many2many('contact.deliverysite', string='Delivery Site')
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
