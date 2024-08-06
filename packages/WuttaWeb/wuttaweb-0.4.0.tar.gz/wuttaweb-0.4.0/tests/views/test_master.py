# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock

from pyramid import testing
from pyramid.response import Response

from wuttjamaican.conf import WuttaConfig
from wuttaweb.views import master
from wuttaweb.subscribers import new_request_set_user


class TestMasterView(TestCase):

    def setUp(self):
        self.config = WuttaConfig(defaults={
            'wutta.web.menus.handler_spec': 'tests.utils:NullMenuHandler',
        })
        self.app = self.config.get_app()
        self.request = testing.DummyRequest(wutta_config=self.config, use_oruga=False)
        self.pyramid_config = testing.setUp(request=self.request, settings={
            'wutta_config': self.config,
            'mako.directories': ['wuttaweb:templates'],
        })
        self.pyramid_config.include('pyramid_mako')
        self.pyramid_config.include('wuttaweb.static')
        self.pyramid_config.include('wuttaweb.views.essential')
        self.pyramid_config.add_subscriber('wuttaweb.subscribers.before_render',
                                           'pyramid.events.BeforeRender')

        event = MagicMock(request=self.request)
        new_request_set_user(event)

    def tearDown(self):
        testing.tearDown()

    def test_defaults(self):
        master.MasterView.model_name = 'Widget'
        # TODO: should inspect pyramid routes after this, to be certain
        master.MasterView.defaults(self.pyramid_config)
        del master.MasterView.model_name

    ##############################
    # class methods
    ##############################

    def test_get_model_class(self):
        
        # no model class by default
        self.assertIsNone(master.MasterView.get_model_class())

        # subclass may specify
        MyModel = MagicMock()
        master.MasterView.model_class = MyModel
        self.assertIs(master.MasterView.get_model_class(), MyModel)
        del master.MasterView.model_class

    def test_get_model_name(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_name)

        # subclass may specify model name
        master.MasterView.model_name = 'Widget'
        self.assertEqual(master.MasterView.get_model_name(), 'Widget')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Blaster')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_model_name(), 'Blaster')
        del master.MasterView.model_class

    def test_get_model_name_normalized(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_name_normalized)

        # subclass may specify *normalized* model name
        master.MasterView.model_name_normalized = 'widget'
        self.assertEqual(master.MasterView.get_model_name_normalized(), 'widget')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_name_normalized(), 'blaster')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_model_name_normalized(), 'dinosaur')
        del master.MasterView.model_class

    def test_get_model_title(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_title)

        # subclass may specify  model title
        master.MasterView.model_title = 'Wutta Widget'
        self.assertEqual(master.MasterView.get_model_title(), "Wutta Widget")
        del master.MasterView.model_title

        # or it may specify model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_title(), "Blaster")
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_model_title(), "Dinosaur")
        del master.MasterView.model_class

    def test_get_model_title_plural(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_model_title_plural)

        # subclass may specify *plural* model title
        master.MasterView.model_title_plural = 'People'
        self.assertEqual(master.MasterView.get_model_title_plural(), "People")
        del master.MasterView.model_title_plural

        # or it may specify *singular* model title
        master.MasterView.model_title = 'Wutta Widget'
        self.assertEqual(master.MasterView.get_model_title_plural(), "Wutta Widgets")
        del master.MasterView.model_title

        # or it may specify model name
        master.MasterView.model_name = 'Blaster'
        self.assertEqual(master.MasterView.get_model_title_plural(), "Blasters")
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Dinosaur')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_model_title_plural(), "Dinosaurs")
        del master.MasterView.model_class

    def test_get_route_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_route_prefix)

        # subclass may specify route prefix
        master.MasterView.route_prefix = 'widgets'
        self.assertEqual(master.MasterView.get_route_prefix(), 'widgets')
        del master.MasterView.route_prefix

        # subclass may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_route_prefix(), 'blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_route_prefix(), 'dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Truck')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_route_prefix(), 'trucks')
        del master.MasterView.model_class

    def test_get_url_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_url_prefix)

        # subclass may specify url prefix
        master.MasterView.url_prefix = '/widgets'
        self.assertEqual(master.MasterView.get_url_prefix(), '/widgets')
        del master.MasterView.url_prefix

        # or it may specify route prefix
        master.MasterView.route_prefix = 'trucks'
        self.assertEqual(master.MasterView.get_url_prefix(), '/trucks')
        del master.MasterView.route_prefix

        # or it may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_url_prefix(), '/blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_url_prefix(), '/dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Machine')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_url_prefix(), '/machines')
        del master.MasterView.model_class

    def test_get_template_prefix(self):
        
        # error by default (since no model class)
        self.assertRaises(AttributeError, master.MasterView.get_template_prefix)

        # subclass may specify template prefix
        master.MasterView.template_prefix = '/widgets'
        self.assertEqual(master.MasterView.get_template_prefix(), '/widgets')
        del master.MasterView.template_prefix

        # or it may specify url prefix
        master.MasterView.url_prefix = '/trees'
        self.assertEqual(master.MasterView.get_template_prefix(), '/trees')
        del master.MasterView.url_prefix

        # or it may specify route prefix
        master.MasterView.route_prefix = 'trucks'
        self.assertEqual(master.MasterView.get_template_prefix(), '/trucks')
        del master.MasterView.route_prefix

        # or it may specify *normalized* model name
        master.MasterView.model_name_normalized = 'blaster'
        self.assertEqual(master.MasterView.get_template_prefix(), '/blasters')
        del master.MasterView.model_name_normalized

        # or it may specify *standard* model name
        master.MasterView.model_name = 'Dinosaur'
        self.assertEqual(master.MasterView.get_template_prefix(), '/dinosaurs')
        del master.MasterView.model_name

        # or it may specify model class
        MyModel = MagicMock(__name__='Machine')
        master.MasterView.model_class = MyModel
        self.assertEqual(master.MasterView.get_template_prefix(), '/machines')
        del master.MasterView.model_class

    ##############################
    # support methods
    ##############################

    def test_get_index_title(self):
        master.MasterView.model_title_plural = "Wutta Widgets"
        view = master.MasterView(self.request)
        self.assertEqual(view.get_index_title(), "Wutta Widgets")
        del master.MasterView.model_title_plural

    def test_render_to_response(self):

        # basic sanity check using /master/index.mako
        # (nb. it skips /widgets/index.mako since that doesn't exist)
        master.MasterView.model_name = 'Widget'
        view = master.MasterView(self.request)
        response = view.render_to_response('index', {})
        self.assertIsInstance(response, Response)
        del master.MasterView.model_name

        # basic sanity check using /appinfo/index.mako
        master.MasterView.model_name = 'AppInfo'
        master.MasterView.template_prefix = '/appinfo'
        view = master.MasterView(self.request)
        response = view.render_to_response('index', {})
        self.assertIsInstance(response, Response)
        del master.MasterView.model_name
        del master.MasterView.template_prefix

        # bad template name causes error
        master.MasterView.model_name = 'Widget'
        self.assertRaises(IOError, view.render_to_response, 'nonexistent', {})
        del master.MasterView.model_name

    ##############################
    # view methods
    ##############################

    def test_index(self):
        
        # basic sanity check using /appinfo
        master.MasterView.model_name = 'AppInfo'
        master.MasterView.template_prefix = '/appinfo'
        view = master.MasterView(self.request)
        response = view.index()
        del master.MasterView.model_name
        del master.MasterView.template_prefix
