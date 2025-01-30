import flet as ft

from frontend.api.host.models import Category


class CategoryButton:
    def __init__(self, category: Category.CategoryContent, page: ft.Page):
        self.category = category
        self.page = page

    def create(self):
        def on_hover(e):
            e.control.scale = 1.025 if e.data == "true" else 1
            e.control.update()

        if self.category.icon:
            icon = ft.Image(
                src_base64=self.category.icon,
                border_radius=15,
                width=200,
                fit=ft.ImageFit.FILL,
            )
        else:
            icon = ft.Icon(
                size=50,
                name=ft.icons.IMAGE
            )

        name = ft.Text(
            value=self.category.name,
            size=15,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        if self.category.description:
            self.category.description = f'{self.category.description[:65]}..'

        description = ft.Text(
            value=self.category.description or "Описание отсутствует",
            text_align=ft.TextAlign.CENTER,
        )

        go_button = ft.ElevatedButton(
            width=100,
            text="Перейти",
            on_click=lambda _: self.page.go(f'/categories/{self.category.id}'),
            data=f"category:{self.category.id}",
            on_hover=on_hover,
        )

        containerGoButton = ft.Container(content=go_button,
                                         expand=True,
                                         alignment=ft.alignment.bottom_center)

        divider = ft.Divider(color=ft.colors.OUTLINE)
        items_column = ft.Column(
            controls=[
                icon,
                divider,
                name,
                description,
                containerGoButton,
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
