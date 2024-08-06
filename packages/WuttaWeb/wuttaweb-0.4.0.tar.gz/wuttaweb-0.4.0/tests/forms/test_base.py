# -*- coding: utf-8; -*-

from unittest import TestCase
from unittest.mock import MagicMock

import colander
import deform
from pyramid import testing

from wuttjamaican.conf import WuttaConfig
from wuttaweb.forms import base
from wuttaweb import helpers


class TestFieldList(TestCase):

    def test_insert_before(self):
        fields = base.FieldList(['f1', 'f2'])
        self.assertEqual(fields, ['f1', 'f2'])

        # typical
        fields.insert_before('f1', 'XXX')
        self.assertEqual(fields, ['XXX', 'f1', 'f2'])
        fields.insert_before('f2', 'YYY')
        self.assertEqual(fields, ['XXX', 'f1', 'YYY', 'f2'])

        # appends new field if reference field is invalid
        fields.insert_before('f3', 'ZZZ')
        self.assertEqual(fields, ['XXX', 'f1', 'YYY', 'f2', 'ZZZ'])

    def test_insert_after(self):
        fields = base.FieldList(['f1', 'f2'])
        self.assertEqual(fields, ['f1', 'f2'])

        # typical
        fields.insert_after('f1', 'XXX')
        self.assertEqual(fields, ['f1', 'XXX', 'f2'])
        fields.insert_after('XXX', 'YYY')
        self.assertEqual(fields, ['f1', 'XXX', 'YYY', 'f2'])

        # appends new field if reference field is invalid
        fields.insert_after('f3', 'ZZZ')
        self.assertEqual(fields, ['f1', 'XXX', 'YYY', 'f2', 'ZZZ'])


