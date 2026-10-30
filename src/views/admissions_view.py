import flet as ft
from src.theme import Palette


def build_admissions_portal_view(
    page: ft.Page,
    user_data: dict,
    on_start_application,
    on_logout,
    on_toggle_theme,
    is_dark: bool,
):
    """
    The Admissions & Registrar Portal of Ninety Eight Percent.
    A private, automated technical academy enforcing single-cursus study.
    """
    pal = Palette(is_dark)

    user_name = user_data.get("name") or user_data.get("email", "Candidate").split("@")[0]
    user_email = user_data.get("email", "candidate@ninetyeight.institute")
    candidate_id = f"REG-2026-{(abs(hash(user_email)) % 90000) + 10000}"

    # Top Institutional Navbar
    navbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ALL_INCLUSIVE, size=20, color="#FFFFFF"),
                        ft.Text(
                            "NINETY EIGHT  |  PRIVATE TECHNICAL REGISTRY  |  AUTONOMOUS ADMISSIONS",
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

    # Candidate Identification Badge
    badge_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.BADGE_OUTLINED, size=28, color=pal.primary),
                    bgcolor=f"{pal.primary}1A",
                    border_radius=8,
                    padding=12,
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"CANDIDATE: {user_name.upper()}",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=pal.text_title,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "STATUS: AWAITING CURRICULUM",
                                        size=10,
                                        weight=ft.FontWeight.W_700,
                                        color="#EAB308",
                                    ),
                                    bgcolor="#FEF9C3" if not is_dark else "#422006",
                                    border_radius=4,
                                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                ),
                            ],
                            spacing=12,
                        ),
                        ft.Text(
                            f"Registry Dossier: {candidate_id}  •  Credential: {user_email}",
                            size=12,
                            color=pal.text_muted,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        ),
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=8,
        padding=ft.Padding.all(18),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=pal.shadow,
            offset=(0, 2),
        ),
    )

    # Core Institute Notice: Single Cursus Policy
    policy_notice = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.RULE, size=22, color=pal.primary),
                ft.Column(
                    controls=[
                        ft.Text(
                            "THE SINGLE-CURRICULUM CHARTER (NO COURSE-HOPPING)",
                            size=12,
                            weight=ft.FontWeight.W_800,
                            color=pal.text_title,
                        ),
                        ft.Text(
                            "Unlike typical learning platforms with disconnected courses, Ninety Eight operates as a private automated institution. "
                            "You are admitted to ONE cohesive curriculum calibrated to your career thesis. All selected skills must correlate with each other. "
                            "Once matriculated, material is strictly progressive and enforced.",
                            size=12,
                            color=pal.text_body,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor=pal.surface,
        border=ft.Border.all(1, pal.border),
        border_radius=8,
        padding=ft.Padding.all(16),
    )

    # 3 Exemplary Track Cards
    def track_card(title, skills, desc, duration, icon_name):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon_name, size=22, color=pal.primary),
                            ft.Text(
                                title,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=pal.text_title,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(
                        content=ft.Text(
                            skills,
                            size=11,
                            weight=ft.FontWeight.W_600,
                            color=pal.primary,
                        ),
                        bgcolor=f"{pal.primary}12",
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    ),
                    ft.Text(
                        desc,
                        size=12,
                        color=pal.text_muted,
                    ),
                    ft.Divider(height=1, color=pal.border),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SCHEDULE, size=14, color=pal.text_muted),
                            ft.Text(duration, size=11, color=pal.text_muted),
                        ],
                        spacing=6,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=pal.card,
            border=ft.Border.all(1, pal.border),
            border_radius=8,
            padding=ft.Padding.all(16),
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=pal.shadow,
                offset=(0, 2),
            ),
        )

    tracks_grid = ft.Row(
        controls=[
            track_card(
                "Backend & Data Systems",
                "Python + SQL + FastAPI",
                "Designed for production services, relational schemas, high-throughput APIs, and query optimization.",
                "Intensive • 40 to 60 Days",
                ft.Icons.STORAGE,
            ),
            track_card(
                "Applied AI & LLM Engineering",
                "Python + Meta Llama + Vector DBs",
                "Agentic workflows, retrieval-augmented generation, embeddings, and fine-tuning pipelines.",
                "Advanced • 45 to 75 Days",
                ft.Icons.PSYCHOLOGY,
            ),
            track_card(
                "Production Cloud Infrastructure",
                "Python + Docker + CI/CD",
                "Containerization, orchestration, pipeline testing, and reproducible local environments.",
                "Foundational • 30 to 45 Days",
                ft.Icons.CLOUD_SYNC,
            ),
        ],
        spacing=14,
    )

    # Action Banner: Launch Formal Application / Onboarding
    apply_cta = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Ready to formulate your Study Thesis?",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=pal.text_title,
                        ),
                        ft.Text(
                            "Select an accredited track above or assemble a custom correlated skill-combo in the formal application.",
                            size=12,
                            color=pal.text_muted,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Start Formal Application",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                            ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color="#FFFFFF"),
                        ],
                        spacing=8,
                    ),
                    bgcolor=pal.secondary_green,
                    border_radius=6,
                    padding=ft.Padding.symmetric(horizontal=24, vertical=14),
                    ink=True,
                    on_click=lambda e: on_start_application(),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color="#3342B72A",
                        offset=(0, 2),
                    ),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        ),
        bgcolor=pal.card,
        border=ft.Border.all(1.5, pal.primary),
        border_radius=8,
        padding=ft.Padding.all(20),
    )

    # Legal / Institutional Notice
    disclaimer = ft.Text(
        "Ninety Eight Percent is an autonomous private learning institute. "
        "Credentials issued are proprietary institutional certificates awarded upon achieving >= 70% on proctored examination.",
        size=10,
        color=pal.text_muted,
        text_align=ft.TextAlign.CENTER,
    )

    # Main Scrollable Body
    content_area = ft.Container(
        content=ft.Column(
            controls=[
                badge_card,
                policy_notice,
                ft.Row(
                    controls=[
                        ft.Text(
                            "FEATURED RIGOR TRACKS (CORRELATED CURRICULA)",
                            size=12,
                            weight=ft.FontWeight.W_800,
                            color=pal.text_muted,
                        ),
                    ],
                ),
                tracks_grid,
                ft.Container(height=4),
                apply_cta,
                disclaimer,
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
