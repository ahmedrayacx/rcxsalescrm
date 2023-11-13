from odoo import models, fields, api
from lxml import etree


class SecurityRole(models.Model):
    _name = 'security.role'

    name = fields.Char("Role Name", copy=False)
    parent_id = fields.Many2one('security.role', string="Parent Role")
    group_id = fields.Many2one('res.groups', copy=False, ondelete='cascade')
    user_ids = fields.Many2many('res.users', string="Users", readonly=False, compute="compute_users",
                                inverse="inverse_users")
    is_sso_role = fields.Boolean("Is for SSO Users?")

    def compute_users(self):
        for rec in self:
            rec.user_ids = [(6, 0, rec.group_id.users.ids)]

    def inverse_users(self):
        for rec in self:
            rec.group_id.users = [(6, 0, rec.user_ids.ids)]

    @api.model
    def create(self, vals):
        call_super = super(SecurityRole, self).create(vals)
        for rec in call_super:
            rec.update_create_res_group()
        return call_super

    def unlink(self):
        for rec in self:
            group_id = rec.group_id
            self.env['ir.model.data'].sudo().search([
                ('module', '=', 'p_view_security_'),
                ('model', '=', group_id._name),
                ('res_id', '=', group_id.id)
            ], limit=1).unlink()
            rec.group_id.unlink()
        call_super = super(SecurityRole, self).unlink()
        return call_super

    def write(self, vals):
        call_super = super(SecurityRole, self).write(vals)
        if not self._context.get('no_update_group'):
            self.update_create_res_group()
        return call_super

    def update_create_res_group(self):
        self.ensure_one()
        vals = {
            'name': 'manually_' + self.name,
            'is_security_role': True
        }
        child_role_ids = self.env['security.role'].sudo().search([('parent_id', '=', self.id)])
        if child_role_ids:
            vals.update({
                'implied_ids': [(6, 0, child_role_ids.mapped('group_id').ids)]
            })
        if self.group_id:
            group_id = self.group_id
            group_id.sudo().write(vals)
            self.env['ir.model.data'].sudo().search([
                ('module', '=', 'p_view_security_'),
                ('model', '=', group_id._name),
                ('res_id', '=', group_id.id)
            ], limit=1).write({
                'name': group_id.name.lower().replace(' ', '_')
            })
        else:
            group_id = self.env['res.groups'].sudo().create(vals)
            self.with_context(no_update_group=True).write({
                'group_id': group_id.id
            })
            self.env['ir.model.data'].sudo().create({
                'name': group_id.name.lower().replace(' ', '_'),
                'module': 'p_view_security_',
                'model': group_id._name,
                'res_id': group_id.id,
            })


class SecurityViewFields(models.Model):
    _name = 'security.view.fields'
    _rec_name = 'field_id'

    model_id = fields.Many2one('ir.model', ondelete='cascade', required=True)
    field_id = fields.Many2one('ir.model.fields', ondelete='cascade', required=True)
    security_role_ids = fields.Many2many('security.role', required=True)
    group_ids = fields.Many2many('res.groups', compute="compute_groups")

    def compute_groups(self):
        for rec in self:
            rec.group_ids = [(6, 0, rec.security_role_ids.mapped('group_id').ids)]


class IR(models.Model):
    _inherit = 'ir.ui.view'

    def postprocess_and_fields(self, node, model=None):
        security_fields = self.env['security.view.fields'].sudo().search(
            [('security_role_ids', '!=', False), ('model_id.model', '=', model)])
        field_dict = {}
        group_xml_dict = security_fields.mapped('group_ids').get_external_id()
        for fiel in security_fields:
            field_dict[fiel.field_id.name] = [group_xml_dict.get(group.id) for group in fiel.group_ids]
        if field_dict:
            doc = etree.XML(etree.tostring(node, encoding='unicode'))
            for field, value in field_dict.items():
                node = doc.xpath("//field[@name='%s']" % field)
                if node and value:
                    node[0].set('groups', ",".join(value))
            node = etree.tostring(doc, encoding='unicode')
            node = etree.fromstring(node)
        super_arc, super_dict = super(IR, self).postprocess_and_fields(node, model)
        return super_arc, super_dict


class resGroups(models.Model):
    _inherit = 'res.groups'

    is_security_role = fields.Boolean('Is Security Role', default=False)

    def get_application_groups(self, domain):
        call_super = super(resGroups, self).get_application_groups(domain)
        return self.search(['&', ('is_security_role', '=', False), ('id', 'in', call_super.ids)])
