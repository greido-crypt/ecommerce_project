import flet as ft
from flet_route import Basket

from frontend.api.host.models import Product


class ProductButton:
    def __init__(self, product: Product.ProductContent, page: ft.Page, basket: Basket):
        self.product = product
        self.page = page
        self.basket = basket

    def create(self):
        def on_hover(e: ft.ControlEvent):
            if e.control.parent:  # Проверяем, добавлен ли элемент в дерево
                e.control.scale = 1.025 if e.data == "true" else 1
                e.control.update()

        def deleteFromBasket(e: ft.ControlEvent):
            for product in self.basket.products:
                product: Product.ProductContent
                if product.id == self.product.id:
                    self.basket.products.remove(product)
                    containerBuyButton.content = ft.ElevatedButton(
                        icon=ft.icons.SHOPPING_CART,
                        text="Купить",
                        on_click=addToBasket,
                        data=f"category:{self.product.id}",
                        on_hover=on_hover,
                    )
                    items_column.update()
                    break

        def addToBasket(e: ft.ControlEvent):
            self.basket.products = self.basket.products + [self.product]
            containerBuyButton.content = ft.ElevatedButton(
                icon=ft.icons.SHOPPING_CART,
                color=ft.colors.YELLOW,
                icon_color=ft.colors.YELLOW,
                bgcolor=ft.colors.GREEN,
                text="Добавлено",
                on_click=deleteFromBasket,
                on_hover=on_hover,
            )
            items_column.update()

        if self.product.icon:
            icon = ft.Image(
                src_base64=self.product.icon,
                border_radius=15,
                width=250,
                fit=ft.ImageFit.FILL,
            )
        else:
            icon = ft.Icon(
                size=200,
                name=ft.icons.IMAGE
            )

        name = ft.Text(
            value=self.product.name,
            size=15,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        if self.product.description:
            self.product.description = f'{self.product.description[:85]}..'

        description = ft.Text(
            value=self.product.description or "Описание отсутствует",
            text_align=ft.TextAlign.CENTER,
        )
        price = ft.Text(value=f'Цена: {self.product.price}')
        buy_button = ft.ElevatedButton(
            icon=ft.icons.SHOPPING_CART,
            text="Купить",
            on_click=addToBasket,
            on_hover=on_hover,
        )

        containerBuyButton = ft.Container(content=buy_button,
                                          expand=True,
                                          alignment=ft.alignment.bottom_center)

        divider = ft.Divider(color=ft.colors.OUTLINE)
        items_column = ft.Column(
            controls=[
                icon,
                divider,
                name,
                description,
                price,
                containerBuyButton,
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

        return ft.Container(
            content=items_column,
            width=230,
            height=400,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=15,
            padding=10,
            border=ft.border.all(color=ft.colors.OUTLINE, width=1),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
            on_hover=on_hover,
        )
