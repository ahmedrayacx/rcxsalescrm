from odoo import models, fields, api


class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    help_depart_id = fields.Many2one(
        'helpdesk.department',
        string="Department"
    )
    help_project_id = fields.Many2one(
        'helpdesk.project',
        string="Project"
    )
    help_subtype_id = fields.Many2one(
        'helpdesk.subtype',
        string="Sub-Type"
    )
    help_email_id = fields.Many2one(
        'helpdesk.email.notif',
        string="Email Notification"
    )
    unit_number = fields.Char(
        "Unit Number"
    )
    case_code = fields.Char(
        "Case Code"
    )

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


class Helpdesk_department_list(models.Model):
    _name = 'helpdesk.department'
    _description = "Helpdesk Department List"

    name = fields.Char(
        "Name",
        required=True
    )
    email_to = fields.Char(
        "Email To"
    )
    email_cc = fields.Char(
        "Email CC"
    )
    template_id = fields.Many2one(
        'mail.template',
        "Email Template",
        domain="[('model', '=', 'helpdesk.ticket')]",
        required=True
    )
    active = fields.Boolean(
        "Active",
        default=True,
    )


class helpdesk_project_list(models.Model):
    _name = 'helpdesk.project'

    name = fields.Char(
        "Name",
        required=True
    )
    active = fields.Boolean(
        "Active",
        default=True
    )


class helpdesk_subtype(models.Model):
    _name = 'helpdesk.subtype'

    name = fields.Char(
        "Name",
        required=True
    )
    active = fields.Boolean(
        "Active",
        default=True
    )


class helpdesk_email(models.Model):
    _name = 'helpdesk.email.notif'

    name = fields.Char(
        "Name",
        required=True
    )
    email_to = fields.Char(
        "Email To"
    )
    email_cc = fields.Char(
        "Email CC"
    )
    template_id = fields.Many2one(
        'mail.template',
        "Email Template",
        domain="[('model', '=', 'helpdesk.ticket')]",
        required=True
    )
    active = fields.Boolean(
        "Active",
        default=True
    )
