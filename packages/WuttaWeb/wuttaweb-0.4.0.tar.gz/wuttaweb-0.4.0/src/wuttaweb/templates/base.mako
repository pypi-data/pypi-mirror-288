## -*- coding: utf-8; -*-
<%namespace name="base_meta" file="/base_meta.mako" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${base_meta.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${base_meta.favicon()}
    ${self.header_core()}
    ${self.head_tags()}
  </head>
  <body>
    <div id="app" style="height: 100%;">
      <whole-page />
    </div>

    ## content body from derived/child template
    ${self.body()}

    ## Vue app
    ${self.make_whole_page_component()}
    ${self.make_whole_page_app()}
  </body>
</html>

<%def name="title()"></%def>

<%def name="content_title()">${self.title()}</%def>

<%def name="header_core()">
  ${self.core_javascript()}
  ${self.extra_javascript()}
  ${self.core_styles()}
  ${self.extra_styles()}
</%def>

<%def name="core_javascript()">
  ${self.vuejs()}
  ${self.buefy()}
  ${self.fontawesome()}

  <script>

    ## NOTE: this code was copied from
    ## https://bulma.io/documentation/components/navbar/#navbar-menu

    document.addEventListener('DOMContentLoaded', () => {

        // Get all "navbar-burger" elements
        const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0)

        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target
                const $target = document.getElementById(target)

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active')
                $target.classList.toggle('is-active')

            })
        })
    })

  </script>
</%def>

<%def name="vuejs()">
  ${h.javascript_link(h.get_liburl(request, 'vue'))}
  ${h.javascript_link(h.get_liburl(request, 'vue_resource'))}
</%def>

<%def name="buefy()">
  ${h.javascript_link(h.get_liburl(request, 'buefy'))}
</%def>

<%def name="fontawesome()">
  <script defer src="${h.get_liburl(request, 'fontawesome')}"></script>
</%def>

<%def name="extra_javascript()"></%def>

<%def name="core_styles()">
  ${self.buefy_styles()}

  <style>

    /* ****************************** */
    /* page */
    /* ****************************** */

    /* nb. helps force footer to bottom of screen */
    html, body {
        height: 100%;
    }

    % if not request.wutta_config.production():
        html, .navbar, .footer {
          background-image: url(${request.static_url('wuttaweb:static/img/testing.png')});
        }
    % endif

    /* nb. this refers to the "menu-sized" app title in far left of main menu */
    #global-header-title {
        font-weight: bold;
    }

    #current-context {
        padding-left: 0.5rem;
    }

    h1.title {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0 !important;
    }

    #content-title h1 {
        max-width: 50%;
        overflow: hidden;
        padding-left: 0.5rem;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

  </style>
</%def>

<%def name="buefy_styles()">
  ${h.stylesheet_link(h.get_liburl(request, 'buefy.css'))}
</%def>

<%def name="extra_styles()">
  ${base_meta.extra_styles()}
</%def>

<%def name="head_tags()"></%def>

<%def name="render_whole_page_template()">
  <script type="text/x-template" id="whole-page-template">
    <div id="whole-page"
         style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">

      <div class="header-wrapper">

        <header>
          <nav class="navbar" role="navigation" aria-label="main navigation">

            <div class="navbar-brand">
              <a class="navbar-item" href="${url('home')}">
                <div style="display: flex; gap: 0.3rem; align-items: center;">
                  ${base_meta.header_logo()}
                  <div id="global-header-title">
                    ${base_meta.global_title()}
                  </div>
                </div>
              </a>
              <a role="button" class="navbar-burger" data-target="navbar-menu" aria-label="menu" aria-expanded="false">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
              </a>
            </div>

            <div class="navbar-menu" id="navbar-menu">
              <div class="navbar-start">

                % for topitem in menus:
                    % if topitem['is_link']:
                        ${h.link_to(topitem['title'], topitem['url'], target=topitem['target'], class_='navbar-item')}
                    % else:
                        <div class="navbar-item has-dropdown is-hoverable">
                          <a class="navbar-link">${topitem['title']}</a>
                          <div class="navbar-dropdown">
                            % for item in topitem['items']:
                                % if item['is_menu']:
                                    <% item_hash = id(item) %>
                                    <% toggle = 'menu_{}_shown'.format(item_hash) %>
                                    <div>
                                      <a class="navbar-link" @click.prevent="toggleNestedMenu('${item_hash}')">
                                        ${item['title']}
                                      </a>
                                    </div>
                                    % for subitem in item['items']:
                                        % if subitem['is_sep']:
                                            <hr class="navbar-divider" v-show="${toggle}">
                                        % else:
                                            ${h.link_to("{}".format(subitem['title']), subitem['url'], class_='navbar-item nested', target=subitem['target'], **{'v-show': toggle})}
                                        % endif
                                    % endfor
                                % else:
                                    % if item['is_sep']:
                                        <hr class="navbar-divider">
                                    % else:
                                        ${h.link_to(item['title'], item['url'], class_='navbar-item', target=item['target'])}
                                    % endif
                                % endif
                            % endfor
                          </div>
                        </div>
                    % endif
                % endfor

              </div><!-- navbar-start -->
              ${self.render_navbar_end()}
            </div>
          </nav>

          <nav class="level" style="margin: 0.5rem auto;">
            <div class="level-left">

              ## Current Context
              <div id="current-context" class="level-item">
                % if index_title:
                    % if index_url:
                        <span class="header-text">
                          ${h.link_to(index_title, index_url)}
                        </span>
                    % else:
                        <h1 class="title">${index_title}</h1>
                    % endif
                % endif
              </div>

            </div><!-- level-left -->
          </nav><!-- level -->
        </header>

        ## Page Title
        % if capture(self.content_title):
            <section id="content-title"
                     class="has-background-primary">
              <div style="display: flex; align-items: center; padding: 0.5rem;">

                <h1 class="title has-text-white"
                    v-html="contentTitleHTML">
                </h1>

                <div style="flex-grow: 1; display: flex; gap: 0.5rem;">
                  ${self.render_instance_header_title_extras()}
                </div>

                <div style="display: flex; gap: 0.5rem;">
                  ${self.render_instance_header_buttons()}
                </div>

              </div>
            </section>
        % endif

      </div> <!-- header-wrapper -->

      <div class="content-wrapper"
           style="flex-grow: 1; padding: 0.5rem;">

        ## Page Body
        <section id="page-body" style="height: 100%;">

          % if request.session.peek_flash('error'):
              % for error in request.session.pop_flash('error'):
                  <b-notification type="is-warning">
                    ${error}
                  </b-notification>
              % endfor
          % endif

          % if request.session.peek_flash('warning'):
              % for msg in request.session.pop_flash('warning'):
                  <b-notification type="is-warning">
                    ${msg}
                  </b-notification>
              % endfor
          % endif

          % if request.session.peek_flash():
              % for msg in request.session.pop_flash():
                  <b-notification type="is-info">
                    ${msg}
                  </b-notification>
              % endfor
          % endif

          <div style="height: 100%;">
            ${self.render_this_page_component()}
          </div>
        </section>

      </div><!-- content-wrapper -->

      ## Footer
      <footer class="footer">
        <div class="content">
          ${base_meta.footer()}
        </div>
      </footer>

    </div>
  </script>
