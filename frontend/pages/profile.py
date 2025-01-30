import base64

import aiohttp
import flet as ft
from flet_route import Params, Basket
from frontend.api.host.requests import HostApi


class ProfilePage:
    def __init__(self):
        self.basket: None | Basket = None
        self.params: None | Params = None
        self.page: None | ft.Page = None
        self.dlg_modal: None | ft.AlertDialog = None

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

    def view(self, page: ft.Page, params: Params, basket: Basket):

        async def submitProfileUpdate():
            first_name = profileFirstName.value if profileFirstName.value != "" else None
            last_name = profileLastName.value if profileLastName.value != "" else None
            email = profileEmail.value if profileEmail.value != "" else None
            phone_number = profilePhoneNumber.value if profilePhoneNumber.value != "" else None

            print(type(profileIconContainer.content))

            if isinstance(profileIconContainer.content, ft.Image):
                icon = profileIconContainer.content.src_base64
            else:
                icon = None

            response = await host_api.updateClientDetails(first_name=first_name,
                                                          last_name=last_name,
                                                          email=email,
                                                          phone_number=phone_number,
                                                          icon=icon)
            if response.status_code == 200:
                return self.successMessage(successMessage=response.content.message)

            return self.errorMessage(errorMessage=response.errors[0])

        self.page = page
        self.params = params
        self.basket = basket

        page.title = 'XYZ Profile Page'

        access_token = self.page.client_storage.get(key='access_token')
        refresh_token = self.page.client_storage.get(key='refresh_token')

        if access_token is None or refresh_token is None:
            return page.go('/')

        host_api = HostApi(refresh_token=refresh_token,
                           access_token=access_token)

        profile = self.page.run_task(handler=host_api.getProfile)
        profile = profile.result()

        profileText = ft.Text(value='Профиль',
                              size=40,
                              weight=ft.FontWeight.BOLD,
                              text_align=ft.TextAlign.CENTER,
                              )

        if profile.content.icon:
            profileIcon = ft.Image(
                src_base64=profile.content.icon,
                border_radius=15,
                width=200,
                fit=ft.ImageFit.FILL,
            )
        else:
            profileIcon = ft.Icon(name=ft.icons.PERSON,
                                  size=100
                                  )

        profileIconContainer = ft.Container(content=profileIcon)

        profileDivider = ft.Divider(color=ft.colors.OUTLINE)

        profileUsername = ft.TextField(read_only=True,
                                       label='Username',
                                       border=ft.InputBorder.UNDERLINE,
                                       value=profile.content.username,
                                       tooltip="Ваш логин")

        profileLastName = ft.TextField(  # read_only=bool(profile.content.last_name),
            label='Last name',
            border=ft.InputBorder.UNDERLINE,
            value=profile.content.last_name,
            tooltip="Введите вашу фамилию")

        profileFirstName = ft.TextField(  # read_only=bool(profile.content.first_name),
            label='First Name',
            border=ft.InputBorder.UNDERLINE,
            value=profile.content.first_name,
            tooltip="Введите ваше имя")

        profileEmail = ft.TextField(  # read_only=bool(profile.content.email),
            label='Email',
            border=ft.InputBorder.UNDERLINE,
            value=profile.content.email,
            autofill_hints=[ft.AutofillHint.EMAIL],
            tooltip="Введите ваш email")

        profilePhoneNumber = ft.TextField(  # read_only=bool(profile.content.phone_number),
            label='Phone Number',
            prefix_text="+7",
            input_filter=ft.NumbersOnlyInputFilter(),
            border=ft.InputBorder.UNDERLINE,
            value=profile.content.phone_number,
            autofill_hints=[ft.AutofillHint.TELEPHONE_NUMBER],
            tooltip="Введите ваш номер телефона")

        file_url_input = ft.TextField(
            label="Введите URL картинки",
            autofocus=True,
            keyboard_type=ft.KeyboardType.URL,
        )

        async def fetch_image_base64(image_url: str) -> str | None:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=image_url) as response:
                        if response.status == 200:
                            image_bytes = await response.read()
                            base64_string = base64.b64encode(image_bytes).decode("utf-8")
                            return base64_string
                        else:
                            return None
            except Exception as e:
                return None

        def open_file_dialog(e):
            # Функция для открытия диалога
            self.dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Загрузить изображение"),
                content=file_url_input,
                actions=[
                    ft.TextButton("Отменить", on_click=self.closeAlertDialog),
                    ft.TextButton(
                        "Загрузить",
                        on_click=lambda _: update_profile_image(file_url_input.value)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = self.dlg_modal
            self.dlg_modal.open = True
            self.page.update()

        def update_profile_image(url: str | None):
            # Обновление изображения на основе URL
            if url:
                image_base64 = self.page.run_task(fetch_image_base64, url)
                image_base64 = image_base64.result()
                profileIconContainer.content = ft.Image(
                    src_base64=image_base64,
                    border_radius=15,
                    width=200,
                    fit=ft.ImageFit.FILL,
                )
                self.dlg_modal.open = False
                profileIconContainer.update()
                self.page.update()
            else:
                self.dlg_modal.open = False
                self.errorMessage("URL не должен быть пустым")

        fileButton = ft.ElevatedButton(
            'Изменить фото',
            width=300,
            icon=ft.icons.UPLOAD_FILE,
            on_click=open_file_dialog
        )

        submitButton = ft.ElevatedButton(
            "Сохранить изменения",
            width=300,
            on_click=lambda _: self.page.run_task(submitProfileUpdate)
        )

        backButton = ft.TextButton(
            "Вернуться назад",
            width=300,
            on_click=lambda _: self.page.go('/categories')
        )

        profileColumn = ft.Column(controls=[profileText,
                                            profileIconContainer,
                                            profileDivider,
                                            profileUsername,
                                            profileLastName,
                                            profileFirstName,
                                            profileEmail,
                                            profilePhoneNumber,
                                            fileButton,
                                            submitButton,
                                            backButton,
                                            ],
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        container = ft.Container(content=profileColumn,
                                 border_radius=18,
                                 padding=10,
                                 width=400,
                                 blur=ft.Blur(4, 6, ft.BlurTileMode.MIRROR),
                                 border=ft.border.all(1, ft.colors.OUTLINE),
                                 alignment=ft.alignment.center,
                                 )
        greeting = ft.Text(
            "XYZ",
            size=45,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        greetingContainer = ft.Container(
            content=ft.Column(controls=[
                ft.Container(content=greeting,
                             alignment=ft.alignment.top_center),
                ft.Divider(color=ft.colors.OUTLINE),
            ],
                spacing=15),
            width=750,
            alignment=ft.alignment.top_center
        )

        column_container = ft.Column(controls=[greetingContainer, container],
                                     #alignment=ft.MainAxisAlignment.CENTER,
                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                     scroll=ft.ScrollMode.HIDDEN
                                     )

        row_container = ft.Row(
            controls=[column_container],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        central_overlay = ft.Stack(
            controls=[
                row_container],
            expand=True
        )

        return ft.View('/profile',
                       controls=[central_overlay])
