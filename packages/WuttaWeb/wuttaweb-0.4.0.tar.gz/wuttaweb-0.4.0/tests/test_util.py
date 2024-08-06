# -*- coding: utf-8; -*-

from unittest import TestCase

from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttaweb import util


class TestGetLibVer(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.request = testing.DummyRequest()
        self.request.wutta_config = self.config

    def test_buefy_default(self):
        version = util.get_libver(self.request, 'buefy')
        self.assertEqual(version, 'latest')

    def test_buefy_custom_old(self):
        self.config.setdefault('wuttaweb.buefy_version', '0.9.29')
        version = util.get_libver(self.request, 'buefy')
        self.assertEqual(version, '0.9.29')

    def test_buefy_custom_new(self):
        self.config.setdefault('wuttaweb.libver.buefy', '0.9.29')
        version = util.get_libver(self.request, 'buefy')
        self.assertEqual(version, '0.9.29')

    def test_buefy_default_only(self):
        self.config.setdefault('wuttaweb.libver.buefy', '0.9.29')
        version = util.get_libver(self.request, 'buefy', default_only=True)
        self.assertEqual(version, 'latest')

    def test_buefy_css_default(self):
        version = util.get_libver(self.request, 'buefy.css')
        self.assertEqual(version, 'latest')

    def test_buefy_css_custom_old(self):
        # nb. this uses same setting as buefy (js)
        self.config.setdefault('wuttaweb.buefy_version', '0.9.29')
        version = util.get_libver(self.request, 'buefy.css')
        self.assertEqual(version, '0.9.29')

    def test_buefy_css_custom_new(self):
        # nb. this uses same setting as buefy (js)
        self.config.setdefault('wuttaweb.libver.buefy', '0.9.29')
        version = util.get_libver(self.request, 'buefy.css')
        self.assertEqual(version, '0.9.29')

    def test_buefy_css_default_only(self):
        self.config.setdefault('wuttaweb.libver.buefy', '0.9.29')
        version = util.get_libver(self.request, 'buefy.css', default_only=True)
        self.assertEqual(version, 'latest')

    def test_vue_default(self):
        version = util.get_libver(self.request, 'vue')
        self.assertEqual(version, '2.6.14')

    def test_vue_custom_old(self):
        self.config.setdefault('wuttaweb.vue_version', '3.4.31')
        version = util.get_libver(self.request, 'vue')
        self.assertEqual(version, '3.4.31')

    def test_vue_custom_new(self):
        self.config.setdefault('wuttaweb.libver.vue', '3.4.31')
        version = util.get_libver(self.request, 'vue')
        self.assertEqual(version, '3.4.31')

    def test_vue_default_only(self):
        self.config.setdefault('wuttaweb.libver.vue', '3.4.31')
        version = util.get_libver(self.request, 'vue', default_only=True)
        self.assertEqual(version, '2.6.14')

    def test_vue_resource_default(self):
        version = util.get_libver(self.request, 'vue_resource')
        self.assertEqual(version, 'latest')

    def test_vue_resource_custom(self):
        self.config.setdefault('wuttaweb.libver.vue_resource', '1.5.3')
        version = util.get_libver(self.request, 'vue_resource')
        self.assertEqual(version, '1.5.3')

    def test_fontawesome_default(self):
        version = util.get_libver(self.request, 'fontawesome')
        self.assertEqual(version, '5.3.1')

    def test_fontawesome_custom(self):
        self.config.setdefault('wuttaweb.libver.fontawesome', '5.6.3')
        version = util.get_libver(self.request, 'fontawesome')
        self.assertEqual(version, '5.6.3')

    def test_bb_vue_default(self):
        version = util.get_libver(self.request, 'bb_vue')
        self.assertEqual(version, '3.4.31')

    def test_bb_vue_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_vue', '3.4.30')
        version = util.get_libver(self.request, 'bb_vue')
        self.assertEqual(version, '3.4.30')

    def test_bb_oruga_default(self):
        version = util.get_libver(self.request, 'bb_oruga')
        self.assertEqual(version, '0.8.12')

    def test_bb_oruga_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_oruga', '0.8.11')
        version = util.get_libver(self.request, 'bb_oruga')
        self.assertEqual(version, '0.8.11')

    def test_bb_oruga_bulma_default(self):
        version = util.get_libver(self.request, 'bb_oruga_bulma')
        self.assertEqual(version, '0.3.0')
        version = util.get_libver(self.request, 'bb_oruga_bulma_css')
        self.assertEqual(version, '0.3.0')

    def test_bb_oruga_bulma_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_oruga_bulma', '0.2.11')
        version = util.get_libver(self.request, 'bb_oruga_bulma')
        self.assertEqual(version, '0.2.11')

    def test_bb_fontawesome_svg_core_default(self):
        version = util.get_libver(self.request, 'bb_fontawesome_svg_core')
        self.assertEqual(version, '6.5.2')

    def test_bb_fontawesome_svg_core_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_fontawesome_svg_core', '6.5.1')
        version = util.get_libver(self.request, 'bb_fontawesome_svg_core')
        self.assertEqual(version, '6.5.1')

    def test_bb_free_solid_svg_icons_default(self):
        version = util.get_libver(self.request, 'bb_free_solid_svg_icons')
        self.assertEqual(version, '6.5.2')

    def test_bb_free_solid_svg_icons_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_free_solid_svg_icons', '6.5.1')
        version = util.get_libver(self.request, 'bb_free_solid_svg_icons')
        self.assertEqual(version, '6.5.1')

    def test_bb_vue_fontawesome_default(self):
        version = util.get_libver(self.request, 'bb_vue_fontawesome')
        self.assertEqual(version, '3.0.6')

    def test_bb_vue_fontawesome_custom(self):
        self.config.setdefault('wuttaweb.libver.bb_vue_fontawesome', '3.0.8')
        version = util.get_libver(self.request, 'bb_vue_fontawesome')
        self.assertEqual(version, '3.0.8')


class TestGetLibUrl(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.request = testing.DummyRequest()
        self.request.wutta_config = self.config

    def test_buefy_default(self):
        url = util.get_liburl(self.request, 'buefy')
        self.assertEqual(url, 'https://unpkg.com/buefy@latest/dist/buefy.min.js')

    def test_buefy_custom(self):
        self.config.setdefault('wuttaweb.liburl.buefy', '/lib/buefy.js')
        url = util.get_liburl(self.request, 'buefy')
        self.assertEqual(url, '/lib/buefy.js')

    def test_buefy_css_default(self):
        url = util.get_liburl(self.request, 'buefy.css')
        self.assertEqual(url, 'https://unpkg.com/buefy@latest/dist/buefy.min.css')

    def test_buefy_css_custom(self):
        self.config.setdefault('wuttaweb.liburl.buefy.css', '/lib/buefy.css')
        url = util.get_liburl(self.request, 'buefy.css')
        self.assertEqual(url, '/lib/buefy.css')

    def test_vue_default(self):
        url = util.get_liburl(self.request, 'vue')
        self.assertEqual(url, 'https://unpkg.com/vue@2.6.14/dist/vue.min.js')

    def test_vue_custom(self):
        self.config.setdefault('wuttaweb.liburl.vue', '/lib/vue.js')
        url = util.get_liburl(self.request, 'vue')
        self.assertEqual(url, '/lib/vue.js')

    def test_vue_resource_default(self):
        url = util.get_liburl(self.request, 'vue_resource')
        self.assertEqual(url, 'https://cdn.jsdelivr.net/npm/vue-resource@latest')

    def test_vue_resource_custom(self):
        self.config.setdefault('wuttaweb.liburl.vue_resource', '/lib/vue-resource.js')
        url = util.get_liburl(self.request, 'vue_resource')
        self.assertEqual(url, '/lib/vue-resource.js')

    def test_fontawesome_default(self):
        url = util.get_liburl(self.request, 'fontawesome')
        self.assertEqual(url, 'https://use.fontawesome.com/releases/v5.3.1/js/all.js')

    def test_fontawesome_custom(self):
        self.config.setdefault('wuttaweb.liburl.fontawesome', '/lib/fontawesome.js')
        url = util.get_liburl(self.request, 'fontawesome')
        self.assertEqual(url, '/lib/fontawesome.js')

    def test_bb_vue_default(self):
        url = util.get_liburl(self.request, 'bb_vue')
        self.assertEqual(url, 'https://unpkg.com/vue@3.4.31/dist/vue.esm-browser.prod.js')

    def test_bb_vue_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_vue', '/lib/vue.js')
        url = util.get_liburl(self.request, 'bb_vue')
        self.assertEqual(url, '/lib/vue.js')

    def test_bb_oruga_default(self):
        url = util.get_liburl(self.request, 'bb_oruga')
        self.assertEqual(url, 'https://unpkg.com/@oruga-ui/oruga-next@0.8.12/dist/oruga.mjs')

    def test_bb_oruga_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_oruga', '/lib/oruga.js')
        url = util.get_liburl(self.request, 'bb_oruga')
        self.assertEqual(url, '/lib/oruga.js')

    def test_bb_oruga_bulma_default(self):
        url = util.get_liburl(self.request, 'bb_oruga_bulma')
        self.assertEqual(url, 'https://unpkg.com/@oruga-ui/theme-bulma@0.3.0/dist/bulma.mjs')

    def test_bb_oruga_bulma_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_oruga_bulma', '/lib/oruga_bulma.js')
        url = util.get_liburl(self.request, 'bb_oruga_bulma')
        self.assertEqual(url, '/lib/oruga_bulma.js')

    def test_bb_oruga_bulma_css_default(self):
        url = util.get_liburl(self.request, 'bb_oruga_bulma_css')
        self.assertEqual(url, 'https://unpkg.com/@oruga-ui/theme-bulma@0.3.0/dist/bulma.css')

    def test_bb_oruga_bulma_css_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_oruga_bulma_css', '/lib/oruga-bulma.css')
        url = util.get_liburl(self.request, 'bb_oruga_bulma_css')
        self.assertEqual(url, '/lib/oruga-bulma.css')

    def test_bb_fontawesome_svg_core_default(self):
        url = util.get_liburl(self.request, 'bb_fontawesome_svg_core')
        self.assertEqual(url, 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-svg-core@6.5.2/+esm')

    def test_bb_fontawesome_svg_core_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_fontawesome_svg_core', '/lib/fontawesome-svg-core.js')
        url = util.get_liburl(self.request, 'bb_fontawesome_svg_core')
        self.assertEqual(url, '/lib/fontawesome-svg-core.js')

    def test_bb_free_solid_svg_icons_default(self):
        url = util.get_liburl(self.request, 'bb_free_solid_svg_icons')
        self.assertEqual(url, 'https://cdn.jsdelivr.net/npm/@fortawesome/free-solid-svg-icons@6.5.2/+esm')

    def test_bb_free_solid_svg_icons_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_free_solid_svg_icons', '/lib/free-solid-svg-icons.js')
        url = util.get_liburl(self.request, 'bb_free_solid_svg_icons')
        self.assertEqual(url, '/lib/free-solid-svg-icons.js')

    def test_bb_vue_fontawesome_default(self):
        url = util.get_liburl(self.request, 'bb_vue_fontawesome')
        self.assertEqual(url, 'https://cdn.jsdelivr.net/npm/@fortawesome/vue-fontawesome@3.0.6/+esm')

    def test_bb_vue_fontawesome_custom(self):
        self.config.setdefault('wuttaweb.liburl.bb_vue_fontawesome', '/lib/vue-fontawesome.js')
        url = util.get_liburl(self.request, 'bb_vue_fontawesome')
        self.assertEqual(url, '/lib/vue-fontawesome.js')


class TestGetFormData(TestCase):

    def setUp(self):
        self.config = WuttaConfig()

    def make_request(self, **kwargs):
        kwargs.setdefault('wutta_config', self.config)
        kwargs.setdefault('POST', {'foo1': 'bar'})
        kwargs.setdefault('json_body', {'foo2': 'baz'})
        return testing.DummyRequest(**kwargs)

    def test_default(self):
        request = self.make_request()
        data = util.get_form_data(request)
        self.assertEqual(data, {'foo1': 'bar'})

    def test_is_xhr(self):
        request = self.make_request(POST=None, is_xhr=True)
        data = util.get_form_data(request)
        self.assertEqual(data, {'foo2': 'baz'})

    def test_content_type(self):
        request = self.make_request(POST=None, content_type='application/json')
        data = util.get_form_data(request)
        self.assertEqual(data, {'foo2': 'baz'})
