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
Common Views
"""

from wuttaweb.views import View


class CommonView(View):
    """
    Common views shared by all apps.
    """

    def home(self):
        """
        Home page view.

        Template: ``/home.mako``

        This is normally the view shown when a user navigates to the
        root URL for the web app.

        """
        return {
            'index_title': self.app.get_title(),
        }

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)

    @classmethod
    def _defaults(cls, config):

        # auto-correct URLs which require trailing slash
        config.add_notfound_view(cls, attr='notfound', append_slash=True)

        # home page
        config.add_route('home', '/')
        config.add_view(cls, attr='home',
                        route_name='home',
                        renderer='/home.mako')


def defaults(config, **kwargs):
    base = globals()

    CommonView = kwargs.get('CommonView', base['CommonView'])
    CommonView.defaults(config)


def includeme(config):
    defaults(config)
