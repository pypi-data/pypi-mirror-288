# -*- coding: utf-8; -*-

from tests.views.utils import WebTestCase

from wuttaweb.views import settings


class TestAppInfoView(WebTestCase):

    def test_index(self):
        # just a sanity check
        view = settings.AppInfoView(self.request)
        response = view.index()
