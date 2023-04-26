from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class SupportSiteFields(models.Model):
    _name = 'support.extra.site'
    _description = 'Support Site Selection'
    _parent_name = "parent_id"
    _parent_store = True
    _order = 'sequence,id'
    _rec_name = 'name'
    _check_company_auto = True

    sequence = fields.Integer(
        "Sequence"
    )
    complete_name = fields.Char("Display Name", compute='_compute_complete_name', store=False)
    name = fields.Char(
        'Name',
        required=True
    )
    parent_id = fields.Many2one(
        'support.extra.site', 'Parent', index=True, ondelete='cascade', check_company=True,
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        required=True
    )
    active = fields.Boolean(
        'Active',
        default=True,
    )
    child_ids = fields.One2many('support.extra.site', 'parent_id', 'Contains')
    len_child_ids = fields.Integer(
        compute="_compute_sub_child",
        store=True,
        default=0
    )
    parent_path = fields.Char(index=True)

    def _compute_complete_name(self):
        for resource in self:
            if resource.parent_id and not self._context.get('show_short_name', False):
                resource.complete_name = '%s/%s' % (resource.parent_id.complete_name, resource.name)
            else:
                resource.complete_name = resource.name

    @api.depends('child_ids')
    def _compute_sub_child(self):
        for rec in self:
            rec.sudo().len_child_ids = len(rec.child_ids.ids)

    def write(self, values):
        if 'company_id' in values:
            for rec in self:
                if rec.company_id.id != values['company_id']:
                    raise UserError(
                        _("Changing the company of this record is forbidden at this point, you should rather archive it and create a new one."))

        return super(SupportSiteFields, self).write(values)

    def action_open_childs_names(self):
        self.ensure_one()
        action = {
            'name': _('%s' % (self.name)),
            'domain': [('parent_id', '=', self.id)],
            'context': {'default_parent_id': self.id},
            'res_model': 'support.extra.site',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')],
        }
        return action


class SupportTypeFields(models.Model):
    _name = 'support.extra.type'
    _description = 'Support Type Selection'
    _parent_name = "parent_id"
    _parent_store = True
    _order = 'sequence,id'
    _rec_name = 'name'
    _check_company_auto = True

    sequence = fields.Integer(
        "Sequence"
    )
    complete_name = fields.Char("Display Name", compute='_compute_complete_name', store=False)
    name = fields.Char(
        'Name',
        required=True
    )
    parent_id = fields.Many2one(
        'support.extra.type', 'Parent', index=True, ondelete='cascade', check_company=True,
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        required=True
    )
    active = fields.Boolean(
        'Active',
        default=True,
    )
    child_ids = fields.One2many('support.extra.type', 'parent_id', 'Contains')
    len_child_ids = fields.Integer(
        compute="_compute_sub_child",
        store=True,
        default=0
    )
    parent_path = fields.Char(index=True)

    team_id = fields.Many2one('helpdesk.team')

    @api.onchange('team_id', 'parent_id')
    def update_team_id(self):
        for rec in self:
            if rec.parent_id:
                rec.team_id = False

    def _compute_complete_name(self):
        for resource in self:
            if resource.parent_id and not self._context.get('show_short_name', False):
                resource.complete_name = '%s/%s' % (resource.parent_id.complete_name, resource.name)
            else:
                resource.complete_name = resource.name

    @api.depends('child_ids')
    def _compute_sub_child(self):
        for rec in self:
            rec.sudo().len_child_ids = len(rec.child_ids.ids)

    def write(self, values):
        if 'company_id' in values:
            for rec in self:
                if rec.company_id.id != values['company_id']:
                    raise UserError(
                        _("Changing the company of this record is forbidden at this point, you should rather archive it and create a new one."))

        return super(SupportTypeFields, self).write(values)

    def action_open_childs_names(self):
        self.ensure_one()
        action = {
            'name': _('%s' % (self.name)),
            'domain': [('parent_id', '=', self.id)],
            'context': {'default_parent_id': self.id},
            'res_model': 'support.extra.type',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (False, 'form')],
        }
        return action


