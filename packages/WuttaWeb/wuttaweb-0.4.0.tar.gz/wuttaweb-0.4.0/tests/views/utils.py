# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock

from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttaweb import subscribers


class WebTestCase(TestCase):
    """
    Base class for test suites requiring a full (typical) web app.
    """

    def setUp(self):
        self.setup_web()

    def setup_web(self):
        self.config = WuttaConfig(defaults={
            'wutta.db.default.url': 'sqlite://',
            'wutta.web.menus.handler_spec': 'tests.utils:NullMenuHandler',
        })

        self.request = testing.DummyRequest()

        self.pyramid_config = testing.setUp(request=self.request, settings={
            'wutta_config': self.config,
            'mako.directories': ['wuttaweb:templates'],
        })

        # init db
        self.app = self.config.get_app()
        model = self.app.model
        model.Base.metadata.create_all(bind=self.config.appdb_engine)
        self.session = self.app.make_session()

        # init web
        self.pyramid_config.include('pyramid_mako')
        self.pyramid_config.include('wuttaweb.static')
        self.pyramid_config.include('wuttaweb.views.essential')
        self.pyramid_config.add_subscriber('wuttaweb.subscribers.before_render',
                                           'pyramid.events.BeforeRender')

        # setup new request w/ anonymous user
        event = MagicMock(request=self.request)
        subscribers.new_request(event)
        def user_getter(request, **kwargs): pass
        subscribers.new_request_set_user(event, db_session=self.session,
                                         user_getter=user_getter)

    def tearDown(self):
        self.teardown_web()

    def teardown_web(self):
        testing.tearDown()