class TestForm(TestCase):

    def setUp(self):
        self.config = WuttaConfig(defaults={
            'wutta.web.menus.handler_spec': 'tests.utils:NullMenuHandler',
        })
        self.request = testing.DummyRequest(wutta_config=self.config, use_oruga=False)

        self.pyramid_config = testing.setUp(request=self.request, settings={
            'mako.directories': ['wuttaweb:templates'],
            'pyramid_deform.template_search_path': 'wuttaweb:templates/deform',
        })

    def tearDown(self):
        testing.tearDown()

    def make_form(self, request=None, **kwargs):
        return base.Form(request or self.request, **kwargs)

    def make_schema(self):
        schema = colander.Schema(children=[
            colander.SchemaNode(colander.String(),
                                name='foo'),
            colander.SchemaNode(colander.String(),
                                name='bar'),
        ])
        return schema

    def test_init_with_none(self):
        form = self.make_form()
        self.assertIsNone(form.fields)

    def test_init_with_fields(self):
        form = self.make_form(fields=['foo', 'bar'])
        self.assertEqual(form.fields, ['foo', 'bar'])

    def test_init_with_schema(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        self.assertEqual(form.fields, ['foo', 'bar'])

    def test_vue_tagname(self):
        form = self.make_form()
        self.assertEqual(form.vue_tagname, 'wutta-form')

    def test_vue_component(self):
        form = self.make_form()
        self.assertEqual(form.vue_component, 'WuttaForm')

    def test_contains(self):
        form = self.make_form(fields=['foo', 'bar'])
        self.assertIn('foo', form)
        self.assertNotIn('baz', form)

    def test_iter(self):
        form = self.make_form(fields=['foo', 'bar'])

        fields = list(iter(form))
        self.assertEqual(fields, ['foo', 'bar'])

        fields = []
        for field in form:
            fields.append(field)
        self.assertEqual(fields, ['foo', 'bar'])

    def test_set_fields(self):
        form = self.make_form(fields=['foo', 'bar'])
        self.assertEqual(form.fields, ['foo', 'bar'])
        form.set_fields(['baz'])
        self.assertEqual(form.fields, ['baz'])

    def test_get_schema(self):
        form = self.make_form()
        self.assertIsNone(form.schema)

        # provided schema is returned
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        self.assertIs(form.schema, schema)
        self.assertIs(form.get_schema(), schema)

        # auto-generating schema not yet supported
        form = self.make_form(fields=['foo', 'bar'])
        self.assertIsNone(form.schema)
        self.assertRaises(NotImplementedError, form.get_schema)

    def test_get_deform(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        self.assertFalse(hasattr(form, 'deform_form'))
        dform = form.get_deform()
        self.assertIsInstance(dform, deform.Form)
        self.assertIs(form.deform_form, dform)

    def test_get_label(self):
        form = self.make_form(fields=['foo', 'bar'])
        self.assertEqual(form.get_label('foo'), "Foo")
        form.set_label('foo', "Baz")
        self.assertEqual(form.get_label('foo'), "Baz")

    def test_set_label(self):
        form = self.make_form(fields=['foo', 'bar'])
        self.assertEqual(form.get_label('foo'), "Foo")
        form.set_label('foo', "Baz")
        self.assertEqual(form.get_label('foo'), "Baz")

        # schema should be updated when setting label
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        form.set_label('foo', "Woohoo")
        self.assertEqual(form.get_label('foo'), "Woohoo")
        self.assertEqual(schema['foo'].title, "Woohoo")

    def test_render_vue_tag(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        html = form.render_vue_tag()
        self.assertEqual(html, '<wutta-form></wutta-form>')

    def test_render_vue_template(self):
        self.pyramid_config.include('pyramid_mako')
        self.pyramid_config.add_subscriber('wuttaweb.subscribers.before_render',
                                           'pyramid.events.BeforeRender')

        # form button is disabled on @submit by default
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        html = form.render_vue_template()
        self.assertIn('<script type="text/x-template" id="wutta-form-template">', html)
        self.assertIn('@submit', html)

        # but not if form is configured otherwise
        form = self.make_form(schema=schema, auto_disable_submit=False)
        html = form.render_vue_template()
        self.assertIn('<script type="text/x-template" id="wutta-form-template">', html)
        self.assertNotIn('@submit', html)

    def test_render_vue_field(self):
        self.pyramid_config.include('pyramid_deform')
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        dform = form.get_deform()

        # typical
        html = form.render_vue_field('foo')
        self.assertIn('<b-field :horizontal="true" label="Foo">', html)
        self.assertIn('<b-input name="foo"', html)
        # nb. no error message
        self.assertNotIn('message', html)

        # with single "static" error
        dform['foo'].error = MagicMock(msg="something is wrong")
        html = form.render_vue_field('foo')
        self.assertIn(' message="something is wrong"', html)

        # with single "dynamic" error
        dform['foo'].error = MagicMock(msg="`something is wrong`")
        html = form.render_vue_field('foo')
        self.assertIn(':message="`something is wrong`"', html)

    def test_get_field_errors(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        dform = form.get_deform()

        # no error
        errors = form.get_field_errors('foo')
        self.assertEqual(len(errors), 0)

        # simple error
        dform['foo'].error = MagicMock(msg="something is wrong")
        errors = form.get_field_errors('foo')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], "something is wrong")

    def test_get_vue_field_value(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)

        # null field value
        value = form.get_vue_field_value('foo')
        self.assertEqual(value, 'null')

        # non-default / explicit value
        # TODO: surely need a different approach to set value
        dform = form.get_deform()
        dform['foo'].cstruct = 'blarg'
        value = form.get_vue_field_value('foo')
        self.assertEqual(value, '"blarg"')

    def test_jsonify_value(self):
        form = self.make_form()

        # null field value
        value = form.jsonify_value(colander.null)
        self.assertEqual(value, 'null')
        value = form.jsonify_value(None)
        self.assertEqual(value, 'null')

        # string value
        value = form.jsonify_value('blarg')
        self.assertEqual(value, '"blarg"')

    def test_validate(self):
        schema = self.make_schema()
        form = self.make_form(schema=schema)
        self.assertFalse(hasattr(form, 'validated'))

        # will not validate unless request is POST
        self.request.POST = {'foo': 'blarg', 'bar': 'baz'}
        self.request.method = 'GET'
        self.assertFalse(form.validate())
        self.request.method = 'POST'
        data = form.validate()
        self.assertEqual(data, {'foo': 'blarg', 'bar': 'baz'})

        # validating a second type updates form.validated
        self.request.POST = {'foo': 'BLARG', 'bar': 'BAZ'}
        data = form.validate()
        self.assertEqual(data, {'foo': 'BLARG', 'bar': 'BAZ'})
        self.assertIs(form.validated, data)

        # bad data does not validate
        self.request.POST = {'foo': 42, 'bar': None}
        self.assertFalse(form.validate())
        dform = form.get_deform()
        self.assertEqual(len(dform.error.children), 2)
        self.assertEqual(dform['foo'].errormsg, "Pstruct is not a string")
