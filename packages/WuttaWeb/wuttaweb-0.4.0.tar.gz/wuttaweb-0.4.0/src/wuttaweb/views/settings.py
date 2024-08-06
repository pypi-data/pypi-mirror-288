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
Views for app settings
"""

from wuttaweb.views import MasterView


class AppInfoView(MasterView):
    """
    Master view for the overall app, to show/edit config etc.
    """
    model_name = 'AppInfo'
    model_title_plural = "App Info"
    route_prefix = 'appinfo'


def defaults(config, **kwargs):
    base = globals()

    AppInfoView = kwargs.get('AppInfoView', base['AppInfoView'])
    AppInfoView.defaults(config)


def includeme(config):
    defaults(config)
