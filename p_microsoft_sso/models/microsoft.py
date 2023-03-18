import simplejson
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import AccessDenied, UserError, ValidationError
from odoo import api, fields, models, tools, _
from odoo.http import request
import logging, requests

_logger = logging.getLogger(__name__)


class Res_Users_Inherit(models.Model):
    _inherit = 'res.users'

    microsoft_refresh_token = fields.Char('Microsoft Refresh Token')

    @api.model
    def create(self, vals):
        call_super = super(Res_Users_Inherit, self).create(vals)
        for users in call_super:
            if users.oauth_provider_id:
                if users.oauth_provider_id.signin_type == 'Internal':
                    users.sudo().write({
                        'sel_groups_1_9_10': 1
                    })
                elif users.oauth_provider_id.signin_type == 'Portal':
                    users.sudo().write({
                        'sel_groups_1_9_10': 9
                    })
        return call_super

    @api.model
    def microsoft_auth_oauth(self, provider, params):
        access_token = params.get('access_token')
        login = self._microsoft_auth_signin(provider, params)
        if not login:
            raise AccessDenied()
        return self._cr.dbname, login, access_token

    @api.model
    def _microsoft_signup_values(self, provider, params):
        email = params.get('email')
        return {
            'name': params.get('name', email),
            'login': email,
            'email': email,
            'groups_id': [(6,0, [self.env.ref('base.group_user').id])],
            'company_id': 1,
            'oauth_provider_id': provider,
            'oauth_uid': params['user_id'],
            'microsoft_refresh_token': params['microsoft_refresh_token'],
            'oauth_access_token': params['access_token'],
            'active': True

        }

    @api.model
    def _microsoft_auth_signin(self, provider, params):

        try:

            oauth_uid = params['user_id']
            all_users = self.sudo().search([
                ("oauth_uid", "=", oauth_uid),
                ('oauth_provider_id', '=', provider)
            ], limit=1)
            if not all_users:
                all_users = self.sudo().search([
                    ("login", "=", params.get('email'))
                ], limit=1)
            if not all_users:
                raise AccessDenied()
            assert len(all_users.ids) == 1
            all_users.sudo().write({
                'oauth_access_token': params['access_token'],
                'microsoft_refresh_token': params['microsoft_refresh_token']})
            return all_users.login
        except AccessDenied as access_denied_exception:
            if self._context and self._context.get('no_user_creation'):
                return None
            vals = self._microsoft_signup_values(provider, params)
            try:
                _, login, _ = self.with_context(
                    mail_create_nosubscribe=True).signup(vals)
                return login
            except (SignupError, UserError):
                _logger.info("Signup error %s" % SignupError)
                _logger.info("UserError %s" % UserError)
                raise access_denied_exception


class Auth_Oauth_Provider_Inherit(models.Model):
    """Class defining the configuration values of an OAuth2 provider"""

    _inherit = 'auth.oauth.provider'

    secret_key = fields.Char('Secret Key (Secret Value)')
    signin_type = fields.Selection([('Internal', 'Internal'), ('Portal', 'Portal')], default='Portal')

    def new_oauth_token(
            self, type_grant, code=None,
            refresh_token=None, context=None):
        info = dict(
            grant_type=type_grant,
            redirect_uri=request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url') + '/auth/microsoft/signin',
            client_id=self.client_id,
            client_secret=self.secret_key,
        )
        _logger.info('Microsoft SSO INFO (token verification): %s' % info)
        if code:
            info.update({'code': code})
        elif refresh_token:
            info.update({'refresh_token': refresh_token})

        _logger.info('INFO___________________________ %s ' % info)
        _logger.info('validation_endpoint____________ %s ' % self.validation_endpoint)

        res = requests.post(self.validation_endpoint, data=info)
        _logger.info('res_________%s' % (res.text))
        return simplejson.loads(res.text)