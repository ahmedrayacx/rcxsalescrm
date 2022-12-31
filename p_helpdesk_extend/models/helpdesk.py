from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    CodeName =fields.Char("Code Name")
    Project = fields.Selection([("New","New")],("Existed","Existed")])
   
    


   
    @api.model
    def create(self, vals):
        call_super = super(Helpdesk_ticket, self).create(vals)
        for rec in call_super:
            if rec.help_depart_id:
                email_values = {
                    'email_to': rec.help_depart_id.email_to,
                    'email_cc': rec.help_depart_id.email_cc,
                }
                rec.help_depart_id.template_id.send_mail(rec.id, force_send=True, email_values=email_values)
        return call_super













