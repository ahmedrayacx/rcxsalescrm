from odoo import http, _, fields
from odoo.http import request
import requests
from odoo.service import db, security
from odoo.addons.web.controllers.main import Session
import logging
_logger = logging.getLogger(__name__)

class CustomAPI(http.Controller):

    @http.route('/record/list', type='json', auth="public", methods=['POST'])
    def CustomRecordList(self, **kw):
        model_name = kw.get('model_name')
        domain = list(kw.get('domain', [])) or []
        field_list = list(kw.get('field_list', [])) or []
        uid = kw.get('uid')
        if not model_name:
            return {
                'code': 1001,
                'message': 'Please enter Model Name !!',
                'data': []
            }
        start = int(kw.get('start', 0))
        end = int(kw.get('end', 0))
        limit = end + 1 - start
        if limit <= 1:
            limit = 10
        try:
            def get_selection_label(request_sudo, field_name, field_value):
                return _(
                    dict(request_sudo.fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

            request_sudo = request.env[model_name].sudo()
            if uid:
                request_sudo = request.env[model_name].with_user(uid)
            order_ids_length = request_sudo.search_count(domain)
            if field_list:
                order_ids = request_sudo.search_read(domain=domain, fields=field_list, limit=limit, offset=start)
            else:
                order_ids = request_sudo.search(domain, limit=limit, offset=start)
                order_ids = order_ids.read()

            selection_field_list = [i for i in request_sudo._fields if request_sudo._fields[i].type == 'selection' and (
                    (field_list and request_sudo._fields[i].name in field_list) or (not field_list))]

            for order in order_ids:
                for selection_name in selection_field_list:
                    if selection_name in order and order[selection_name]:
                        order[selection_name] = get_selection_label(request_sudo,
                                                                    selection_name,
                                                                    order[selection_name])

        except Exception as e:
            return {
                'code': 1001,
                'message': e,
                'data': []
            }
        return {
            'code': 1000,
            'message': 'Records Found Successfully!',
            'data': order_ids,
            'start': start,
            'fetched_records': len(order_ids),
            'total_records': order_ids_length
        }

    @http.route('/mobile/helpdesk/default', type='json', auth="user", methods=['GET'])
    def GetDefultHelpdeskValues(self, **kw):
        _logger.info("Helpdesk Default %s" % (kw))
        vals = {
            'site_ids': request.env['support.extra.site'].sudo().search_read([('parent_id', '=', False)],
                                                                             ['id', 'name']),
            'site_project_ids': request.env['support.extra.site'].sudo().search(
                [('parent_id.parent_id', '=', False)]),
            'type_ids': request.env['support.extra.type'].sudo().search(
                [('parent_id', '=', False), ('team_id', '!=', False)]),
            'team_ids': request.env['helpdesk.team'].sudo().search_read([('is_helpdesk', '=', True)],
                                                                        ['id', 'name', 'portal_color_code']),
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
        default_user_vals = {}
        url = "https://alnadasms-api.rayacx.com/api/GetEmployeeDataByEmail?email=%s" % (request.env.user.login)
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.request("GET", url=url, headers=headers)
            if response.status_code == 200:
                default_user_vals = response.json()
        except Exception as e:
            default_user_vals = {}

        if default_user_vals:
            site_id = request.env['support.extra.site'].sudo().search(
                [('parent_id', '=', False), ('name', '=', default_user_vals.get('Site', ''))], limit=1)
            if site_id:
                vals.update({
                    'default_site_id': site_id.id
                })
            site_project_id = request.env['support.extra.site'].sudo().search(
                [('parent_id', '=', site_id.id), ('name', '=', default_user_vals.get('Project', ''))], limit=1)
            if site_project_id:
                vals.update({
                    'default_site_project_id': site_project_id.id
                })
            vals.update({
                'default_hrid': default_user_vals.get('HRId', '')
            })
        vals.update({
            'default_partner_email': request.env.user.login
        })
        return vals

    @http.route('/mobile/helpdesk/create', type='json', auth="user", methods=['POST'])
    def MobileHelpdeskCreate(self, **kwargs):
        _logger.info("Helpdesk Create %s" % (kwargs))
        attachment_list = kwargs.get('attachments', [])
        if 'attachments' in kwargs:
            del kwargs['attachments']
        helpdesk_sudo = request.env['helpdesk.ticket']
        helpdesk_field_list = helpdesk_sudo._fields
        default_vals = helpdesk_sudo.default_get(helpdesk_sudo._fields)
        try:
            Many_2one_list = ['site_id', 'site_project_id', 'type_id', 'team_id']
            for i in helpdesk_field_list:
                if i in Many_2one_list:
                    kwargs[i] = kwargs.get(i) and int(kwargs.get(i)) or False
                elif i in kwargs.keys():
                    kwargs[i] = kwargs.get(i) and kwargs.get(i) or False
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
                attach_id = request.env['ir.attachment'].sudo().create({
                    'name': attach['filename'],
                    'res_model': 'helpdesk.ticket',
                    'res_id': helpdesk_id.id,
                    'datas': attach['base64_data']
                })
                attach_list.append(attach_id.id)
            if attach_list:
                helpdesk_id.write({
                    'ticket_attachment_ids': [(6, 0, attach_list)]
                })
            return {
                'code': 1000,
                'message': 'Records Created Successfully!',
                'data': [{
                    'id': helpdesk_id.id
                }]
            }
        except Exception as e:
            return {
                'code': 1001,
                'message': 'Please Try again after some time.',
                'error_message': e,
                'data': []
            }

    @http.route('/mobile/helpdesk/list', type='json', auth="user", methods=['POST'])
    def MobileHelpdeskHelpdeskList(self, **kw):
        _logger.info("Helpdesk List %s" % (kw))
        domain = ['|', ('team_id.is_helpdesk', '=', True), ('team_id', '=', False)]
        if 'id' in kw:
            domain.append(('id', '=', kw.get('id')))
        try:
            field_list = ['team_id', 'type_id', 'name', 'hrid', 'site_id', 'site_project_id', 'partner_phone',
                          'partner_email']

            request_sudo = request.env['helpdesk.ticket']
            order_ids_length = request_sudo.search_count(domain)
            order_ids = request_sudo.search_read(domain, field_list)
            # message_sudo = request.env['mail.message']
            # for order in order_ids:
            #     order.update({
            #         'message_ids'
            #     })

        except Exception as e:
            return {
                'code': 1001,
                'message': e,
                'data': []
            }
        return {
            'code': 1000,
            'message': 'Records Found Successfully!',
            'data': order_ids,
            'fetched_records': len(order_ids),
            'total_records': order_ids_length
        }

    @http.route('/mobile/sso/login', type='json', auth="none", methods=['POST'])
    def MobileSSOLOGIN(self, **kw):
        _logger.info("SSO Login %s" % (kw))
        email = kw.get('email')
        if email:
            user_id = request.env['res.users'].sudo().search([('login', '=', str(email))])
            if user_id:
                request.session.uid = user_id.id
                request.env['res.users'].clear_caches()
                request.session.session_token = security.compute_session_token(request.session, request.env)
        return Session.get_session_info(self)