class SupportSubTeamField(models.Model):
    _name = 'helpdesk.team.child'
    _description = 'Helpdesk Child Team'
    _order = 'sequence,id'
    _rec_name = 'name'

    sequence = fields.Integer(
        "Sequence"
    )
    name = fields.Char(
        'Name',
        required=True
    )
    team_id = fields.Many2one(
        'helpdesk.team', 'Parent Team', index=True, ondelete='cascade',
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        required=True
    )
    active = fields.Boolean(
        'Active',
        default=True,
    )
    available_team_ids = fields.Many2many('helpdesk.team', compute="compute_available_team_ids")

    @api.depends('team_id')
    def compute_available_team_ids(self):
        for rec in self:
            domain = ['|', ('security_role_ids', '=', False),
                      ('security_role_ids.group_id.users', 'in', self.env.user.id)]

            is_helpdesk = self._context.get('show_only_helpdesk', False)
            domain.append(('is_helpdesk', '=', is_helpdesk))
            rec.available_team_ids = self.env['helpdesk.team'].search(domain)

class Helpdesk_ticket(models.Model):
    _inherit = 'helpdesk.ticket'

    is_helpdesk = fields.Boolean(related="team_id.is_helpdesk", store=True)
    sub_team_id = fields.Many2one('helpdesk.team.child', string="Sub-Team")
    hrid = fields.Char("HRID")
    site_id = fields.Many2one(
        'support.extra.site'
    )
    site_project_id = fields.Many2one(
        'support.extra.site'
    )
    type_id = fields.Many2one(
        'support.extra.type'
    )
    sub_type_1 = fields.Many2one(
        'support.extra.type'
    )
    sub_type_2 = fields.Many2one(
        'support.extra.type'
    )
    sub_type_3 = fields.Many2one(
        'support.extra.type'
    )
    sub_type_4 = fields.Many2one(
        'support.extra.type'
    )
    ticket_attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    is_incident = fields.Boolean("Is Incident?")
    due_date = fields.Date("Due Date")
    show_due_date = fields.Boolean("Show Due Date", compute="compute_due_date")

    partner_ids = fields.Many2many('res.partner', compute="compute_customers")

    @api.depends('is_helpdesk', 'team_id', 'type_id')
    def compute_due_date(self):
        for rec in self:
            show_due_date = False
            if rec.is_helpdesk and rec.team_id and rec.team_id.name.upper() == 'IT' and rec.type_id and rec.type_id.name.upper() == 'CHANGE':
                show_due_date = True
            rec.show_due_date = show_due_date

    @api.depends('partner_id')
    def compute_customers(self):
        for rec in self:
            domain = ['|', ('company_id', '=', False), ('company_id', '=', rec.company_id.id)]
            is_helpdesk = self._context.get('show_only_helpdesk', False)
            domain.append(('is_helpdesk', '=', is_helpdesk))
            rec.partner_ids = self.env['res.partner'].search(domain)

    def _default_team_id(self):
        is_helpdesk = self._context.get('show_only_helpdesk', False)
        team_id = self.env['helpdesk.team'].search(
            [('is_helpdesk', '=', is_helpdesk), ('member_ids', 'in', self.env.uid)], limit=1).id
        if not team_id:
            team_id = self.env['helpdesk.team'].search([('is_helpdesk', '=', is_helpdesk)], limit=1).id
        return team_id

    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', default=_default_team_id, index=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if args:
            args = ['&'] + args
        args += ['|', ('team_id.security_role_ids', '=', False),
                 ('team_id.security_role_ids.group_id.users', 'in', self.env.user.id)]
        if not self.env.context.get('force_search'):
            group_1 = self.env.user.sudo().has_group('p_helpdesk_extend.group_support_ticket')
            group_2 = self.env.user.sudo().has_group('p_website_helpdesk_extend.group_helpdesk_ticket')
            if group_1 and not group_2:
                args = ['&'] + args
                args += [('is_helpdesk', '=', False)]
            elif not group_1 and group_2:
                args = ['&'] + args
                args += [('is_helpdesk', '=', True)]
        if self.env.user.sudo().has_group('base.group_portal'):
            call_super = super(Helpdesk_ticket, self.sudo()).search(args, offset, limit, order, count)
        else:
            call_super = super(Helpdesk_ticket, self).search(args, offset, limit, order, count)
        return call_super

    def action_open_helpdesk_ticket(self):
        self.ensure_one()
        if self.is_helpdesk:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "p_website_helpdesk_extend.new_helpdesk_ticket_action_main_tree")
        else:
            action = self.env["ir.actions.actions"]._for_xml_id("helpdesk.helpdesk_ticket_action_main_tree")

        action.update({
            'domain': [('id', '!=', self.id), ('id', 'in', self.partner_ticket_ids.ids)],
            'context': {'create': False},
        })
        return action

    @api.onchange('team_id')
    def onchange_type_team_id(self):
        for rec in self:
            rec.update({
                'type_id': False,
                'sub_type_1': False,
                'sub_type_2': False,
                'sub_type_3': False,
                'sub_type_4': False,
                'sub_team_id': False
            })

    @api.onchange('type_id')
    def onchange_type_type_id(self):
        for rec in self:
            rec.update({
                'sub_type_1': False,
                'sub_type_2': False,
                'sub_type_3': False,
                'sub_type_4': False,
            })

    @api.onchange('sub_type_1')
    def onchange_sub_type_1(self):
        for rec in self:
            rec.update({
                'sub_type_2': False,
                'sub_type_3': False,
                'sub_type_4': False,
            })

    @api.onchange('sub_type_2')
    def onchange_sub_type_2(self):
        for rec in self:
            rec.update({
                'sub_type_3': False,
                'sub_type_4': False,
            })

    @api.onchange('sub_type_3')
    def onchange_sub_type_3(self):
        for rec in self:
            rec.update({
                'sub_type_4': False,
            })

    @api.model
    def _sla_reset_trigger(self):
        field_list = super()._sla_reset_trigger()
        field_list.append('type_id')
        field_list.append('sub_type_1')
        return field_list

    def _sla_find_extra_domain(self):
        domain = super()._sla_find_extra_domain()
        domain = expression.OR([domain, [
            '|', ('type_id', 'in', self.type_id.ids), ('type_id', '=', False),
        ]])
        domain = expression.OR([domain, [
            '|', ('sub_type_1', 'in', self.sub_type_1.ids), ('sub_type_1', '=', False),
        ]])
        return domain


