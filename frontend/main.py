import flet as ft

from .router import Router


async def main(page: ft.Page):
    page.title = "XYZ"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    Router(page)


if __name__ == "__main__":
    ft.app(target=main,
           view=ft.AppView.WEB_BROWSER,
           assets_dir='assets',
           port=1337)
