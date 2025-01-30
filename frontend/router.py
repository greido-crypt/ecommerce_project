import flet as ft
from flet_route import Routing, path

from .pages import LoginPage, SignUpPage, CategoriesPage, ProfilePage, CategoryPage, BasketPage
from .pages.admin import AdminPage


class Router:
    def __init__(self, page: ft.Page):
        self.__page = page
        self.__app_routes = [
            path(url='/', clear=True, view=LoginPage().view),
            path(url='/signup', clear=True, view=SignUpPage().view),
            path(url='/categories', clear=True, view=CategoriesPage().view),
            path(url='/profile', clear=True, view=ProfilePage().view),
            path(url='/categories/:category_id', clear=True, view=CategoryPage().view),
            path(url='/basket', clear=False, view=BasketPage().view),
            path(url='/admin', clear=False, view=AdminPage().view),
        ]

        Routing(
            page=self.__page,
            app_routes=self.__app_routes
        )
        self.__page.go(self.__page.route)
