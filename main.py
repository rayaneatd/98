import flet as ft
from src.theme import get_app_theme, Palette
from src.views.login_view import build_login_view
from src.views.admissions_view import build_admissions_portal_view
from src.views.onboarding_view import build_onboarding_view
from src.views.dashboard_view import build_matriculated_dashboard_view
from src.services.auth_service import sign_out


def main(page: ft.Page):
    page.title = "Ninety Eight — Private Technical Institute"
    page.theme = get_app_theme()
    page.padding = 0

    current_mode = [ft.ThemeMode.LIGHT]
    if page.platform_brightness == ft.Brightness.DARK:
        current_mode[0] = ft.ThemeMode.DARK

    def is_dark():
        return current_mode[0] == ft.ThemeMode.DARK

    page.theme_mode = current_mode[0]

    if page.window:
        page.window.width = 1060
        page.window.height = 780
        page.window.min_width = 850
        page.window.min_height = 660

    # User state
    current_user = [{"name": "Candidate Scholar", "email": "candidate@ninetyeight.institute"}]
    matriculation_data = [{}]

    def toggle_theme(e):
        current_mode[0] = ft.ThemeMode.LIGHT if is_dark() else ft.ThemeMode.DARK
        page.theme_mode = current_mode[0]
        # Refresh current active view
        if not current_user[0].get("authenticated"):
            load_login_view()
        elif matriculation_data[0].get("skills"):
            load_dashboard_view()
        else:
            load_admissions_view()

    def handle_logout(e=None):
        sign_out()
        current_user[0] = {}
        matriculation_data[0] = {}
        load_login_view()

    def handle_login_success(user_data):
        current_user[0] = user_data
        current_user[0]["authenticated"] = True
        load_admissions_view()

    def handle_start_application():
        load_onboarding_view()

    def handle_finish_onboarding(app_data):
        matriculation_data[0] = app_data
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
        portal = build_admissions_portal_view(
            page=page,
            user_data=current_user[0],
            on_start_application=handle_start_application,
            on_logout=handle_logout,
            on_toggle_theme=toggle_theme,
            is_dark=is_dark(),
        )
        page.add(portal)
        page.update()

    def load_onboarding_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        onboarding = build_onboarding_view(
            page=page,
            user_data=current_user[0],
            on_finish_onboarding=handle_finish_onboarding,
            on_back_to_portal=load_admissions_view,
            on_toggle_theme=toggle_theme,
            is_dark=is_dark(),
        )
        page.add(onboarding)
        page.update()

    def load_dashboard_view():
        pal = Palette(is_dark())
        page.bgcolor = pal.bg
        page.clean()
        dashboard = build_matriculated_dashboard_view(
            page=page,
            user_data=current_user[0],
            app_data=matriculation_data[0],
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
