import http.client as httplib
from odoo.addons.web.controllers.main import\
    set_cookie_and_redirect, login_and_redirect
from odoo.addons.auth_oauth.controllers.main import\
    fragment_to_query_string
import logging
import odoo
import json
import simplejson
from odoo.http import request
from odoo import http
import werkzeug.utils
from werkzeug.urls import url_encode
from odoo.addons.auth_oauth.controllers.main import OAuthLogin as Home


_logger = logging.getLogger(__name__)

class OAuth_Controller(http.Controller):

    @http.route('/auth/microsoft/signin',
                type='http',
                auth='none',
                csrf=False)
    @fragment_to_query_string
    def microsoft_signin(self, **kw):
        root_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/'

        oauth_provider_rec =request.env['ir.model.data'].sudo()._xmlid_to_res_id('p_microsoft_sso.provider_microsoft')

        provider = request.env['auth.oauth.provider'].sudo().browse(oauth_provider_rec)

        authorization_data = provider.new_oauth_token(
                'authorization_code',
                kw.get('code'),
                refresh_token=None)

        access_token = authorization_data.get('access_token')

        refresh_token = authorization_data.get('refresh_token')

        try:
            conn = httplib.HTTPSConnection(provider.data_endpoint)
            conn.request("GET", "/v1.0/me", "", {
                'Authorization': access_token,
                'Accept': 'application/json'
            })
            response = conn.getresponse()
            data = simplejson.loads(response.read())
            displayName = data.get('displayName')
            user_id = data.get('id')
            email = data.get('userPrincipalName')
            conn.close()
        except Exception as e:
            _logger.error(e)
        try:
            credentials = request.env['res.users'].sudo().microsoft_auth_oauth(
                provider.id, {
                    'access_token': access_token,
                    'user_id': user_id,
                    'email': email,
                    'name': displayName,
                    'microsoft_refresh_token': refresh_token
                })
            request.cr.commit()
            return login_and_redirect(*credentials,
                                      redirect_url=root_url + 'web?')
        except odoo.exceptions.AccessDenied:
            _logger.info(
                'OAuth2: access denied,'
                ' redirect to main page in case a valid'
                ' session exists, without setting cookies')
            url = "/web/login?oauth_error=3"
            redirect = werkzeug.utils.redirect(url, 303)
            redirect.autocorrect_location_header = False
            return redirect
        except AttributeError:
            _logger.error(
                "auth_signup not installed on"
                " database %s: oauth sign up cancelled." % (
                    request.cr.dbname))
            url = "/web/login?oauth_error=1"
        except Exception as e:
            _logger.exception("OAuth2: %s" % str(e))
            url = "/web/login?oauth_error=2"
        return set_cookie_and_redirect(root_url + url)

class OAuth_Login(Home):

    def list_providers(self):
        try:
            all_providers = request.env['auth.oauth.provider'].sudo().search_read(
                [('enabled', '=', True)])
        except Exception:
            all_providers = []
        provider_microsoft = request.env.ref(
            'p_microsoft_sso.provider_microsoft')
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        for provider in all_providers:
            if provider.get('id') == provider_microsoft.id:
                return_url = base_url + '/auth/microsoft/signin'
                params = dict(
                    client_id=provider['client_id'],
                    response_type='code',
                    redirect_uri=return_url,
                    prompt='select_account',
                    scope=provider['scope'],
                )
            else:
                return_url = base_url + '/auth_oauth/signin'
                state = self.get_state(provider)
                params = dict(
                    response_type='token',
                    client_id=provider['client_id'],
                    redirect_uri=return_url,
                    scope=provider['scope'],
                    state=json.dumps(state),
                )
            provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'],
                                               url_encode(params))
        return all_providers
