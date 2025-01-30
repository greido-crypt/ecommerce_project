from typing import List

import flet as ft
from flet_route import Params, Basket

from frontend.api.host.models import Product
from frontend.api.host.requests import HostApi
from frontend.utils.product_button import ProductButton


class CategoryPage:
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

        self.search_field = ft.TextField(label='Поиск', autofocus=True, width=700)
        self.search_button = ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=self.perform_search)
        self.search_row = ft.Row(
            controls=[
                self.search_field,
                self.search_button
            ],
            alignment=ft.alignment.top_center
        )

        self.products = []  # Список всех продуктов для хранения исходных данных
        self.product_buttons = []  # Список готовых кнопок для продуктов
        self.productsColumn = None  # Колонка для отображения продуктов

    def perform_search(self, e):
        """Фильтрует продукты на основе поискового запроса."""
        query = self.search_field.value.lower()
        filtered_buttons = [
            button for button, product in zip(self.product_buttons, self.products)
            if query in product.name.lower() or query in product.description.lower()
        ]
        self.productsColumn.controls = [
            ft.Row(controls=filtered_buttons[i:i+3],
                   alignment=ft.alignment.top_center,
                   spacing=10)
            for i in range(0, len(filtered_buttons), 3)
        ]
        self.page.update()

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        self.params = params
        self.basket = basket

        category_id = int(params.get('category_id'))

        page.title = 'XYZ Category Page'

        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')

        if access_token is None or refresh_token is None:
            return page.go('/')

        host_api = HostApi(refresh_token=refresh_token,
                           access_token=access_token)

        products = self.page.run_task(host_api.getProductsByCategory, category_id)
        self.products: List[Product.ProductContent] = products.result().content.products  # Сохраняем список всех продуктов

        self.product_buttons = [
            ProductButton(product=product_data, page=self.page, basket=self.basket).create()
            for product_data in self.products if product_data.is_visible and not product_data.is_deleted
        ]

        self.productsColumn = ft.Column(
            controls=[
                ft.Row(controls=self.product_buttons[i:i+3],
                       alignment=ft.alignment.top_center,
                       spacing=10)
                for i in range(0, len(self.product_buttons), 3)
            ],
            alignment=ft.alignment.top_center
        )

        def create_top_container():
            return ft.Container(
                content=ft.Column(controls=[
                    ft.Container(content=self.greeting,
                                 alignment=ft.alignment.top_center),
                    ft.Divider(color=ft.colors.OUTLINE),
                    self.search_row,
                    self.productsColumn
                ],
                    scroll=ft.ScrollMode.HIDDEN,
                    spacing=15),
                width=800,
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
            f'/categories/{category_id}',
            controls=[central_overlay],
        )
