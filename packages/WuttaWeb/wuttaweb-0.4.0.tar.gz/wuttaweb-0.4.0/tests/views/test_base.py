# -*- coding: utf-8; -*-

from unittest import TestCase

from pyramid import testing
from pyramid.httpexceptions import HTTPFound, HTTPForbidden, HTTPNotFound

from wuttjamaican.conf import WuttaConfig
from wuttaweb.views import base
from wuttaweb.forms import Form


class TestView(TestCase):

    def setUp(self):
        self.config = WuttaConfig()
        self.app = self.config.get_app()
        self.request = testing.DummyRequest(wutta_config=self.config)
        self.view = base.View(self.request)

    def test_basic(self):
        self.assertIs(self.view.request, self.request)
        self.assertIs(self.view.config, self.config)
        self.assertIs(self.view.app, self.app)

    def test_forbidden(self):
        error = self.view.forbidden()
        self.assertIsInstance(error, HTTPForbidden)

    def test_make_form(self):
        form = self.view.make_form()
        self.assertIsInstance(form, Form)

    def test_notfound(self):
        error = self.view.notfound()
        self.assertIsInstance(error, HTTPNotFound)

    def test_redirect(self):
        error = self.view.redirect('/')
        self.assertIsInstance(error, HTTPFound)
        self.assertEqual(error.location, '/')
