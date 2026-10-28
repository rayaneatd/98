import flet as ft
from src.theme import get_app_theme, Palette
from src.views.login_view import build_login_view


def main(page: ft.Page):
    page.title = "Ninety Eight — Connexion"
    page.theme = get_app_theme()
    page.padding = 0

    current_mode = [ft.ThemeMode.LIGHT]
    if page.platform_brightness == ft.Brightness.DARK:
        current_mode[0] = ft.ThemeMode.DARK

    def is_dark():
        return current_mode[0] == ft.ThemeMode.DARK

    page.theme_mode = current_mode[0]

    if page.window:
        page.window.width = 1040
        page.window.height = 760
        page.window.min_width = 820
        page.window.min_height = 640

    def toggle_theme(e):
        current_mode[0] = ft.ThemeMode.LIGHT if is_dark() else ft.ThemeMode.DARK
        page.theme_mode = current_mode[0]
        load_login_view()

    def handle_login_success(user_data):
        pal = Palette(is_dark())
        page.clean()
        page.bgcolor = pal.bg

        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Bienvenue",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=pal.text_title,
                        ),
                        ft.Text(
                            f"Connecté en tant que {user_data.get('name', 'Utilisateur')} ({user_data.get('email', '')})",
                            size=14,
                            color=pal.text_muted,
                        ),
                        ft.Container(height=12),
                        ft.Container(
                            content=ft.Text(
                                "Se déconnecter",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color="#FFFFFF",
                            ),
                            bgcolor=pal.primary,
                            border_radius=6,
                            padding=ft.Padding.symmetric(horizontal=18, vertical=10),
                            ink=True,
                            on_click=lambda e: load_login_view(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
                bgcolor=pal.bg,
            )
        )
        page.update()

    def load_login_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        login_view = build_login_view(page, handle_login_success, toggle_theme, is_dark())
        page.add(login_view)
        page.update()

    load_login_view()


if __name__ == "__main__":
    ft.run(main)