class Helpdesk_Team(models.Model):
    _inherit = 'helpdesk.team'

    is_helpdesk = fields.Boolean("")
    portal_color_code = fields.Char("Portal Color Code")

    def action_view_ticket(self):
        if self._context.get('show_only_helpdesk'):
            action = self.env["ir.actions.actions"]._for_xml_id(
                "p_website_helpdesk_extend.new_helpdesk_ticket_action_team")
        else:
            action = self.env["ir.actions.actions"]._for_xml_id("helpdesk.helpdesk_ticket_action_team")
        action['display_name'] = self.name
        return action


class ResPartner_Inherit(models.Model):
    _inherit = 'res.partner'

    is_helpdesk = fields.Boolean("Is Helpdesk Customer")


class HelpdeskSLA(models.Model):
    _inherit = 'helpdesk.sla'

    type_id = fields.Many2one(
        'support.extra.type',
        string="Type",
        help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types."
    )
    new_type_id = fields.Many2one(
        'support.extra.type',
        string="Old Type",
        help="Only apply the SLA to a specific ticket type. If left empty it will apply to all types."
    )
    sub_type_1 = fields.Many2one(
        'support.extra.type',
        help="Only apply the SLA to a specific Sub Type 1. If left empty it will apply to all Sub Type 1."
    )