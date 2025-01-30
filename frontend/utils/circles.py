import flet as ft


def circles(page: ft.Page):
    # print(page.width, " ", page.height)
    return [
        ft.Container(
            width=page.width * 0.25, height=page.width * 0.25,
            border_radius=360,  # Круглый край
            gradient=ft.LinearGradient(
                colors=['#c233e6', '#122fd3'],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            alignment=ft.alignment.center,
            top=page.width * 0.04,  # Позиция по вертикали
            left=page.width * 0.04,  # Позиция по горизонтали
            shadow=ft.BoxShadow(blur_radius=10)
        ),
        ft.Container(
            width=page.width * 0.25, height=page.width * 0.25,
            border_radius=360,  # Круглый край
            gradient=ft.LinearGradient(
                colors=['#ff7f50', '#ff1493'],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            alignment=ft.alignment.center,
            top=page.width * 0.15,
            right=page.width * 0.15,
            shadow=ft.BoxShadow(blur_radius=10)
        ),
        ft.Container(
            width=page.width * 0.15, height=page.width * 0.15,
            border_radius=360,  # Круглый край
            gradient=ft.LinearGradient(
                colors=['#ffb6c1', '#ff6347'],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            alignment=ft.alignment.center,
            bottom=page.width * 0.10,
            left=page.width * 0.15,
            shadow=ft.BoxShadow(blur_radius=10)
        ),
        ft.Container(
            width=page.width * 0.10, height=page.width * 0.10,
            border_radius=360,  # Круглый край
            gradient=ft.LinearGradient(
                colors=['#ff6347', '#00fa9a'],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            alignment=ft.alignment.center,
            bottom=page.width * 0.10,
            right=page.width * 0.5,
            shadow=ft.BoxShadow(blur_radius=10)
        ),
    ]
