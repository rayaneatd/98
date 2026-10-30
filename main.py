import flet as ft
from src.theme import get_app_theme, Palette
from src.views.login_view import build_login_view
from src.views.admissions_view import build_admissions_portal_view
from src.views.dashboard_view import build_matriculated_dashboard_view
from src.services.auth_service import sign_out


def main(page: ft.Page):
    page.title = "Ninety Eight"
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
        page.window.min_height = 620

    current_user = [{"email": "candidate@user.net"}]
    current_plan = [{}]

    def toggle_theme(e):
        current_mode[0] = ft.ThemeMode.LIGHT if is_dark() else ft.ThemeMode.DARK
        page.theme_mode = current_mode[0]
        if not current_user[0].get("authenticated"):
            load_login_view()
        elif current_plan[0].get("skills"):
            load_dashboard_view()
        else:
            load_admissions_view()

    def handle_logout(e=None):
        sign_out()
        current_user[0] = {}
        current_plan[0] = {}
        load_login_view()

    def handle_login_success(user_data):
        current_user[0] = user_data
        current_user[0]["authenticated"] = True
        load_admissions_view()

    def handle_submit_plan(payload):
        current_plan[0] = payload
        load_dashboard_view()

    def load_login_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        login_view = build_login_view(page, handle_login_success, toggle_theme, is_dark())
        page.add(login_view)
        page.update()

    def load_admissions_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        admissions = build_admissions_portal_view(
            page=page,
            user_data=current_user[0],
            on_submit_plan=handle_submit_plan,
            on_logout=handle_logout,
            on_toggle_theme=toggle_theme,
            is_dark=is_dark(),
        )
        page.add(admissions)
        page.update()

    def load_dashboard_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        dashboard = build_matriculated_dashboard_view(
            page=page,
            user_data=current_user[0],
            app_data=current_plan[0],
            on_reconfigure=load_admissions_view,
            on_logout=handle_logout,
            on_toggle_theme=toggle_theme,
            is_dark=is_dark(),
        )
        page.add(dashboard)
        page.update()

    load_login_view()


if __name__ == "__main__":
    ft.run(main)
