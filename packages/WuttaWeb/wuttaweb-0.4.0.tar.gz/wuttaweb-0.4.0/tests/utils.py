# -*- coding: utf-8; -*-

from wuttaweb.menus import MenuHandler


class NullMenuHandler(MenuHandler):
    """
    Dummy menu handler for testing.
    """
    def make_menus(self, request, **kwargs):
        return []
