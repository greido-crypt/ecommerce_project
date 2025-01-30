import flet as ft
from flet_route import Params, Basket

from frontend.api.host.models import Category, Product
from frontend.api.host.requests import HostApi


class AdminPage:
    def __init__(self):
        self.basket: None | Basket = None
        self.params: None | Params = None
        self.page: None | ft.Page = None
        self.dlg_modal: None | ft.AlertDialog = None
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self.host_api: HostApi | None = None

    def show_message(self, title: str, message: str, success: bool = False):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, weight=ft.FontWeight.BOLD),
            content=ft.Text(message),
            bgcolor=ft.colors.GREEN if success else ft.colors.RED,
            actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(self.dlg_modal))],
        )
        self.page.open(self.dlg_modal)

    def edit_category(self, category: Category.CategoryContent):
        def submit_edit(e):
            updated_name = name_field.value
            updated_description = description_field.value
            self.page.run_task(self.host_api.updateCategory, category.id, updated_name, updated_description, category.icon)

            self.show_message("Сохранено", f"Категория {updated_name} обновлена", success=True)
            self.page.close(dialog)

        name_field = ft.TextField(label="Название", value=category.name)
        description_field = ft.TextField(label="Описание", value=category.description)

        dialog = ft.AlertDialog(
            title=ft.Text("Редактировать категорию"),
            content=ft.Column([name_field, description_field]),
            actions=[
                ft.TextButton("Сохранить", on_click=submit_edit),
                ft.TextButton("Отмена", on_click=lambda e: self.page.close(dialog))
            ]
        )
        self.page.open(dialog)

    def edit_product(self, product: Product.ProductContent):
        def submit_edit(e: ft.ControlEvent):
            updated_name = name_field.value
            updated_price = price_field.value
            updated_description = description_field.value
            self.page.run_task(self.host_api.updateProduct, None, product.id, float(updated_price), updated_name, updated_description, product.icon)
            self.show_message("Сохранено", f"Товар {updated_name} обновлён", success=True)
            self.page.close(dialog)

        name_field = ft.TextField(label="Название", value=product.name)
        price_field = ft.TextField(label="Цена", value=str(product.price))
        description_field = ft.TextField(label="Описание", value=product.description)

        dialog = ft.AlertDialog(
            title=ft.Text("Редактировать товар"),
            content=ft.Column([name_field, price_field, description_field]),
            actions=[
                ft.TextButton("Сохранить", on_click=submit_edit),
                ft.TextButton("Отмена", on_click=lambda e: self.page.close(dialog))
            ]
        )
        self.page.open(dialog)

    def edit_client(self, client):
        def submit_edit(e):
            updated_username = username_field.value
            updated_email = email_field.value
            updated_first_name = first_name_field.value
            updated_last_name = last_name_field.value
            updated_phone_number = phone_field.value
            # Call API to update client here
            self.show_message("Сохранено", f"Пользователь {updated_username} обновлён", success=True)
            self.page.close(dialog)

        username_field = ft.TextField(label="Логин", value=client.username)
        email_field = ft.TextField(label="Email", value=client.email)
        first_name_field = ft.TextField(label="Имя", value=client.first_name)
        last_name_field = ft.TextField(label="Фамилия", value=client.last_name)
        phone_field = ft.TextField(label="Телефон", value=client.phone_number)

        dialog = ft.AlertDialog(
            title=ft.Text("Редактировать пользователя"),
            content=ft.Column([username_field, email_field, first_name_field, last_name_field, phone_field]),
            actions=[
                ft.TextButton("Сохранить", on_click=submit_edit),
                ft.TextButton("Отмена", on_click=lambda e: self.page.close(dialog))
            ]
        )
        self.page.open(dialog)

    def view_categories(self):
        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')
        host_api = HostApi(access_token=access_token, refresh_token=refresh_token)
        categories = self.page.run_task(handler=host_api.getAllCategories)
        categories = categories.result().content.categories

        rows = []
        for category in categories:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(category.id)),
                    ft.DataCell(ft.Text(category.name)),
                    ft.DataCell(ft.Text(category.description[:70])),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, cat=category: self.edit_category(cat)),
                        ft.IconButton(ft.icons.VISIBILITY if category.is_visible else ft.icons.VISIBILITY_OFF,
                                      on_click=lambda e, cat=category: self.hide_category(cat)),
                        ft.IconButton(ft.icons.DELETE if category.is_deleted else ft.icons.DELETE_FOREVER, on_click=lambda e, cat=category: self.delete_category(cat))
                    ]))
                ])
            )

        table = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Название")),
            ft.DataColumn(label=ft.Text("Описание")),
            ft.DataColumn(label=ft.Text("Действия"))
        ], rows=rows)

        return ft.Column(controls=[table], expand=True, scroll=ft.ScrollMode.AUTO)

    def view_products(self):
        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')
        host_api = HostApi(access_token=access_token, refresh_token=refresh_token)
        products = self.page.run_task(handler=host_api.getAllProducts)
        products = products.result()

        rows = []
        for product in products.content.products:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(product.id)),
                    ft.DataCell(ft.Text(product.name)),
                    ft.DataCell(ft.Text(product.price)),
                    ft.DataCell(ft.Text(product.description)),
                    ft.DataCell(ft.Text(product.category_name)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, prod=product: self.edit_product(prod)),
                        ft.IconButton(ft.icons.VISIBILITY if product.is_visible else ft.icons.VISIBILITY_OFF,
                                      on_click=lambda e, prod=product: self.hide_product(prod)),
                        ft.IconButton(ft.icons.DELETE if product.is_deleted else ft.icons.DELETE_FOREVER, on_click=lambda e, prod=product: self.delete_product(prod))
                    ]))
                ])
            )

        table = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Название")),
            ft.DataColumn(label=ft.Text("Цена")),
            ft.DataColumn(label=ft.Text("Описание")),
            ft.DataColumn(label=ft.Text("Название категории")),
            ft.DataColumn(label=ft.Text("Действия"))
        ], rows=rows)

        return ft.Column(controls=[table], expand=True, scroll=ft.ScrollMode.AUTO)

    def view_clients(self):
        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')
        host_api = HostApi(access_token=access_token, refresh_token=refresh_token)
        clients = self.page.run_task(handler=host_api.getAllClients)
        clients = clients.result()

        rows = []
        for client in clients.content:
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(client.id)),
                    ft.DataCell(ft.Text(client.username)),
                    ft.DataCell(ft.Text(client.email)),
                    ft.DataCell(ft.Text(client.first_name)),
                    ft.DataCell(ft.Text(client.last_name)),
                    ft.DataCell(ft.Text(client.phone_number)),
                    ft.DataCell(ft.Text(client.role)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, usr=client: self.edit_client(usr)),
                        ft.IconButton(ft.icons.BLOCK, on_click=lambda e, usr=client: self.ban_client(usr)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, usr=client: self.delete_client(usr))
                    ]))
                ])
            )

        table = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text("ID")),
            ft.DataColumn(label=ft.Text("Username")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("First name")),
            ft.DataColumn(label=ft.Text("Last name")),
            ft.DataColumn(label=ft.Text("Phone number")),
            ft.DataColumn(label=ft.Text("Role")),
            ft.DataColumn(label=ft.Text("Действия"))
        ], rows=rows)

        return ft.Column(controls=[table], expand=True, scroll=ft.ScrollMode.AUTO)

    def hide_category(self, category: Category.CategoryContent):
        task = self.page.run_task(self.host_api.hideCategory, category.id)
        task.result()
        self.show_message("Скрытие", f"Категория {category.name} скрыта")

    def delete_category(self, category: Category.CategoryContent):
        task = self.page.run_task(self.host_api.deleteCategory, category.id)
        task.result()
        self.show_message("Удаление", f"Категория {category.name} удалена")

    def hide_product(self, product: Product.ProductContent):
        task = self.page.run_task(self.host_api.hideProduct, product.id)
        task.result()
        self.show_message("Скрытие", f"Товар {product.name} скрыт")

    def delete_product(self, product: Product.ProductContent):
        task = self.page.run_task(self.host_api.deleteProduct, product.id)
        task.result()
        self.show_message("Удаление", f"Товар {product.name} удалён")

    def ban_client(self, client):
        self.show_message("Блокировка", f"Пользователь {client.username} заблокирован")

    def delete_client(self, client):
        self.show_message("Удаление", f"Пользователь {client.username} удалён")

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        self.params = params
        self.basket = basket

        page.title = 'XYZ Admin Page'

        self.access_token = self.page.client_storage.get(key='access_token')
        self.refresh_token = self.page.client_storage.get(key='refresh_token')
        self.host_api = HostApi(access_token=self.access_token, refresh_token=self.refresh_token)

        if self.access_token is None or self.refresh_token is None:
            return page.go('/')

        nav_bar = ft.NavigationRail(
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.CATEGORY, label="Категории"),
                ft.NavigationRailDestination(icon=ft.icons.SHOPPING_BAG, label="Товары"),
                ft.NavigationRailDestination(icon=ft.icons.PERSON, label="Клиенты")
            ],
            selected_index=0,
            on_change=self.update_view
        )

        self.content = ft.Column()
        self.update_view(ft.ControlEvent(target="nav_bar", name="change", control=nav_bar, page=self.page, data="0"))

        return ft.View(
            '/admin',
            controls=[ft.Row(controls=[nav_bar, self.content], expand=True)]
        )

    def update_view(self, e: ft.ControlEvent):
        views = [self.view_categories, self.view_products, self.view_clients]
        self.content.controls = [views[int(e.data)]()]
        self.page.update()
