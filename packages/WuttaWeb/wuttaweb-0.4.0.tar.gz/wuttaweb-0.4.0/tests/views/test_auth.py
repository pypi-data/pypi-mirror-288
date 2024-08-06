# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock

from pyramid import testing
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from wuttjamaican.conf import WuttaConfig
from wuttaweb.views import auth as mod
from wuttaweb.auth import WuttaSecurityPolicy
from wuttaweb.subscribers import new_request


class TestAuthView(TestCase):

    def setUp(self):
        self.config = WuttaConfig(defaults={
            'wutta.db.default.url': 'sqlite://',
        })

        self.request = testing.DummyRequest(wutta_config=self.config, user=None)
        self.pyramid_config = testing.setUp(request=self.request, settings={
            'wutta_config': self.config,
        })

        self.app = self.config.get_app()
        auth = self.app.get_auth_handler()
        model = self.app.model
        model.Base.metadata.create_all(bind=self.config.appdb_engine)
        self.session = self.app.make_session()
        self.user = model.User(username='barney')
        self.session.add(self.user)
        auth.set_user_password(self.user, 'testpass')
        self.session.commit()

        self.pyramid_config.set_security_policy(WuttaSecurityPolicy(db_session=self.session))
        self.pyramid_config.include('wuttaweb.views.auth')
        self.pyramid_config.include('wuttaweb.views.common')

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        view = mod.AuthView(self.request)
        context = view.login()
        self.assertIn('form', context)

        # redirect if user already logged in
        self.request.user = self.user
        view = mod.AuthView(self.request)
        redirect = view.login(session=self.session)
        self.assertIsInstance(redirect, HTTPFound)

        # login fails w/ wrong password
        self.request.user = None
        self.request.method = 'POST'
        self.request.POST = {'username': 'barney', 'password': 'WRONG'}
        view = mod.AuthView(self.request)
        context = view.login(session=self.session)
        self.assertIn('form', context)

        # redirect if login succeeds
        self.request.method = 'POST'
        self.request.POST = {'username': 'barney', 'password': 'testpass'}
        view = mod.AuthView(self.request)
        redirect = view.login(session=self.session)
        self.assertIsInstance(redirect, HTTPFound)

    def test_logout(self):
        view = mod.AuthView(self.request)
        self.request.session.delete = MagicMock()
        redirect = view.logout()
        self.request.session.delete.assert_called_once_with()
        self.assertIsInstance(redirect, HTTPFound)

    def test_change_password(self):
        view = mod.AuthView(self.request)
        auth = self.app.get_auth_handler()

        # unauthenticated user is redirected
        redirect = view.change_password()
        self.assertIsInstance(redirect, HTTPFound)

        # now "login" the user, and set initial password
        self.request.user = self.user
        auth.set_user_password(self.user, 'foo')
        self.session.commit()

        # view should now return context w/ form
        context = view.change_password()
        self.assertIn('form', context)

        # submit valid form, ensure password is changed
        # (nb. this also would redirect user to home page)
        self.request.method = 'POST'
        self.request.POST = {
            'current_password': 'foo',
            # nb. new_password requires colander mapping structure
            '__start__': 'new_password:mapping',
            'new_password': 'bar',
            'new_password-confirm': 'bar',
            '__end__': 'new_password:mapping',
        }
        redirect = view.change_password()
        self.assertIsInstance(redirect, HTTPFound)
        self.session.commit()
        self.session.refresh(self.user)
        self.assertFalse(auth.check_user_password(self.user, 'foo'))
        self.assertTrue(auth.check_user_password(self.user, 'bar'))

        # at this point 'foo' is the password, now let's submit some
        # invalid forms and make sure we get back a context w/ form

        # first try empty data
        self.request.POST = {}
        context = view.change_password()
        self.assertIn('form', context)
        dform = context['form'].get_deform()
        self.assertEqual(dform['current_password'].errormsg, "Required")
        self.assertEqual(dform['new_password'].errormsg, "Required")

        # now try bad current password
        self.request.POST = {
            'current_password': 'blahblah',
            '__start__': 'new_password:mapping',
            'new_password': 'baz',
            'new_password-confirm': 'baz',
            '__end__': 'new_password:mapping',
        }
        context = view.change_password()
        self.assertIn('form', context)
        dform = context['form'].get_deform()
        self.assertEqual(dform['current_password'].errormsg, "Current password is incorrect.")

        # now try bad new password
        self.request.POST = {
            'current_password': 'bar',
            '__start__': 'new_password:mapping',
            'new_password': 'bar',
            'new_password-confirm': 'bar',
            '__end__': 'new_password:mapping',
        }
        context = view.change_password()
        self.assertIn('form', context)
        dform = context['form'].get_deform()
        self.assertEqual(dform['new_password'].errormsg, "New password must be different from old password.")

    def test_become_root(self):
        event = MagicMock(request=self.request)
        new_request(event)      # add request.get_referrer()
        view = mod.AuthView(self.request)

        # GET not allowed
        self.request.method = 'GET'
        self.assertRaises(HTTPForbidden, view.become_root)

        # non-admin users also not allowed
        self.request.method = 'POST'
        self.request.is_admin = False
        self.assertRaises(HTTPForbidden, view.become_root)

        # but admin users can become root
        self.request.is_admin = True
        self.assertNotIn('is_root', self.request.session)
        redirect = view.become_root()
        self.assertIsInstance(redirect, HTTPFound)
        self.assertTrue(self.request.session['is_root'])

    def test_stop_root(self):
        event = MagicMock(request=self.request)
        new_request(event)      # add request.get_referrer()
        view = mod.AuthView(self.request)

        # GET not allowed
        self.request.method = 'GET'
        self.assertRaises(HTTPForbidden, view.stop_root)

        # non-admin users also not allowed
        self.request.method = 'POST'
        self.request.is_admin = False
        self.assertRaises(HTTPForbidden, view.stop_root)

        # but admin users can stop being root
        # (nb. there is no check whether user is currently root)
        self.request.is_admin = True
        self.assertNotIn('is_root', self.request.session)
        redirect = view.stop_root()
        self.assertIsInstance(redirect, HTTPFound)
        self.assertFalse(self.request.session['is_root'])
