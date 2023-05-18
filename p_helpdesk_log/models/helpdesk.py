from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def write(self, vals):
        fields_list = []
        fields_data = {}
        old_val = []
        if self.is_helpdesk or vals.get('is_helpdesk') == True:
            fields_data = self.fields_get()
            fields_list = list(vals.keys())
            old_val = self.read(fields_list)
        call_super = super(HelpdeskTicket, self).write(vals)
        if self.is_helpdesk or vals.get('is_helpdesk') == True:
            new_val = self.read(fields_list)
            msg_lst = []
            for val in vals:
                field_string = fields_data[val]['string'] + ' : '
                old_value = old_val and old_val[0][val]
                new_value = new_val and new_val[0][val]

                if fields_data[val]['type'] not in ['one2many', 'many2many']:
                    if fields_data[val]['type'] == 'many2one':
                        if old_value:
                            old_value = old_value[1]
                        if new_value:
                            new_value = new_value[1]

                    message = _(field_string + ((str(old_value) + ' ---> ') if old_value else '') + (str(new_value) if new_value else ''))
                    msg_lst.append(message)

            if msg_lst:
                email_values_new = {
                    'message': msg_lst
                }
                self.send_ticket_mail(email_values_new)
        return call_super

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        message = super(HelpdeskTicket, self).message_post(**kwargs)
        email_values_new = {
            'message': [kwargs.get('body')]
        }
        self.send_ticket_mail(email_values_new)
        return message

    def send_ticket_mail(self, ticket_context={}):
        email_to = []
        user_partner_id = self.env.user.partner_id
        if user_partner_id != self.partner_id and (self.partner_email or self.partner_id.email):
            email_to += [self.partner_email or self.partner_id.email]

        if user_partner_id != self.user_id.partner_id and self.user_id.partner_id.email:
            email_to += [self.user_id.email]

        email_values = {
            'email_to': ','.join(email_to)
        }
        mail_template = self.env.ref(
            'p_helpdesk_log.email_template_helpdesk_ticket')
        if mail_template:
            mail_template.with_context(ticket_context).send_mail(self.id, email_values=email_values, force_send=True)