</%def>

<%def name="render_this_page_component()">
  <this-page @change-content-title="changeContentTitle" />
</%def>

<%def name="render_navbar_end()">
  <div class="navbar-end">
    ${self.render_user_menu()}
  </div>
</%def>

<%def name="render_user_menu()">
  % if request.user:
      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link ${'has-background-danger has-text-white' if request.is_root else ''}">${request.user}</a>
        <div class="navbar-dropdown">
          % if request.is_root:
              ${h.form(url('stop_root'), ref='stopBeingRootForm')}
              ## TODO
              ## ${h.csrf_token(request)}
              <input type="hidden" name="referrer" value="${request.current_route_url()}" />
              <a @click="stopBeingRoot()"
                 class="navbar-item has-background-danger has-text-white">
                Stop being root
              </a>
              ${h.end_form()}
          % elif request.is_admin:
              ${h.form(url('become_root'), ref='startBeingRootForm')}
              ## TODO
              ## ${h.csrf_token(request)}
              <input type="hidden" name="referrer" value="${request.current_route_url()}" />
              <a @click="startBeingRoot()"
                 class="navbar-item has-background-danger has-text-white">
                Become root
              </a>
              ${h.end_form()}
          % endif
          ${h.link_to("Change Password", url('change_password'), class_='navbar-item')}
          ${h.link_to("Logout", url('logout'), class_='navbar-item')}
        </div>
      </div>
  % else:
      ${h.link_to("Login", url('login'), class_='navbar-item')}
  % endif
</%def>

<%def name="render_instance_header_title_extras()"></%def>

<%def name="render_instance_header_buttons()">
  ${self.render_crud_header_buttons()}
  ${self.render_prevnext_header_buttons()}
</%def>

<%def name="render_crud_header_buttons()"></%def>

<%def name="render_prevnext_header_buttons()"></%def>

<%def name="declare_whole_page_vars()">
  <script>

    let WholePage = {
        template: '#whole-page-template',
        computed: {},

        mounted() {
            for (let hook of this.mountedHooks) {
                hook(this)
            }
        },

        methods: {

            changeContentTitle(newTitle) {
                this.contentTitleHTML = newTitle
            },

            toggleNestedMenu(hash) {
                const key = 'menu_' + hash + '_shown'
                this[key] = !this[key]
            },

            % if request.is_admin:

                startBeingRoot() {
                    this.$refs.startBeingRootForm.submit()
                },

                stopBeingRoot() {
                    this.$refs.stopBeingRootForm.submit()
                },

            % endif
        },
    }

    let WholePageData = {
        contentTitleHTML: ${json.dumps(capture(self.content_title))|n},
        mountedHooks: [],
    }

    ## declare nested menu visibility toggle flags
    % for topitem in menus:
        % if topitem['is_menu']:
            % for item in topitem['items']:
                % if item['is_menu']:
                    WholePageData.menu_${id(item)}_shown = false
                % endif
            % endfor
        % endif
    % endfor

  </script>
</%def>

<%def name="modify_whole_page_vars()"></%def>

<%def name="finalize_whole_page_vars()"></%def>

<%def name="make_whole_page_component()">
  ${self.render_whole_page_template()}
  ${self.declare_whole_page_vars()}
  ${self.modify_whole_page_vars()}
  ${self.finalize_whole_page_vars()}

  <script>

    WholePage.data = function() { return WholePageData }
    Vue.component('whole-page', WholePage)

  </script>
</%def>

<%def name="make_whole_page_app()">
  <script>

    new Vue({
        el: '#app'
    })

  </script>
</%def>
