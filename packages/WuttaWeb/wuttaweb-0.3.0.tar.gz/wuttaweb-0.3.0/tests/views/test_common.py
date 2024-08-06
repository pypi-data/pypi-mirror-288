# -*- coding: utf-8; -*-

from unittest import TestCase

from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttaweb.views import common


class TestCommonView(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.app = self.config.get_app()
        self.request = testing.DummyRequest()
        self.request.wutta_config = self.config
        self.pyramid_config = testing.setUp(request=self.request)
        self.pyramid_config.include('wuttaweb.views.common')

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        view = common.CommonView(self.request)
        context = view.home()
        self.assertEqual(context['index_title'], self.app.get_title())
