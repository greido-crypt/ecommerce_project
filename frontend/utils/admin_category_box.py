import flet as ft

from frontend.api.host.models import CategoryContent


class CategoryButton:
    def __init__(self, category: CategoryContent, page: ft.Page):
        self.category = category
        self.page = page

    def create(self):
        ...