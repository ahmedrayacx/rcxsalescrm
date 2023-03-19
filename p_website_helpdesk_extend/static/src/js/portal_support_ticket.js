odoo.define('p_website_helpdesk_extend.support_ticket', function (require) {
    "use strict";
    require('web.dom_ready');
    var ajax = require('web.ajax');

    $(document).ready(function() {
        const forms = document.querySelectorAll('.support-ticket')
        Array.from(forms).forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
        $("form.support-ticket input[name='team_id']").on("change", function(ev){
            $("form.support-ticket #support_type_id").val('')
            $("form.support-ticket #support_type_id option").addClass('d-none')
            $("form.support-ticket #support_type_id option[team='"+$(ev.currentTarget).val()+"']").removeClass('d-none')
        });
        $("form.support-ticket select[name='type_id']").on("change", function(ev){
            $("form.support-ticket #support_type_id_1").val('')
            $("form.support-ticket #support_type_id_1 option").addClass('d-none')
            $("form.support-ticket #support_type_id_1 option[type='"+$(ev.currentTarget).val()+"']").removeClass('d-none')
        });
        $("form.support-ticket #support_site_id").on("change", function(ev){
            $("form.support-ticket #support_project_id").val('')
            $("form.support-ticket #support_project_id option").addClass('d-none')
            $("form.support-ticket #support_project_id option[site_id='"+$(ev.currentTarget).val()+"']").removeClass('d-none')
        });
    });
})