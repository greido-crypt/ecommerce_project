import flet as ft
from flet_route import Basket, Params
from frontend.api.host.models import Product


class BasketPage:
    def __init__(self):
        self.basket: None | Basket = None
        self.params: None | Params = None
        self.page: None | ft.Page = None
        self.items_column: None | ft.Column = None
        self.total_price_text: None | ft.Text = None
        self.dlg_modal: None | ft.AlertDialog = None

    def show_alert(self, title: str, message: str, success: bool = False):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                title, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD
            ),
            content=ft.Text(message),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=ft.colors.GREEN if success else ft.colors.RED,
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.page.close(self.dlg_modal))
            ],
        )
        self.page.open(self.dlg_modal)

    def update_items_column(self):
        try:
            if not self.basket or not hasattr(self.basket, 'products') or not self.basket.products:
                self.items_column.controls = [
                    ft.Text("Корзина пуста", size=18, text_align=ft.TextAlign.CENTER)
                ]
                self.total_price_text.value = "Итоговая сумма: 0 руб."
                self.page.update()
                return

            basket_items = []
            total_price = 0

            for product in self.basket.products:
                product: Product.ProductContent
                product_name = ft.Text(
                    value=product.name, size=16, weight=ft.FontWeight.BOLD
                )

                product_description = ft.Text(
                    value=product.description or "Описание отсутствует",
                    size=12,
                    text_align=ft.TextAlign.LEFT,
                )

                remove_button = ft.ElevatedButton(
                    text="Удалить",
                    icon=ft.icons.DELETE,
                    on_click=lambda e, p=product: self.remove_from_basket(p),
                )

                basket_items.append(
                    ft.Row(
                        controls=[product_name, product_description, remove_button],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )

                total_price += product.price

            self.items_column.controls = basket_items
            self.total_price_text.value = f"Итоговая сумма: {total_price:.2f} руб."
            self.page.update()
        except AttributeError as e:
            self.show_alert("Ошибка", "Произошла ошибка при загрузке корзины. Попробуйте позже.")

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        self.basket = basket
        self.params = params

        page.title = "Корзина"

        self.items_column = ft.Column(
            alignment=ft.alignment.top_center, spacing=15
        )

        self.total_price_text = ft.Text(
            value="Итоговая сумма: 0 руб.", size=18, weight=ft.FontWeight.BOLD
        )

        def create_top_container():
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Корзина", size=30, weight=ft.FontWeight.BOLD),
                        ft.Divider(color=ft.colors.OUTLINE),
                        self.items_column,
                        self.total_price_text,
                        ft.ElevatedButton(
                            text="Купить",
                            icon=ft.icons.SHOPPING_CART,
                            on_click=self.purchase_items,
                            width=200,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=800,
                alignment=ft.alignment.top_center,
            )

        row_container = ft.Row(
            controls=[create_top_container()],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        central_overlay = ft.Stack(
            controls=[row_container],
            expand=True,
        )

        self.update_items_column()

        return ft.View(
            "/basket",
            controls=[central_overlay],
        )

    def remove_from_basket(self, product):
        if self.basket:
            try:
                self.basket.products.remove(product)
                self.show_alert(
                    "Успех",
                    f"Продукт '{product.name}' удален из корзины",
                    success=True,
                )
                self.update_items_column()
            except ValueError:
                self.show_alert(
                    "Ошибка",
                    f"Продукт '{product.name}' не найден в корзине.",
                )

    def purchase_items(self, e):
        if self.basket and hasattr(self.basket, 'products') and self.basket.products:
            self.show_alert("Успех", "Покупка успешно завершена!", success=True)
            self.basket.products.clear()
            self.update_items_column()
        else:
            self.show_alert("Ошибка", "Корзина пуста, ничего не куплено.")
