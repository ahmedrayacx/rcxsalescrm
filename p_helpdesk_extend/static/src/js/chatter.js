/** @odoo-module **/

import FormRenderer from 'web.FormRenderer';

import { registerFieldPatchModel } from '@mail/model/model_core';
import { getMessagingComponent } from "@mail/utils/messaging_component";
import { ChatterContainer } from '@mail/components/chatter_container/chatter_container';
import { patch } from 'web.utils';

const components = { ChatterContainer };

import { attr } from '@mail/model/model_field';

patch(components.ChatterContainer, 'p_helpdesk_extend/static/src/js/chatter.js', {
    props: Object.assign({}, components.ChatterContainer.props, { show_send_message_button: {
            type: Boolean,
            optional: true,
        }
    })
});

registerFieldPatchModel('mail.chatter', 'p_helpdesk_extend/static/src/js/chatter.js', {
    show_send_message_button: attr({
        default: true,
    }),
});

FormRenderer.include({
    _makeChatterContainerProps() {
        var call_super = this._super(...arguments);
        if (this.state.model == 'helpdesk.ticket') {
            call_super['show_send_message_button'] = this.state.data.is_helpdesk
        }
        return call_super
    }
})
