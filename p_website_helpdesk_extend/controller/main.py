# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import requests
import logging, base64

_logger = logging.getLogger(__name__)


class WebsiteHelpdeskExtend(http.Controller):

    @http.route(['/support/ticket'], type='http', auth="user", website=True,
                sitemap=True)
    def website_support_ticket(self, **kwargs):
        result = self.get_support_ticket_vals()
        if request.httprequest.method == 'POST' and kwargs:
            attachment_list = request.httprequest.files.getlist('attachments')
            if 'attachments' in kwargs:
                del kwargs['attachments']
            helpdesk_sudo = request.env['helpdesk.ticket'].sudo()
            default_vals = helpdesk_sudo.default_get(helpdesk_sudo._fields)
            try:
                Many_2one_list = ['site_id', 'site_project_id', 'type_id', 'team_id', 'sub_type_1']
                for m2o_name in Many_2one_list:
                    kwargs[m2o_name] = kwargs.get(m2o_name) and int(kwargs.get(m2o_name)) or False
                default_vals.update(kwargs)
                email = default_vals.get('partner_email')
                if email:
                    partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
                    if not partner:
                        partner = request.env['res.partner'].sudo().create({
                            'email': email,
                            'name': email,
                            'phone': default_vals.get('partner_phone'),
                            'is_helpdesk': True
                        })
                    else:
                        partner.is_helpdesk = True
                    default_vals['partner_id'] = partner.id
                helpdesk_id = helpdesk_sudo.create(default_vals)
                attach_list = []
                for attach in attachment_list:
                    attached_file = attach.read()
                    attach_id = request.env['ir.attachment'].sudo().create({
                        'name': attach.filename,
                        'res_model': 'helpdesk.ticket',
                        'res_id': helpdesk_id.id,
                        'datas': base64.encodebytes(attached_file)
                    })
                    attach_list.append(attach_id.id)
                if attach_list:
                    helpdesk_id.write({
                        'ticket_attachment_ids': [(6, 0, attach_list)]
                    })
                return request.render("p_website_helpdesk_extend.support_ticket_submitted", {'ticket': helpdesk_id})
            except Exception as e:
                result.update({
                    'error_message': result['error_message'] + ['Please Try again after some time.']
                })
                _logger.info("Error while creating Helpdesk Ticket %s" % (e))

        default_user_vals = self.get_default_ticket_vals()
        if default_user_vals:
            site_id = request.env['support.extra.site'].sudo().search(
                [('parent_id', '=', False), ('name', '=', default_user_vals.get('Site', ''))], limit=1)
            if site_id:
                result.update({
                    'default_site_id': site_id.id
                })
            site_project_id = request.env['support.extra.site'].sudo().search(
                [('parent_id', '=', site_id.id), ('name', '=', default_user_vals.get('Project', ''))], limit=1)
            if site_project_id:
                result.update({
                    'default_site_project_id': site_project_id.id
                })
            result.update({
                'default_hrid': default_user_vals.get('HRId', 'Emaar')
            })
        result.update({
            'default_partner_email': request.env.user.login
        })
        return request.render("p_website_helpdesk_extend.support_ticket_view", result)

    def get_default_ticket_vals(self):
        url = "https://alnadasms-api.rayacx.com/api/GetEmployeeDataByEmail?email=%s" % (request.env.user.login)
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.request("GET", url=url, headers=headers)
            _logger.info("Employee Detail Response Status Code(%s) and Data(%s)" % (response.status_code, response.text))
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            _logger.info(e)
        return {}

    def get_support_ticket_vals(self):
        vals = {
            'error': {},
            'error_message': [],
            'site_ids': request.env['support.extra.site'].sudo().search_read([('parent_id', '=', False)],
                                                                             ['id', 'name']),
            'site_project_ids': request.env['support.extra.site'].sudo().search(
                [('parent_id.parent_id', '=', False)]),
            'type_ids': request.env['support.extra.type'].sudo().search(
                [('parent_id', '=', False), ('team_id', '!=', False)]),
            'team_ids': request.env['helpdesk.team'].sudo().search_read([('is_helpdesk', '=', True)], ['id', 'name', 'portal_color_code']),
            'form_action': '/support/ticket',
            'sub_type_1_ids': request.env['support.extra.type'].sudo().search(
                [('parent_id.parent_id', '=', False)]),
        }
        new_sub_type = []
        for sub_type in vals.get('sub_type_1_ids'):
            new_sub_type.append({
                'id': sub_type.id,
                'name': sub_type.name,
                'type': sub_type.parent_id.id or ''
            })
        vals['sub_type_1_ids'] = new_sub_type
        new_type = []
        for type in vals.get('type_ids'):
            new_type.append({
                'id': type.id,
                'name': type.name,
                'team': type.team_id.id or ''
            })
        vals['type_ids'] = new_type
        new_project = []
        for proj in vals['site_project_ids']:
            new_project.append({
                'id': proj.id,
                'name': proj.name,
                'site_id': proj.parent_id.id or ''
            })
        vals['site_project_ids'] = new_project
        return vals
