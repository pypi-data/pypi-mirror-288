## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="page_content()">

  <nav class="panel item-panel">
    <p class="panel-heading">Application</p>
    <div class="panel-block">
      <div style="width: 100%;">
        <b-field horizontal label="Distribution">
          <span>${app.get_distribution(obj=app.get_web_handler()) or f'?? - set config for `{app.appname}.app_dist`'}</span>
        </b-field>
        <b-field horizontal label="Version">
          <span>${app.get_version(obj=app.get_web_handler()) or f'?? - set config for `{app.appname}.app_dist`'}</span>
        </b-field>
        <b-field horizontal label="App Title">
          <span>${app.get_title()}</span>
        </b-field>
      </div>
    </div>
  </nav>

  <nav class="panel item-panel">
    <p class="panel-heading">Configuration Files</p>
    <div class="panel-block">
      <div style="width: 100%;">
        <${b}-table :data="configFiles">

          <${b}-table-column field="priority"
                          label="Priority"
                          v-slot="props">
            {{ props.row.priority }}
          </${b}-table-column>

          <${b}-table-column field="path"
                          label="File Path"
                          v-slot="props">
            {{ props.row.path }}
          </${b}-table-column>

        </${b}-table>
      </div>
    </div>
  </nav>

</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script>
    ThisPageData.configFiles = ${json.dumps([dict(path=p, priority=i) for i, p in enumerate(config.get_prioritized_files(), 1)])|n}
  </script>
</%def>


${parent.body()}
