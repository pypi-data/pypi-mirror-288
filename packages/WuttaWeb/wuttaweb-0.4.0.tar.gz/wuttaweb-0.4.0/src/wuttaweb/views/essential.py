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
Essential views for convenient includes

Most apps should include this module::

   pyramid_config.include('wuttaweb.views.essential')

That will in turn include the following modules:

* :mod:`wuttaweb.views.auth`
* :mod:`wuttaweb.views.common`
"""


def defaults(config, **kwargs):
    mod = lambda spec: kwargs.get(spec, spec)

    config.include(mod('wuttaweb.views.auth'))
    config.include(mod('wuttaweb.views.common'))
    config.include(mod('wuttaweb.views.settings'))


def includeme(config):
    defaults(config)
