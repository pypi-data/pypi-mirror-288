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
Base Logic for Master Views
"""

from pyramid.renderers import render_to_response

from wuttaweb.views import View


class MasterView(View):
    """
    Base class for "master" views.

    Master views typically map to a table in a DB, though not always.
    They essentially are a set of CRUD views for a certain type of
    data record.

    Many attributes may be overridden in subclass.  For instance to
    define :attr:`model_class`::

       from wuttaweb.views import MasterView
       from wuttjamaican.db.model import Person

       class MyPersonView(MasterView):
           model_class = Person

       def includeme(config):
           MyPersonView.defaults(config)

    .. note::

       Many of these attributes will only exist if they have been
       explicitly defined in a subclass.  There are corresponding
       ``get_xxx()`` methods which should be used instead of accessing
       these attributes directly.

    .. attribute:: model_class

       Optional reference to a data model class.  While not strictly
       required, most views will set this to a SQLAlchemy mapped
       class,
       e.g. :class:`wuttjamaican:wuttjamaican.db.model.auth.User`.

       Code should not access this directly but instead call
       :meth:`get_model_class()`.

    .. attribute:: model_name

       Optional override for the view's data model name,
       e.g. ``'WuttaWidget'``.

       Code should not access this directly but instead call
       :meth:`get_model_name()`.

    .. attribute:: model_name_normalized

       Optional override for the view's "normalized" data model name,
       e.g. ``'wutta_widget'``.

       Code should not access this directly but instead call
       :meth:`get_model_name_normalized()`.

    .. attribute:: model_title

       Optional override for the view's "humanized" (singular) model
       title, e.g. ``"Wutta Widget"``.

       Code should not access this directly but instead call
       :meth:`get_model_title()`.

    .. attribute:: model_title_plural

       Optional override for the view's "humanized" (plural) model
       title, e.g. ``"Wutta Widgets"``.

       Code should not access this directly but instead call
       :meth:`get_model_title_plural()`.

    .. attribute:: route_prefix

       Optional override for the view's route prefix,
       e.g. ``'wutta_widgets'``.

       Code should not access this directly but instead call
       :meth:`get_route_prefix()`.

    .. attribute:: url_prefix

       Optional override for the view's URL prefix,
       e.g. ``'/widgets'``.

       Code should not access this directly but instead call
       :meth:`get_url_prefix()`.

    .. attribute:: template_prefix

       Optional override for the view's template prefix,
       e.g. ``'/widgets'``.

       Code should not access this directly but instead call
       :meth:`get_template_prefix()`.

    .. attribute:: listable

       Boolean indicating whether the view model supports "listing" -
       i.e. it should have an :meth:`index()` view.
    """

    ##############################
    # attributes
    ##############################

    listable = True

    ##############################
    # view methods
    ##############################

    def index(self):
        """
        View to "list" (filter/browse) the model data.

        This is the "default" view for the model and is what user sees
        when visiting the "root" path under the :attr:`url_prefix`,
        e.g. ``/widgets/``.
        """
        return self.render_to_response('index', {})

    ##############################
    # support methods
    ##############################

    def get_index_title(self):
        """
        Returns the main index title for the master view.

        By default this returns the value from
        :meth:`get_model_title_plural()`.  Subclass may override as
        needed.
        """
        return self.get_model_title_plural()

    def render_to_response(self, template, context):
        """
        Locate and render an appropriate template, with the given
        context, and return a :term:`response`.

        The specified ``template`` should be only the "base name" for
        the template - e.g.  ``'index'`` or ``'edit'``.  This method
        will then try to locate a suitable template file, based on
        values from :meth:`get_template_prefix()` and
        :meth:`get_fallback_templates()`.

        In practice this *usually* means two different template paths
        will be attempted, e.g. if ``template`` is ``'edit'`` and
        :attr:`template_prefix` is ``'/widgets'``:

        * ``/widgets/edit.mako``
        * ``/master/edit.mako``

        The first template found to exist will be used for rendering.
        It then calls
        :func:`pyramid:pyramid.renderers.render_to_response()` and
        returns the result.

        :param template: Base name for the template.

        :param context: Data dict to be used as template context.

        :returns: Response object containing the rendered template.
        """
        defaults = {
            'index_title': self.get_index_title(),
        }

        # merge defaults + caller-provided context
        defaults.update(context)
        context = defaults

        # first try the template path most specific to this view
        template_prefix = self.get_template_prefix()
        mako_path = f'{template_prefix}/{template}.mako'
        try:
            return render_to_response(mako_path, context, request=self.request)
        except IOError:

            # failing that, try one or more fallback templates
            for fallback in self.get_fallback_templates(template):
                try:
                    return render_to_response(fallback, context, request=self.request)
                except IOError:
                    pass

            # if we made it all the way here, then we found no
            # templates at all, in which case re-attempt the first and
            # let that error raise on up
            return render_to_response(mako_path, context, request=self.request)

    def get_fallback_templates(self, template):
        """
        Returns a list of "fallback" template paths which may be
        attempted for rendering a view.  This is used within
        :meth:`render_to_response()` if the "first guess" template
        file was not found.

        :param template: Base name for a template (without prefix), e.g.
           ``'custom'``.

        :returns: List of full template paths to be tried, based on
           the specified template.  For instance if ``template`` is
           ``'custom'`` this will (by default) return::

              ['/master/custom.mako']
        """
        return [f'/master/{template}.mako']

    ##############################
    # class methods
    ##############################

    @classmethod
    def get_model_class(cls):
        """
        Returns the model class for the view (if defined).

        A model class will *usually* be a SQLAlchemy mapped class,
        e.g. :class:`wuttjamaican:wuttjamaican.db.model.base.Person`.

        There is no default value here, but a subclass may override by
        assigning :attr:`model_class`.

        Note that the model class is not *required* - however if you
        do not set the :attr:`model_class`, then you *must* set the
        :attr:`model_name`.
        """
        if hasattr(cls, 'model_class'):
            return cls.model_class

    @classmethod
    def get_model_name(cls):
        """
        Returns the model name for the view.

        A model name should generally be in the format of a Python
        class name, e.g. ``'WuttaWidget'``.  (Note this is
        *singular*, not plural.)

        The default logic will call :meth:`get_model_class()` and
        return that class name as-is.  A subclass may override by
        assigning :attr:`model_name`.
        """
        if hasattr(cls, 'model_name'):
            return cls.model_name

        return cls.get_model_class().__name__

    @classmethod
    def get_model_name_normalized(cls):
        """
        Returns the "normalized" model name for the view.

        A normalized model name should generally be in the format of a
        Python variable name, e.g. ``'wutta_widget'``.  (Note this is
        *singular*, not plural.)

        The default logic will call :meth:`get_model_name()` and
        simply lower-case the result.  A subclass may override by
        assigning :attr:`model_name_normalized`.
        """
        if hasattr(cls, 'model_name_normalized'):
            return cls.model_name_normalized

        return cls.get_model_name().lower()

    @classmethod
    def get_model_title(cls):
        """
        Returns the "humanized" (singular) model title for the view.

        The model title will be displayed to the user, so should have
        proper grammar and capitalization, e.g. ``"Wutta Widget"``.
        (Note this is *singular*, not plural.)

        The default logic will call :meth:`get_model_name()` and use
        the result as-is.  A subclass may override by assigning
        :attr:`model_title`.
        """
        if hasattr(cls, 'model_title'):
            return cls.model_title

        return cls.get_model_name()

    @classmethod
    def get_model_title_plural(cls):
        """
        Returns the "humanized" (plural) model title for the view.

        The model title will be displayed to the user, so should have
        proper grammar and capitalization, e.g. ``"Wutta Widgets"``.
        (Note this is *plural*, not singular.)

        The default logic will call :meth:`get_model_title()` and
        simply add a ``'s'`` to the end.  A subclass may override by
        assigning :attr:`model_title_plural`.
        """
        if hasattr(cls, 'model_title_plural'):
            return cls.model_title_plural

        model_title = cls.get_model_title()
        return f"{model_title}s"

    @classmethod
    def get_route_prefix(cls):
        """
        Returns the "route prefix" for the master view.  This prefix
        is used for all named routes defined by the view class.

        For instance if route prefix is ``'widgets'`` then a view
        might have these routes:

        * ``'widgets'``
        * ``'widgets.create'``
        * ``'widgets.edit'``
        * ``'widgets.delete'``

        The default logic will call
        :meth:`get_model_name_normalized()` and simply add an ``'s'``
        to the end, making it plural.  A subclass may override by
        assigning :attr:`route_prefix`.
        """
        if hasattr(cls, 'route_prefix'):
            return cls.route_prefix

        model_name = cls.get_model_name_normalized()
        return f'{model_name}s'

    @classmethod
    def get_url_prefix(cls):
        """
        Returns the "URL prefix" for the master view.  This prefix is
        used for all URLs defined by the view class.

        Using the same example as in :meth:`get_route_prefix()`, the
        URL prefix would be ``'/widgets'`` and the view would have
        defined routes for these URLs:

        * ``/widgets/``
        * ``/widgets/new``
        * ``/widgets/XXX/edit``
        * ``/widgets/XXX/delete``

        The default logic will call :meth:`get_route_prefix()` and
        simply add a ``'/'`` to the beginning.  A subclass may
        override by assigning :attr:`url_prefix`.
        """
        if hasattr(cls, 'url_prefix'):
            return cls.url_prefix

        route_prefix = cls.get_route_prefix()
        return f'/{route_prefix}'

    @classmethod
    def get_template_prefix(cls):
        """
        Returns the "template prefix" for the master view.  This
        prefix is used to guess which template path to render for a
        given view.

        Using the same example as in :meth:`get_url_prefix()`, the
        template prefix would also be ``'/widgets'`` and the templates
        assumed for those routes would be:

        * ``/widgets/index.mako``
        * ``/widgets/create.mako``
        * ``/widgets/edit.mako``
        * ``/widgets/delete.mako``

        The default logic will call :meth:`get_url_prefix()` and
        return that value as-is.  A subclass may override by assigning
        :attr:`template_prefix`.
        """
        if hasattr(cls, 'template_prefix'):
            return cls.template_prefix

        return cls.get_url_prefix()

    ##############################
    # configuration
    ##############################

    @classmethod
    def defaults(cls, config):
        """
        Provide default Pyramid configuration for a master view.

        This is generally called from within the module's
        ``includeme()`` function, e.g.::

           from wuttaweb.views import MasterView

           class WidgetView(MasterView):
               model_name = 'Widget'

           def includeme(config):
               WidgetView.defaults(config)

        :param config: Reference to the app's
           :class:`pyramid:pyramid.config.Configurator` instance.
        """
        cls._defaults(config)

    @classmethod
    def _defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()

        # index view
        if cls.listable:
            config.add_route(route_prefix, f'{url_prefix}/')
            config.add_view(cls, attr='index',
                            route_name=route_prefix)
