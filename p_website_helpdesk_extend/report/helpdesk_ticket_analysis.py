from odoo import fields, models


class HelpdeskTicketReport(models.Model):
    _inherit = 'helpdesk.ticket.report.analysis'

    type_id = fields.Many2one(
        'support.extra.type',
        string="Type",
        help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types."
    )
    sub_type_1 = fields.Many2one(
        'support.extra.type',
        help="Only apply the SLA to a specific Sub Type 1. If left empty it will apply to all Sub Type 1."
    )
    sub_type_2 = fields.Many2one(
        'support.extra.type',
        help="Only apply the SLA to a specific Sub Type 1. If left empty it will apply to all Sub Type 2."
    )
    sub_type_3 = fields.Many2one(
        'support.extra.type',
        help="Only apply the SLA to a specific Sub Type 1. If left empty it will apply to all Sub Type 3."
    )
    sub_type_4 = fields.Many2one(
        'support.extra.type',
        help="Only apply the SLA to a specific Sub Type 1. If left empty it will apply to all Sub Type 4."
    )

    def _select(self):
        select_str = super()._select()
        select_str += ", T.type_id as type_id, T.sub_type_1 as sub_type_1, T.sub_type_2 as sub_type_2, T.sub_type_3 as sub_type_3, T.sub_type_4 as sub_type_4"
        return select_str
