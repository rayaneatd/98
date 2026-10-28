import flet as ft
from src.theme import Palette


def _input_border(pal: Palette):
    return {
        ft.ControlState.DEFAULT: ft.OutlineInputBorder(
            border_radius=6,
            side=ft.BorderSide(1, pal.input_border),
        ),
        ft.ControlState.FOCUSED: ft.OutlineInputBorder(
            border_radius=6,
            side=ft.BorderSide(1.5, pal.primary),
        ),
    }


def build_login_view(page: ft.Page, on_login_success, on_toggle_theme, is_dark: bool):
    """
    Minimalist login screen inspired by Facebook's clean authentication UI.
    English copy, natural tone, without cliché or AI-sounding prose.
    """
    pal = Palette(is_dark)

    email_field = ft.TextField(
        hint_text="Email address or username",
        border=_input_border(pal),
        bgcolor=pal.input_bg,
        text_size=15,
        color=pal.text_body,
        hint_style=ft.TextStyle(color=pal.text_muted, size=15),
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        autofocus=True,
    )

    password_field = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        border=_input_border(pal),
        bgcolor=pal.input_bg,
        text_size=15,
        color=pal.text_body,
        hint_style=ft.TextStyle(color=pal.text_muted, size=15),
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
    )

    error_text = ft.Text(
        "",
        color="#E41E3F",
        size=13,
        visible=False,
    )

    def handle_submit(e=None):
        email_val = (email_field.value or "").strip()
        pwd_val = (password_field.value or "").strip()

        if not email_val:
            error_text.value = "Please enter your email address or username."
            error_text.visible = True
            email_field.focus()
            page.update()
            return

        if not pwd_val:
            error_text.value = "Please enter your password."
            error_text.visible = True
            password_field.focus()
            page.update()
            return

        error_text.visible = False
        page.update()
        on_login_success({
            "email": email_val,
            "name": email_val.split("@")[0].capitalize(),
            "role": "candidate",
        })

    def handle_guest_login(e):
        on_login_success({
            "email": "guest@ninetyeight.local",
            "name": "Guest Scholar",
            "role": "guest",
        })

    email_field.on_submit = handle_submit
    password_field.on_submit = handle_submit

    # Sign Up Dialog
    reg_firstname = ft.TextField(hint_text="First name", border=_input_border(pal), expand=True)
    reg_lastname = ft.TextField(hint_text="Last name", border=_input_border(pal), expand=True)
    reg_email = ft.TextField(hint_text="Email address", border=_input_border(pal))
    reg_password = ft.TextField(hint_text="New password", password=True, can_reveal_password=True, border=_input_border(pal))
    reg_error = ft.Text("", color="#E41E3F", size=12, visible=False)

    def close_register_dialog(e):
        register_dialog.open = False
        page.update()

    def submit_register(e):
        if not (reg_email.value or "").strip() or not (reg_password.value or "").strip():
            reg_error.value = "All required fields must be completed."
            reg_error.visible = True
            page.update()
            return
        register_dialog.open = False
        page.update()
        name = f"{(reg_firstname.value or '').strip()} {(reg_lastname.value or '').strip()}".strip()
        if not name:
            name = reg_email.value.split("@")[0].capitalize()
        on_login_success({
            "email": reg_email.value.strip(),
            "name": name,
            "role": "candidate",
        })

    register_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Column(
            controls=[
                ft.Text("Sign Up", size=22, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text("It's quick and easy.", size=14, color=pal.text_muted),
                ft.Divider(color=pal.border, height=1),
            ],
            spacing=4,
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=[reg_firstname, reg_lastname], spacing=10),
                    reg_email,
                    reg_password,
                    reg_error,
                ],
                spacing=12,
                tight=True,
            ),
            width=400,
        ),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=close_register_dialog,
                style=ft.ButtonStyle(color=pal.text_muted),
            ),
            ft.Container(
                content=ft.Text("Sign Up", size=15, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                bgcolor=pal.secondary_green,
                border_radius=6,
                padding=ft.Padding.symmetric(horizontal=24, vertical=10),
                ink=True,
                on_click=submit_register,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_register_modal(e):
        reg_error.visible = False
        page.overlay.append(register_dialog)
        register_dialog.open = True
        page.update()

    # Forgot Password Dialog
    forgot_email_field = ft.TextField(hint_text="Email address", border=_input_border(pal))
    forgot_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Find Your Account", size=20, weight=ft.FontWeight.BOLD, color=pal.text_title),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Please enter your email address to search for your account.",
                        size=14,
                        color=pal.text_muted,
                    ),
                    forgot_email_field,
                ],
                spacing=12,
                tight=True,
            ),
            width=400,
        ),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=lambda e: setattr(forgot_dialog, "open", False) or page.update(),
                style=ft.ButtonStyle(color=pal.text_muted),
            ),
            ft.Container(
                content=ft.Text("Search", size=14, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                bgcolor=pal.primary,
                border_radius=6,
                padding=ft.Padding.symmetric(horizontal=18, vertical=9),
                ink=True,
                on_click=lambda e: setattr(forgot_dialog, "open", False) or page.update(),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_forgot_modal(e):
        page.overlay.append(forgot_dialog)
        forgot_dialog.open = True
        page.update()

    # Main "Log In" button
    login_btn = ft.Container(
        content=ft.Text(
            "Log In",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=pal.primary,
        border_radius=6,
        height=48,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=handle_submit,
    )

    # Secondary "Create new account" button
    create_btn = ft.Container(
        content=ft.Text(
            "Create new account",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=pal.secondary_green,
        border_radius=6,
        height=46,
        padding=ft.Padding.symmetric(horizontal=20),
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=open_register_modal,
    )

    # Right Login Card
    login_card = ft.Container(
        content=ft.Column(
            controls=[
                email_field,
                password_field,
                error_text,
                login_btn,
                ft.Container(
                    content=ft.Text(
                        "Forgotten password?",
                        size=14,
                        color=pal.primary,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(vertical=6),
                    ink=True,
                    on_click=open_forgot_modal,
                ),
                ft.Divider(color=pal.border, height=1, thickness=1),
                ft.Container(height=6),
                ft.Row(
                    controls=[create_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=396,
        bgcolor=pal.card,
        border_radius=8,
        border=ft.Border.all(1, pal.border) if is_dark else None,
        padding=ft.Padding.all(18),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=16,
            color=pal.shadow,
            offset=(0, 4),
        ),
    )

    # Left Branding Column
    branding_column = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "98%",
                    size=54,
                    weight=ft.FontWeight.BOLD,
                    color=pal.primary,
                ),
                ft.Container(height=4),
                ft.Text(
                    "Ninety Eight helps you structure your technical study and stay accountable to your goals.",
                    size=24,
                    weight=ft.FontWeight.W_400,
                    color=pal.text_title,
                ),
            ],
            spacing=2,
        ),
        width=480,
        padding=ft.Padding.only(right=32, bottom=40),
    )

    # Guest link under card
    bottom_helper = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Exploring the platform?", size=13, color=pal.text_muted),
                ft.Text(
                    "Enter as guest",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=pal.text_title,
                ),
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(top=24),
        ink=True,
        on_click=handle_guest_login,
    )

    right_section = ft.Column(
        controls=[
            login_card,
            bottom_helper,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # Minimal top bar with theme toggle
    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(),
                ft.IconButton(
                    icon=ft.Icons.DARK_MODE_OUTLINED if not is_dark else ft.Icons.LIGHT_MODE_OUTLINED,
                    tooltip="Toggle theme",
                    icon_color=pal.text_muted,
                    icon_size=20,
                    on_click=on_toggle_theme,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=12),
    )

    # Footer
    footer = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Ninety Eight © 2026", size=12, color=pal.text_muted),
                ft.Text("•", size=12, color=pal.text_muted),
                ft.Text("Technical study & accountability", size=12, color=pal.text_muted),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(vertical=16),
    )

    # Centered Two-Column Layout
    center_layout = ft.Container(
        content=ft.Row(
            controls=[
                branding_column,
                right_section,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        padding=ft.Padding.symmetric(horizontal=24),
    )

    return ft.Column(
        controls=[
            top_bar,
            center_layout,
            footer,
        ],
        spacing=0,
        expand=True,
    )
