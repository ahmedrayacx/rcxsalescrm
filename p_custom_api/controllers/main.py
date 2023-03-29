from odoo import http, _, fields
from odoo.http import request

class CustomAPI(http.Controller):

    @http.route('/record/list', type='json', auth="public")
    def employee_profile(self, **kw):
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
            request_sudo = request.env[model_name].sudo()
            if uid:
                request_sudo = request.env[model_name].with_user(uid)
            order_ids_length = request_sudo.search_count(domain)
            if field_list:
                order_ids = request_sudo.search_read(domain= domain, fields= field_list, limit=limit, offset=start)
            else:
                order_ids = request_sudo.search(domain, limit=limit, offset=start)
                order_ids = order_ids.read()
        except Exception as e:
            return {
                'code': 100,
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
