# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Base form classes
"""

import json
import logging

import colander
import deform
from pyramid.renderers import render
from webhelpers2.html import HTML

from wuttaweb.util import get_form_data


log = logging.getLogger(__name__)


class FieldList(list):
    """
    Convenience wrapper for a form's field list.  This is a subclass
    of :class:`python:list`.

    You normally would not need to instantiate this yourself, but it
    is used under the hood for e.g. :attr:`Form.fields`.
    """

    def insert_before(self, field, newfield):
        """
        Insert a new field, before an existing field.

        :param field: String name for the existing field.

        :param newfield: String name for the new field, to be inserted
           just before the existing ``field``.
        """
        if field in self:
            i = self.index(field)
            self.insert(i, newfield)
        else:
            log.warning("field '%s' not found, will append new field: %s",
                        field, newfield)
            self.append(newfield)

    def insert_after(self, field, newfield):
        """
        Insert a new field, after an existing field.

        :param field: String name for the existing field.

        :param newfield: String name for the new field, to be inserted
           just after the existing ``field``.
        """
        if field in self:
            i = self.index(field)
            self.insert(i + 1, newfield)
        else:
            log.warning("field '%s' not found, will append new field: %s",
                        field, newfield)
            self.append(newfield)


class Form:
    """
    Base class for all forms.

    :param request: Reference to current :term:`request` object.

    :param fields: List of field names for the form.  This is
       optional; if not specified an attempt will be made to deduce
       the list automatically.  See also :attr:`fields`.

    :param schema: Colander-based schema object for the form.  This is
       optional; if not specified an attempt will be made to construct
       one automatically.  See also :meth:`get_schema()`.

    :param labels: Optional dict of default field labels.

    .. note::

       Some parameters are not explicitly described above.  However
       their corresponding attributes are described below.

    Form instances contain the following attributes:

    .. attribute:: fields

       :class:`FieldList` instance containing string field names for
       the form.  By default, fields will appear in the same order as
       they are in this list.

    .. attribute:: request

       Reference to current :term:`request` object.

    .. attribute:: action_url

       String URL to which the form should be submitted, if applicable.

    .. attribute:: vue_tagname

       String name for Vue component tag.  By default this is
       ``'wutta-form'``.  See also :meth:`render_vue_tag()`.

    .. attribute:: align_buttons_right

       Flag indicating whether the buttons (submit, cancel etc.)
       should be aligned to the right of the area below the form.  If
       not set, the buttons are left-aligned.

    .. attribute:: auto_disable_submit

       Flag indicating whether the submit button should be
       auto-disabled, whenever the form is submitted.

    .. attribute:: button_label_submit

       String label for the form submit button.  Default is ``"Save"``.

    .. attribute:: button_icon_submit

       String icon name for the form submit button.  Default is ``'save'``.

    .. attribute:: show_button_reset

       Flag indicating whether a Reset button should be shown.

    .. attribute:: validated

       If the :meth:`validate()` method was called, and it succeeded,
       this will be set to the validated data dict.

       Note that in all other cases, this attribute may not exist.
    """

    def __init__(
            self,
            request,
            fields=None,
            schema=None,
            labels={},
            action_url=None,
            vue_tagname='wutta-form',
            align_buttons_right=False,
            auto_disable_submit=True,
            button_label_submit="Save",
            button_icon_submit='save',
            show_button_reset=False,
    ):
        self.request = request
        self.schema = schema
        self.labels = labels or {}
        self.action_url = action_url
        self.vue_tagname = vue_tagname
        self.align_buttons_right = align_buttons_right
        self.auto_disable_submit = auto_disable_submit
        self.button_label_submit = button_label_submit
        self.button_icon_submit = button_icon_submit
        self.show_button_reset = show_button_reset

        self.config = self.request.wutta_config
        self.app = self.config.get_app()

        if fields is not None:
            self.set_fields(fields)
        elif self.schema:
            self.set_fields([f.name for f in self.schema])
        else:
            self.fields = None

    def __contains__(self, name):
        """
        Custom logic for the ``in`` operator, to allow easily checking
        if the form contains a given field::

           myform = Form()
           if 'somefield' in myform:
               print("my form has some field")
        """
        return bool(self.fields and name in self.fields)

    def __iter__(self):
        """
        Custom logic to allow iterating over form field names::

           myform = Form(fields=['foo', 'bar'])
           for fieldname in myform:
               print(fieldname)
        """
        return iter(self.fields)

    @property
    def vue_component(self):
        """
        String name for the Vue component, e.g. ``'WuttaForm'``.

        This is a generated value based on :attr:`vue_tagname`.
        """
        words = self.vue_tagname.split('-')
        return ''.join([word.capitalize() for word in words])

    def set_fields(self, fields):
        """
        Explicitly set the list of form fields.

        This will overwrite :attr:`fields` with a new
        :class:`FieldList` instance.

        :param fields: List of string field names.
        """
        self.fields = FieldList(fields)

    def set_label(self, key, label):
        """
        Set the label for given field name.

        See also :meth:`get_label()`.
        """
        self.labels[key] = label

        # update schema if necessary
        if self.schema and key in self.schema:
            self.schema[key].title = label

    def get_label(self, key):
        """
        Get the label for given field name.

        Note that this will always return a string, auto-generating
        the label if needed.

        See also :meth:`set_label()`.
        """
        return self.labels.get(key, self.app.make_title(key))

    def get_schema(self):
        """
        Return the :class:`colander:colander.Schema` object for the
        form, generating it automatically if necessary.
        """
        if not self.schema:
            raise NotImplementedError

        return self.schema

    def get_deform(self):
        """
        Return the :class:`deform:deform.Form` instance for the form,
        generating it automatically if necessary.
        """
        if not hasattr(self, 'deform_form'):
            schema = self.get_schema()
            form = deform.Form(schema)
            self.deform_form = form

        return self.deform_form

    def render_vue_tag(self, **kwargs):
        """
        Render the Vue component tag for the form.

        By default this simply returns:

        .. code-block:: html

           <wutta-form></wutta-form>

        The actual output will depend on various form attributes, in
        particular :attr:`vue_tagname`.
        """
        return HTML.tag(self.vue_tagname, **kwargs)

    def render_vue_template(
            self,
            template='/forms/vue_template.mako',
            **context):
        """
        Render the Vue template block for the form.

        This returns something like:

        .. code-block:: none

           <script type="text/x-template" id="wutta-form-template">
             <form>
               <!-- fields etc. -->
             </form>
           </script>

        .. todo::

           Why can't Sphinx render the above code block as 'html' ?

           It acts like it can't handle a ``<script>`` tag at all?

        Actual output will of course depend on form attributes, i.e.
        :attr:`vue_tagname` and :attr:`fields` list etc.

        :param template: Path to Mako template which is used to render
           the output.
        """
        context['form'] = self
        context.setdefault('form_attrs', {})

        # auto disable button on submit
        if self.auto_disable_submit:
            context['form_attrs']['@submit'] = 'formSubmitting = true'

        output = render(template, context)
        return HTML.literal(output)

    def render_vue_field(self, fieldname):
        """
        Render the given field completely, i.e. ``<b-field>`` wrapper
        with label and containing a widget.

        Actual output will depend on the field attributes etc.
        Typical output might look like:

        .. code-block:: html

           <b-field label="Foo"
                    horizontal
                    type="is-danger"
                    message="something went wrong!">
              <!-- widget element(s) -->
           </b-field>
        """
        dform = self.get_deform()
        field = dform[fieldname]

        # render the field widget or whatever
        html = field.serialize()
        html = HTML.literal(html)

        # render field label
        label = self.get_label(fieldname)

        # b-field attrs
        attrs = {
            ':horizontal': 'true',
            'label': label,
        }

        # next we will build array of messages to display..some
        # fields always show a "helptext" msg, and some may have
        # validation errors..
        field_type = None
        messages = []

        # show errors if present
        errors = self.get_field_errors(fieldname)
        if errors:
            field_type = 'is-danger'
            messages.extend(errors)

        # ..okay now we can declare the field messages and type
        if field_type:
            attrs['type'] = field_type
        if messages:
            if len(messages) == 1:
                msg = messages[0]
                if msg.startswith('`') and msg.endswith('`'):
                    attrs[':message'] = msg
                else:
                    attrs['message'] = msg
            # TODO
            # else:
            #     # nb. must pass an array as JSON string
            #     attrs[':message'] = '[{}]'.format(', '.join([
            #         "'{}'".format(msg.replace("'", r"\'"))
            #         for msg in messages]))

        return HTML.tag('b-field', c=[html], **attrs)

    def get_field_errors(self, field):
        """
        Return a list of error messages for the given field.

        Not useful unless a call to :meth:`validate()` failed.
        """
        dform = self.get_deform()
        if field in dform:
            error = dform[field].errormsg
            if error:
                return [error]
        return []

    def get_vue_field_value(self, field):
        """
        This method returns a JSON string which will be assigned as
        the initial model value for the given field.  This JSON will
        be written as part of the overall response, to be interpreted
        on the client side.

        Again, this must return a *string* such as:

        * ``'null'``
        * ``'{"foo": "bar"}'``

        In practice this calls :meth:`jsonify_value()` to convert the
        ``field.cstruct`` value to string.
        """
        if isinstance(field, str):
            dform = self.get_deform()
            field = dform[field]

        return self.jsonify_value(field.cstruct)

    def jsonify_value(self, value):
        """
        Convert a Python value to JSON string.

        See also :meth:`get_vue_field_value()`.
        """
        if value is colander.null:
            return 'null'

        return json.dumps(value)

    def validate(self):
        """
        Try to validate the form.

        This should work whether request data was submitted as classic
        POST data, or as JSON body.

        If the form data is valid, this method returns the data dict.
        This data dict is also then available on the form object via
        the :attr:`validated` attribute.

        However if the data is not valid, ``False`` is returned, and
        there will be no :attr:`validated` attribute.  In that case
        you should inspect the form errors to learn/display what went
        wrong for the user's sake.  See also
        :meth:`get_field_errors()`.

        :returns: Data dict, or ``False``.
        """
        if hasattr(self, 'validated'):
            del self.validated

        if self.request.method != 'POST':
            return False

        dform = self.get_deform()
        controls = get_form_data(self.request).items()

        try:
            self.validated = dform.validate(controls)
        except deform.ValidationFailure:
            return False

        return self.validated
