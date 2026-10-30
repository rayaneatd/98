import flet as ft
from src.theme import Palette


def build_onboarding_view(
    page: ft.Page,
    user_data: dict,
    on_finish_onboarding,
    on_back_to_portal,
    on_toggle_theme,
    is_dark: bool,
):
    """
    Standardized, clean, classical admission questionnaire.
    No gimmicky chips: realistic open text fields, standard radio inputs,
    and formal collegiate layout.
    """
    pal = Palette(is_dark)

    user_email = user_data.get("email", "applicant@registry.internal")
    app_id = f"APP-{(abs(hash(user_email)) % 900000) + 100000}"

    error_banner = ft.Container(
        content=ft.Text("", size=12, color="#991B1B"),
        bgcolor="#FEE2E2" if not is_dark else "#450A0A",
        border=ft.Border.all(1, "#F87171" if not is_dark else "#991B1B"),
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        border_radius=3,
        visible=False,
    )

    # Question 1: Target Skills (Free Text Input)
    skills_field = ft.TextField(
        hint_text="e.g., Python, PostgreSQL, and FastAPI",
        border={
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(border_radius=3, side=ft.BorderSide(1, pal.input_border)),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(border_radius=3, side=ft.BorderSide(1.5, pal.primary)),
        },
        bgcolor=pal.input_bg,
        color=pal.text_body,
        hint_style=ft.TextStyle(size=12, color=pal.text_muted),
        text_size=13,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )

    # Question 2: Academic & Professional Objective (Free Text Input)
    objective_field = ft.TextField(
        hint_text="Explain what specific technical problems you want to solve with these skills, and why they must be studied together.",
        multiline=True,
        min_lines=3,
        max_lines=5,
        border={
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(border_radius=3, side=ft.BorderSide(1, pal.input_border)),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(border_radius=3, side=ft.BorderSide(1.5, pal.primary)),
        },
        bgcolor=pal.input_bg,
        color=pal.text_body,
        hint_style=ft.TextStyle(size=12, color=pal.text_muted),
        text_size=13,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )

    # Question 3: Current Technical Background (Standard Radios)
    background_radio = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(value="non_tech", label="Non-technical professional (Transitioning / Career switch)"),
                ft.Radio(value="stem_student", label="STEM / Computer Science university student"),
                ft.Radio(value="self_taught", label="Self-taught programmer (Foundations in progress)"),
                ft.Radio(value="working_dev", label="Practicing developer looking to formalize gaps"),
            ],
            spacing=4,
        ),
        value="self_taught",
    )

    # Question 4: Current Baseline Proficiency (Standard Radios)
    proficiency_radio = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="beginner", label="Complete Beginner"),
                ft.Radio(value="elementary", label="Elementary Syntax"),
                ft.Radio(value="intermediate", label="Functional Knowledge"),
            ],
            spacing=16,
        ),
        value="elementary",
    )

    # Question 5: Weekly Commitment (Standard Radios)
    hours_radio = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="10", label="10 hrs/week (Part-Time)"),
                ft.Radio(value="15", label="15 hrs/week (Standard)"),
                ft.Radio(value="25", label="25+ hrs/week (Intensive)"),
            ],
            spacing=16,
        ),
        value="15",
    )

    # Question 6: Study Period & Final Examination Target (Standard Radios)
    duration_radio = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="30", label="30 Days (Accelerated)"),
                ft.Radio(value="45", label="45 Days (Standard)"),
                ft.Radio(value="60", label="60 Days (Extended)"),
            ],
            spacing=16,
        ),
        value="45",
    )

    # Question 7: Honor Code & Attendance Compact
    compact_checkbox = ft.Checkbox(
        label="I certify that the information provided is accurate. I understand that attendance is tracked daily, missed milestones require written explanations, and graduation requires scoring at least 70% on the final proctored exam.",
        value=True,
    )

    def handle_submit(e):
        skills_val = skills_field.value.strip() if skills_field.value else ""
        obj_val = objective_field.value.strip() if objective_field.value else ""

        if not skills_val:
            error_banner.content.value = "Error: Please specify the technical skills you wish to learn in Section 1."
            error_banner.visible = True
            page.update()
            return

        if not obj_val:
            error_banner.content.value = "Error: Please state your study objective in Section 2."
            error_banner.visible = True
            page.update()
            return

        if not compact_checkbox.value:
            error_banner.content.value = "Error: You must accept the attendance compact in Section 7 to submit."
            error_banner.visible = True
            page.update()
            return

        # Success - prepare structured application data
        # Split skills by comma or plus
        raw_skills = [s.strip() for s in skills_val.replace("+", ",").split(",") if s.strip()]
        if not raw_skills:
            raw_skills = [skills_val]

        application_payload = {
            "skills": raw_skills,
            "skills_raw": skills_val,
            "thesis": obj_val,
            "background": background_radio.value,
            "baseline": proficiency_radio.value,
            "hours_per_week": int(hours_radio.value),
            "duration_days": int(duration_radio.value),
            "slot": "evenings",
        }

        on_finish_onboarding(application_payload)

    # Masthead for form
    form_masthead = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, size=18, color="#FFFFFF"),
                        ft.Text(
                            "NINETY EIGHT INSTITUTE — STANDARDIZED ADMISSION QUESTIONNAIRE",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        ),
                    ],
                    spacing=10,
                ),
                ft.TextButton(
                    content=ft.Text("Return to Portal", size=11, color="#FFFFFF"),
                    on_click=lambda e: on_back_to_portal(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=pal.navbar,
        padding=ft.Padding.symmetric(horizontal=24, vertical=8),
    )

    # Form Sections Helper
    def form_section(num, title, subtitle, control):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"{num}. {title}", size=13, weight=ft.FontWeight.BOLD, color=pal.text_title),
                    ft.Text(subtitle, size=11, color=pal.text_muted) if subtitle else ft.Container(),
                    ft.Container(height=2),
                    control,
                ],
                spacing=4,
            ),
            padding=ft.Padding.only(bottom=14),
        )

    # The Paper Sheet (Like a classical university printed application form)
    form_sheet = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("FORM ADM-2026: CURRICULUM PETITION & STUDY PLAN", size=16, weight=ft.FontWeight.BOLD, color=pal.text_title),
                                ft.Text(f"Application File: {app_id} • Applicant: {user_email}", size=11, color=pal.text_muted),
                            ],
                            spacing=2,
                        ),
                        ft.Container(
                            content=ft.Text("SECTION I OF I", size=10, weight=ft.FontWeight.BOLD, color=pal.text_muted),
                            border=ft.Border.all(1, pal.border),
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                            border_radius=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color=pal.border),
                error_banner,
                form_section(
                    "1",
                    "Proposed Technical Skills",
                    "Enter the technologies you want to study. You may list several (e.g., Python, SQL, Docker).",
                    skills_field,
                ),
                form_section(
                    "2",
                    "Statement of Objective & Interdependence",
                    "Explain why you selected these skills together and how they relate to your practical goals.",
                    objective_field,
                ),
                form_section(
                    "3",
                    "Current Educational / Professional Background",
                    "Select the category that most accurately describes your previous background.",
                    background_radio,
                ),
                form_section(
                    "4",
                    "Self-Reported Baseline Proficiency",
                    "Assess your current level in the technologies listed above.",
                    proficiency_radio,
                ),
                form_section(
                    "5",
                    "Dedicated Weekly Study Capacity",
                    "Estimate the active hours per week you will reserve for coursework and problem sets.",
                    hours_radio,
                ),
                form_section(
                    "6",
                    "Target Term Duration to Final Proctored Exam",
                    "Select the timeframe within which you commit to sitting the final comprehensive assessment.",
                    duration_radio,
                ),
                form_section(
                    "7",
                    "Academic Honor & Attendance Compact",
                    "",
                    compact_checkbox,
                ),
                ft.Divider(height=1, color=pal.border),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            "Cancel & Discard",
                            on_click=lambda e: on_back_to_portal(),
                        ),
                        ft.Container(
                            content=ft.Text("Submit Formal Application", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            bgcolor=pal.secondary_green,
                            border_radius=3,
                            padding=ft.Padding.symmetric(horizontal=24, vertical=11),
                            ink=True,
                            on_click=handle_submit,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
        ),
        width=840,
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=4,
        padding=ft.Padding.all(28),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=pal.shadow,
            offset=(0, 2),
        ),
    )

    return ft.Column(
        controls=[
            form_masthead,
            ft.Container(
                content=form_sheet,
                alignment=ft.Alignment.TOP_CENTER,
                padding=ft.Padding.symmetric(horizontal=16, vertical=20),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
