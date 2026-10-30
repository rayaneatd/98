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
    Candidate Active Dashboard: Displays the locked unified curriculum,
    adherence streak, upcoming lesson block, and disciplinary status.
    """
    pal = Palette(is_dark)

    user_name = user_data.get("name") or user_data.get("email", "Candidate").split("@")[0]
    user_email = user_data.get("email", "candidate@ninetyeight.institute")
    skills = app_data.get("skills", ["Python", "SQL"])
    duration = app_data.get("duration_days", 45)
    hours = app_data.get("hours_per_week", 15)
    slot = app_data.get("slot", "evenings").capitalize()

    # Top Navbar
    navbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ALL_INCLUSIVE, size=20, color="#FFFFFF"),
                        ft.Text(
                            "NINETY EIGHT  |  ACTIVE MATRICULATED CURRICULUM",
                            size=11,
                            weight=ft.FontWeight.W_700,
                            color="#FFFFFF",
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.LIGHT_MODE_OUTLINED if is_dark else ft.Icons.DARK_MODE_OUTLINED,
                            tooltip="Toggle Theme",
                            icon_color="#FFFFFF",
                            icon_size=18,
                            on_click=on_toggle_theme,
                        ),
                        ft.TextButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.LOGOUT, size=14, color="#FFFFFF"),
                                    ft.Text("Log Out", size=12, color="#FFFFFF"),
                                ],
                                spacing=4,
                            ),
                            on_click=on_logout,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=pal.primary,
        padding=ft.Padding.symmetric(horizontal=24, vertical=6),
    )

    # Status Banner
    status_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.VERIFIED, size=32, color=pal.secondary_green),
                    bgcolor=f"{pal.secondary_green}1A",
                    border_radius=8,
                    padding=12,
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"MATRICULATED SCHOLAR: {user_name.upper()}",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=pal.text_title,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "STATUS: IN GOOD STANDING",
                                        size=10,
                                        weight=ft.FontWeight.W_700,
                                        color=pal.secondary_green,
                                    ),
                                    bgcolor=f"{pal.secondary_green}1A",
                                    border_radius=4,
                                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                ),
                            ],
                            spacing=12,
                        ),
                        ft.Text(
                            f"Enrolled Major: {' + '.join(skills)}  •  Rigor: {hours} hrs/wk ({slot})  •  Final Exam: {duration} Days",
                            size=12,
                            color=pal.text_muted,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.OutlinedButton(
                    "Petition Review / Reset Track",
                    on_click=lambda e: on_reconfigure(),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        ),
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=8,
        padding=ft.Padding.all(18),
    )

    # 3 Metrics Cards (Progress, Attendance, Disciplinary Standing)
    def metric_card(title, value, sub, icon_name, color):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon_name, size=18, color=color),
                            ft.Text(title, size=11, weight=ft.FontWeight.W_700, color=pal.text_muted),
                        ],
                        spacing=6,
                    ),
                    ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color=pal.text_title),
                    ft.Text(sub, size=11, color=color),
                ],
                spacing=4,
            ),
            bgcolor=pal.card,
            border=ft.Border.all(1, pal.border),
            border_radius=8,
            padding=ft.Padding.all(16),
            expand=True,
        )

    metrics_row = ft.Row(
        controls=[
            metric_card("SYLLABUS PROGRESS", "Day 1 of " + str(duration), "Module 1 Scaffolding Ready", ft.Icons.TRENDING_UP, pal.primary),
            metric_card("DISCIPLINARY RECORD", "0 Strikes", "Absences Pardoned: 0", ft.Icons.GAVEL, pal.secondary_green),
            metric_card("FINAL EXAM READINESS", "0% / 100%", "Threshold: >= 70% required", ft.Icons.VERIFIED_OUTLINED, "#EAB308"),
        ],
        spacing=14,
    )

    # Active Daily Lesson Box
    active_lesson = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, size=20, color=pal.primary),
                        ft.Text(
                            f"CURRENT MANDATORY SESSION: {skills[0]} Foundation & Architecture Setup",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=pal.text_title,
                        ),
                        ft.Container(
                            content=ft.Text("MANDATORY", size=9, weight=ft.FontWeight.BOLD, color="#EF4444"),
                            bgcolor="#FEE2E2" if not is_dark else "#450A0A",
                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                            border_radius=3,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    f"In this block, you formulate your environment according to your vocational thesis: '{app_data.get('thesis', 'Core setup')[:90]}...'. "
                    "Complete the drill by midnight to preserve your attendance record.",
                    size=12,
                    color=pal.text_body,
                ),
                ft.Divider(height=1, color=pal.border),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.PLAY_ARROW, size=16, color="#FFFFFF"),
                                    ft.Text("Begin Assigned Lesson & Drills", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                ],
                                spacing=6,
                            ),
                            bgcolor=pal.primary,
                            border_radius=6,
                            padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                            ink=True,
                        ),
                        ft.OutlinedButton(
                            "Report Absence / Submit Written Excuse to Dean",
                            icon=ft.Icons.MAIL_OUTLINE,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
        bgcolor=pal.card,
        border=ft.Border.all(1.5, pal.primary),
        border_radius=8,
        padding=ft.Padding.all(20),
    )

    content_area = ft.Container(
        content=ft.Column(
            controls=[
                status_card,
                metrics_row,
                active_lesson,
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=960,
        padding=ft.Padding.symmetric(horizontal=16, vertical=20),
    )

    return ft.Column(
        controls=[
            navbar,
            ft.Container(
                content=content_area,
                alignment=ft.Alignment.TOP_CENTER,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
