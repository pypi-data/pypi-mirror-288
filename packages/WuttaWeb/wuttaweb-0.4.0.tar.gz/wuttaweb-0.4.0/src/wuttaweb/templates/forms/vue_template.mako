## -*- coding: utf-8; -*-

<script type="text/x-template" id="${form.vue_tagname}-template">
  ${h.form(form.action_url, method='post', enctype='multipart/form-data', **form_attrs)}

    <section>
      % for fieldname in form:
          ${form.render_vue_field(fieldname)}
      % endfor
    </section>

    <div style="margin-top: 1.5rem; display: flex; gap: 0.5rem; justify-content: ${'end' if form.align_buttons_right else 'start'}; width: 100%; padding-left: 10rem;">

      % if form.show_button_reset:
          <b-button native-type="reset">
            Reset
          </b-button>
      % endif

      <b-button type="is-primary"
                native-type="submit"
                % if form.auto_disable_submit:
                    :disabled="formSubmitting"
                % endif
                icon-pack="fas"
                icon-left="${form.button_icon_submit}">
        % if form.auto_disable_submit:
            {{ formSubmitting ? "Working, please wait..." : "${form.button_label_submit}" }}
        % else:
            ${form.button_label_submit}
        % endif
      </b-button>

    </div>

  ${h.end_form()}
</script>

<script>

  let ${form.vue_component} = {
      template: '#${form.vue_tagname}-template',
      methods: {},
  }

  let ${form.vue_component}Data = {

      ## field model values
      % for key in form:
          model_${key}: ${form.get_vue_field_value(key)|n},
      % endfor

      % if form.auto_disable_submit:
          formSubmitting: false,
      % endif
  }

</script>
