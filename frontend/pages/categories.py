import flet as ft
from flet_route import Params, Basket

from frontend.api.host.requests import HostApi
from frontend.utils.category_button import CategoryButton


class CategoriesPage:
    def __init__(self):
        self.basket: None | Basket = None
        self.params: None | Params = None
        self.page: None | ft.Page = None
        self.dlg_modal: None | ft.AlertDialog = None

        self.profile_icon = ft.IconButton(
            ft.icons.PERSON,
            icon_size=35,
            tooltip="Profile",
            on_click=lambda e: self.page.go('/profile'))

        self.basket_icon = ft.IconButton(
            ft.icons.SHOPPING_CART,
            icon_size=35,
            tooltip="Basket",
            on_click=lambda e: self.page.go('/basket'))

        self.greeting = ft.Text(
            "XYZ",
            size=45,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.search_row = ft.Row(
            controls=[
                ft.TextField(label='Поиск', autofocus=True, width=700),
                ft.FloatingActionButton(icon=ft.icons.SEARCH)
            ],
            alignment=ft.alignment.top_center
        )

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        self.params = params
        self.basket = basket
        self.basket.products = []

        page.title = 'XYZ Categories Page'

        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')

        if access_token is None or refresh_token is None:
            return page.go('/')

        host_api = HostApi(refresh_token=refresh_token,
                           access_token=access_token)

        categories = self.page.run_task(handler=host_api.getAllCategories)
        categories = categories.result()
        categoryList = []
        for category in categories.content.categories:
            if not category.is_deleted or not category.is_visible:
                continue
            ctgButton = CategoryButton(category=category, page=page).create()
            categoryList.append(ctgButton)

        categoryRow = ft.Row(controls=categoryList,
                             alignment=ft.alignment.top_center,
                             spacing=10)

        def create_top_container():
            return ft.Container(
                content=ft.Column(controls=[
                    ft.Container(content=self.greeting,
                                 alignment=ft.alignment.top_center),
                    ft.Divider(color=ft.colors.OUTLINE),
                    # self.search_row,
                    categoryRow
                ],
                    spacing=15),
                width=750,
                alignment=ft.alignment.top_center
            )

        row_container = ft.Row(
            controls=[create_top_container()],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        top_icons = ft.Row(
            controls=[self.profile_icon, self.basket_icon],
            alignment=ft.MainAxisAlignment.END,
            spacing=10,
        )

        central_overlay = ft.Stack(
            controls=[row_container, top_icons],
            expand=True
        )

        return ft.View(
            '/categories',
            controls=[central_overlay],
        )
