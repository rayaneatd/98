import flet as ft
from src.theme import Palette


def build_matriculated_dashboard_view(
    page: ft.Page,
    user_data: dict,
    app_data: dict,
    on_reconfigure,
    on_logout,
    on_toggle_theme,
    is_dark: bool,
):
    """
    Clean, functional student workspace.
    No fake stats, real daily task list, attendance tracker, and excuse dialog.
    """
    pal = Palette(is_dark)

    user_email = user_data.get("email", "student@user.net")
    skills = app_data.get("skills_raw", "Python, SQL")
    deadline = app_data.get("deadline", "45 days")
    hours = app_data.get("hours", "10-15 hrs/wk")

    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Ninety Eight", size=14, weight=ft.FontWeight.W_600, color=pal.text_title),
                        ft.Text("/", size=14, color=pal.text_muted),
                        ft.Text("Dashboard", size=14, color=pal.text_muted),
                    ],
                    spacing=6,
                ),
                ft.Row(
                    controls=[
                        ft.Text(user_email, size=12, color=pal.text_muted),
                        ft.IconButton(
                            icon=ft.Icons.LIGHT_MODE_OUTLINED if is_dark else ft.Icons.DARK_MODE_OUTLINED,
                            tooltip="Theme",
                            icon_color=pal.text_muted,
                            icon_size=16,
                            on_click=on_toggle_theme,
                        ),
                        ft.TextButton(
                            content=ft.Text("Sign out", size=12, color=pal.text_muted),
                            on_click=on_logout,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=pal.surface,
        border=ft.Border(bottom=ft.BorderSide(1, pal.border)),
        padding=ft.Padding.symmetric(horizontal=24, vertical=10),
    )

    # Absence Excuse Dialog State
    excuse_input = ft.TextField(
        hint_text="Explain the legitimate reason for your absence...",
        multiline=True,
        min_lines=3,
        bgcolor=pal.input_bg,
        color=pal.text_body,
        text_size=13,
        border_color=pal.input_border,
    )

    def close_dialog(e):
        page.pop_dialog()

    def submit_excuse(e):
        page.pop_dialog()
        snack = ft.SnackBar(
            content=ft.Text("Excuse submitted to your Teacher. Reviewing..."),
            bgcolor=pal.primary,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    excuse_dialog = ft.AlertDialog(
        title=ft.Text("Report Absence / Submit Justification", size=15, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Your Teacher evaluates every excuse. Weak or dishonest justifications lead to penalty drills.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Container(height=4),
                excuse_input,
            ],
            spacing=6,
            height=140,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.ElevatedButton("Submit Excuse", bgcolor=pal.primary, color="#FFFFFF", on_click=submit_excuse),
        ],
    )

    def open_excuse_dialog(e):
        page.show_dialog(excuse_dialog)

    # Program summary bar
    summary_box = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(f"Current Track: {skills}", size=15, weight=ft.FontWeight.BOLD, color=pal.text_title),
                        ft.Text(f"Pace: {hours} • Examination Target: {deadline}", size=12, color=pal.text_muted),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.OutlinedButton(
                    "Change Track",
                    on_click=lambda e: on_reconfigure(),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=pal.surface,
        border=ft.Border.all(1, pal.border),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
    )

    # Daily Tasks List
    task_checkbox_1 = ft.Checkbox(label="Complete setup drill: configure local virtualenv & package dependencies", value=False)
    task_checkbox_2 = ft.Checkbox(label="Practice: Write and run 3 basic schema queries in Python", value=False)
    task_checkbox_3 = ft.Checkbox(label="Submit check-in summary before midnight", value=False)

    tasks_box = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Today's Milestones (Day 1)", size=14, weight=ft.FontWeight.BOLD, color=pal.text_title),
                        ft.Container(
                            content=ft.Text("In Progress", size=11, color=pal.accent),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color=pal.border),
                task_checkbox_1,
                task_checkbox_2,
                task_checkbox_3,
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("Mark Day Complete", size=12, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                            bgcolor=pal.primary,
                            border_radius=4,
                            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                            ink=True,
                            on_click=lambda e: page.open(ft.SnackBar(content=ft.Text("Day 1 completed! Day 2 will unlock tomorrow."), bgcolor=pal.primary)),
                        ),
                        ft.TextButton(
                            content=ft.Text("Cannot attend today? Submit excuse", size=12, color="#CF222E"),
                            on_click=open_excuse_dialog,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=8,
        ),
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=6,
        padding=ft.Padding.all(18),
    )

    # Main column
    body = ft.Container(
        content=ft.Column(
            controls=[
                summary_box,
                tasks_box,
            ],
            spacing=16,
        ),
        width=740,
        padding=ft.Padding.symmetric(vertical=24),
    )

    return ft.Column(
        controls=[
            header,
            ft.Container(
                content=body,
                alignment=ft.Alignment.TOP_CENTER,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
