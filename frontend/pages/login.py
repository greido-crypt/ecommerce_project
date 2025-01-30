from math import pi

import flet as ft
from flet_route import Params, Basket

from frontend.api.host.requests import HostApi
from frontend.utils.animated_box import AnimatedBox
from frontend.utils.circles import circles


class LoginPage:

    def __init__(self):
        self.basket: None | Basket = None
        self.params: None | Params = None
        self.page: None | ft.Page = None
        self.dlg_modal: None | ft.AlertDialog = None

        self.greeting = ft.Text(
            "XYZ",
            size=30,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.auth_greeting = ft.Text(
            "Авторизация",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.login_input = ft.TextField(
            label="Логин",
            width=300,
            text_align=ft.TextAlign.LEFT,
            autofocus=True,
            border_radius=15,
        )

        self.password_input = ft.TextField(
            label="Пароль",
            width=300,
            password=True,
            can_reveal_password=True,
            border_radius=15,
        )

        self.login_button = ft.ElevatedButton(
            "Авторизоваться",
            width=300,
            on_click=lambda _: self.page.run_task(self.loginPress, _)
        )

        self.register_button = ft.TextButton(
            "Зарегистрироваться",
            width=300,
            on_click=lambda _: self.page.go('/signup')
        )

    def closeAlertDialog(self, e):
        self.page.close(self.dlg_modal)

    def errorMessage(self, errorMessage: str):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error",
                          text_align=ft.alignment.center),
            content=ft.Text(errorMessage),
            actions_alignment=ft.alignment.center,
            bgcolor=ft.colors.RED,
            actions=[ft.TextButton("Ok", on_click=self.closeAlertDialog)],
        )
        self.page.open(self.dlg_modal)

    def successMessage(self, successMessage: str):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Success",
                          text_align=ft.alignment.center),
            content=ft.Text(successMessage),
            actions_alignment=ft.alignment.center,
            bgcolor=ft.colors.GREEN,
            actions=[ft.TextButton("Ok", on_click=self.closeAlertDialog)],
        )
        self.page.open(self.dlg_modal)

    async def loginPress(self, e: ft.ControlEvent):
        if self.login_input.value == "":
            self.login_input.focus()
            return self.errorMessage('Write login')

        if self.password_input.value == "":
            self.password_input.focus()
            return self.errorMessage('Write password')

        host_api = HostApi()
        response = await host_api.login(username=self.login_input.value,
                                        password=self.password_input.value)

        if response.content:
            await self.page.client_storage.set_async(key='access_token', value=response.content.access_token)
            await self.page.client_storage.set_async(key='refresh_token', value=response.content.refresh_token)
            self.successMessage('Successfully logged in')
            return self.page.go('/categories')

        return self.errorMessage(errorMessage=response.errors[0])

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.page = page
        self.params = params
        self.basket = basket

        self.page.title = 'XYZ Login Page'

        purpleBox = AnimatedBox(width=48,
                                height=48,
                                border=ft.border.all(2.5, color=ft.colors.PURPLE),
                                clock_wize_rotate=pi / 4,
                                rotate=ft.transform.Rotate(
                                    angle=0.0,
                                    alignment=ft.alignment.center),
                                animate_rotation=ft.animation.Animation(700, ft.animation.AnimationCurve.EASE_IN_OUT))

        blueBox = AnimatedBox(width=48,
                              height=48,
                              border=ft.border.all(2.5, color=ft.colors.BLUE),
                              clock_wize_rotate=pi / 4,
                              rotate=ft.transform.Rotate(
                                  angle=pi / 4,
                                  alignment=ft.alignment.center
                              ),
                              blur=ft.Blur(4, 6, ft.BlurTileMode.MIRROR),
                              animate_rotation=ft.animation.Animation(700, ft.animation.AnimationCurve.EASE_IN_OUT))

        animatedBox = ft.Stack(controls=[purpleBox,
                                         blueBox])

        inputContainer = ft.Container(
            border_radius=18,
            padding=10,
            width=400,
            blur=ft.Blur(4, 6, ft.BlurTileMode.MIRROR),
            border=ft.border.all(1, ft.colors.OUTLINE),
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    self.greeting,
                    animatedBox,
                    self.auth_greeting,
                    self.login_input,
                    self.password_input,
                    self.login_button,
                    self.register_button,
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        column_container = ft.Column(controls=[inputContainer],
                                     alignment=ft.MainAxisAlignment.CENTER,
                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        row_container = ft.Row(
            controls=[column_container],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        central_overlay = ft.Stack(
            controls=[*circles(page=self.page),
                      row_container],
            expand=True
        )

        return ft.View(
            '/',
            controls=[central_overlay],
        )
