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
    Candidate Formal Application & Curriculum Formulator (The Onboarding).
    4 steps:
    1. Skill Selection & Inter-correlation Thesis (Why this specific combo?)
    2. Background Assessment & Baseline Proficiency
    3. Study Schedule, Hours/Week & Blackout constraints
    4. Target Examination Deadline & Matriculation Oath
    """
    pal = Palette(is_dark)

    current_step = [1]
    application_data = {
        "skills": ["Python", "SQL"],
        "thesis": "",
        "background": "self_taught",
        "baseline": "beginner",
        "hours_per_week": 15,
        "slot": "evenings",
        "blackout_days": "None",
        "duration_days": 45,
    }

    container_body = ft.Container(expand=True)

    # Available skills chips
    AVAILABLE_SKILLS = [
        "Python", "SQL", "FastAPI", "Docker", "Meta Llama / LLMs",
        "Vector Databases", "Git & CI/CD", "Data Structures", "System Design"
    ]

    def update_step_view():
        step = current_step[0]
        step_indicator.content = ft.Row(
            controls=[
                ft.Text(f"STEP {step} OF 4", size=11, weight=ft.FontWeight.W_800, color=pal.primary),
                ft.Container(
                    width=180,
                    height=6,
                    bgcolor=pal.border,
                    border_radius=3,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=180 * (step / 4),
                                height=6,
                                bgcolor=pal.primary,
                                border_radius=3,
                            )
                        ]
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        if step == 1:
            render_step_1()
        elif step == 2:
            render_step_2()
        elif step == 3:
            render_step_3()
        elif step == 4:
            render_step_4()

        page.update()

    # Step 1: Skills & Thesis
    def render_step_1():
        def toggle_skill(skill_name):
            if skill_name in application_data["skills"]:
                if len(application_data["skills"]) > 1:
                    application_data["skills"].remove(skill_name)
            else:
                application_data["skills"].append(skill_name)
            render_step_1()
            page.update()

        chips = []
        for s in AVAILABLE_SKILLS:
            is_selected = s in application_data["skills"]
            chips.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.CHECK if is_selected else ft.Icons.ADD,
                                size=13,
                                color="#FFFFFF" if is_selected else pal.text_body,
                            ),
                            ft.Text(
                                s,
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color="#FFFFFF" if is_selected else pal.text_body,
                            ),
                        ],
                        spacing=4,
                    ),
                    bgcolor=pal.primary if is_selected else pal.surface,
                    border=ft.Border.all(1, pal.primary if is_selected else pal.border),
                    border_radius=16,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    ink=True,
                    on_click=lambda e, name=s: toggle_skill(name),
                )
            )

        thesis_input = ft.TextField(
            hint_text="e.g. 'I need to master SQL and Python to build automated backend data ingestion pipelines for my job transition by summer.'",
            multiline=True,
            min_lines=3,
            max_lines=4,
            value=application_data["thesis"],
            border={
                ft.ControlState.DEFAULT: ft.OutlineInputBorder(border_radius=6, side=ft.BorderSide(1, pal.border)),
                ft.ControlState.FOCUSED: ft.OutlineInputBorder(border_radius=6, side=ft.BorderSide(1.5, pal.primary)),
            },
            bgcolor=pal.input_bg,
            color=pal.text_body,
            hint_style=ft.TextStyle(size=12, color=pal.text_muted),
            text_size=13,
            on_change=lambda e: application_data.update({"thesis": e.control.value}),
        )

        combo_text = " + ".join(application_data["skills"])

        container_body.content = ft.Column(
            controls=[
                ft.Text("1. Academic Major & Correlated Skills", size=18, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text(
                    "Select the technologies that compose your unified curriculum. All skills must reinforce each other.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Container(height=4),
                ft.Text("Select Skills (Multiple allowed):", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                ft.Row(controls=chips, wrap=True, spacing=8),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.AUTO_AWESOME, size=16, color=pal.primary),
                            ft.Text(f"Current Correlated Focus: {combo_text}", size=12, weight=ft.FontWeight.BOLD, color=pal.primary),
                        ],
                        spacing=8,
                    ),
                    bgcolor=f"{pal.primary}10",
                    border=ft.Border.all(1, f"{pal.primary}33"),
                    border_radius=6,
                    padding=ft.Padding.all(10),
                ),
                ft.Container(height=4),
                ft.Text(
                    "State Your Vocational Thesis (Why these specific skills?):",
                    size=12,
                    weight=ft.FontWeight.W_700,
                    color=pal.text_title,
                ),
                thesis_input,
                ft.Text(
                    "Note: The Autonomous Dean uses this thesis to reject procrastination and calibrate your makeup assignments.",
                    size=10,
                    color=pal.text_muted,
                ),
            ],
            spacing=10,
        )

    # Step 2: Background & Baseline
    def render_step_2():
        bg_radios = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="cs_student", label="Computer Science / STEM Student"),
                    ft.Radio(value="career_changer", label="Career Switcher (Transitioning from non-tech)"),
                    ft.Radio(value="self_taught", label="Self-Taught / Independent Learner"),
                    ft.Radio(value="junior_dev", label="Practicing Junior Developer (Upskilling)"),
                ],
                spacing=6,
            ),
            value=application_data["background"],
            on_change=lambda e: application_data.update({"background": e.control.value}),
        )

        level_radios = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="beginner", label="Absolute Beginner"),
                    ft.Radio(value="intermediate", label="Some Syntax Knowledge"),
                    ft.Radio(value="advanced_basics", label="Solid Fundamentals"),
                ],
                spacing=12,
            ),
            value=application_data["baseline"],
            on_change=lambda e: application_data.update({"baseline": e.control.value}),
        )

        container_body.content = ft.Column(
            controls=[
                ft.Text("2. Candidate Background & Baseline Assessment", size=18, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text(
                    "Help the curriculum engine determine whether to begin with conceptual scaffolding or jump directly to drills.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Container(height=6),
                ft.Text("What best describes your current technical background?", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                bg_radios,
                ft.Container(height=6),
                ft.Text("What is your current baseline on your selected technologies?", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                level_radios,
            ],
            spacing=10,
        )

    # Step 3: Schedule & Weekly Commitment
    def render_step_3():
        hours_slider = ft.Slider(
            min=5,
            max=40,
            divisions=7,
            value=application_data["hours_per_week"],
            label="{value} hrs/week",
            active_color=pal.primary,
            on_change=lambda e: (
                application_data.update({"hours_per_week": int(e.control.value)}),
                hours_label.update(),
            ),
        )

        hours_label = ft.Text(
            f"Commitment: {application_data['hours_per_week']} hours per week",
            size=13,
            weight=ft.FontWeight.BOLD,
            color=pal.primary,
        )

        slot_radios = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="mornings", label="Early Mornings (6am - 9am)"),
                    ft.Radio(value="evenings", label="Evenings (7pm - 11pm)"),
                    ft.Radio(value="weekends", label="Weekend Concentrated"),
                    ft.Radio(value="fulltime", label="Full-Time Flexible"),
                ],
                spacing=8,
            ),
            value=application_data["slot"],
            on_change=lambda e: application_data.update({"slot": e.control.value}),
        )

        blackout_input = ft.TextField(
            hint_text="e.g. 'Unavailable on Wednesdays due to late work shift'",
            value=application_data["blackout_days"],
            bgcolor=pal.input_bg,
            color=pal.text_body,
            text_size=13,
            border={
                ft.ControlState.DEFAULT: ft.OutlineInputBorder(border_radius=6, side=ft.BorderSide(1, pal.border)),
                ft.ControlState.FOCUSED: ft.OutlineInputBorder(border_radius=6, side=ft.BorderSide(1.5, pal.primary)),
            },
            on_change=lambda e: application_data.update({"blackout_days": e.control.value}),
        )

        container_body.content = ft.Column(
            controls=[
                ft.Text("3. Weekly Capacity & Schedule Constraints", size=18, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text(
                    "Attendance is strictly tracked. The system allocates daily lesson blocks based strictly on this schedule.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Container(height=4),
                hours_label,
                hours_slider,
                ft.Container(height=4),
                ft.Text("Primary Study Slot:", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                slot_radios,
                ft.Container(height=4),
                ft.Text("Blackout / Reserved Days (When the AI will NOT schedule sessions):", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                blackout_input,
            ],
            spacing=8,
        )

    # Step 4: Examination Deadline & Oath
    def render_step_4():
        duration_radios = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="30", label="30 Days (Commando Track)"),
                    ft.Radio(value="45", label="45 Days (Standard Rigor)"),
                    ft.Radio(value="60", label="60 Days (Comprehensive)"),
                ],
                spacing=16,
            ),
            value=str(application_data["duration_days"]),
            on_change=lambda e: application_data.update({"duration_days": int(e.control.value)}),
        )

        oath_box = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.VERIFIED, size=20, color=pal.primary),
                            ft.Text(
                                "MATRICULATION OATH & DISCIPLINARY COMPACT",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=pal.text_title,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Text(
                        "1. I acknowledge that I cannot course-hop; my curriculum is locked to my selected major.\n"
                        "2. In the event of missed milestones, I will submit formal written justifications to the AI Proctor.\n"
                        "3. Unjustified absences will incur makeup penalty drills before new lessons unlock.\n"
                        "4. Certification requires passing the final timed proctored exam with >= 70%.",
                        size=11,
                        color=pal.text_body,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=pal.surface,
            border=ft.Border.all(1, pal.border),
            border_radius=6,
            padding=ft.Padding.all(14),
        )

        container_body.content = ft.Column(
            controls=[
                ft.Text("4. Target Examination Deadline & Matriculation Oath", size=18, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text(
                    "Upon deadline expiration, the Pearson VUE-style certification test will be scheduled.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Container(height=4),
                ft.Text("Choose Curricular Duration to Final Exam:", size=12, weight=ft.FontWeight.W_700, color=pal.text_title),
                duration_radios,
                ft.Container(height=6),
                oath_box,
            ],
            spacing=10,
        )

    def handle_next(e):
        if current_step[0] < 4:
            current_step[0] += 1
            update_step_view()
        else:
            on_finish_onboarding(application_data)

    def handle_prev(e):
        if current_step[0] > 1:
            current_step[0] -= 1
            update_step_view()
        else:
            on_back_to_portal()

    # Step Indicator
    step_indicator = ft.Container(padding=ft.Padding.only(bottom=10))

    # Top Mini Bar
    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=18, color="#FFFFFF"),
                        ft.Text(
                            "NINETY EIGHT  |  FORMAL CANDIDATE DOSSIER  |  CURRICULUM FORMULATION",
                            size=11,
                            weight=ft.FontWeight.W_700,
                            color="#FFFFFF",
                        ),
                    ],
                    spacing=8,
                ),
                ft.TextButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.ARROW_BACK, size=14, color="#FFFFFF"),
                            ft.Text("Cancel to Portal", size=11, color="#FFFFFF"),
                        ],
                        spacing=4,
                    ),
                    on_click=lambda e: on_back_to_portal(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=pal.primary,
        padding=ft.Padding.symmetric(horizontal=24, vertical=6),
    )

    # Nav Buttons
    btn_row = ft.Row(
        controls=[
            ft.OutlinedButton(
                "Previous Step",
                on_click=handle_prev,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Proceed to Next Step", size=13, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=14, color="#FFFFFF"),
                    ],
                    spacing=6,
                ),
                bgcolor=pal.primary,
                border_radius=6,
                padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                ink=True,
                on_click=handle_next,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    card_container = ft.Container(
        content=ft.Column(
            controls=[
                step_indicator,
                container_body,
                ft.Divider(height=1, color=pal.border),
                btn_row,
            ],
            spacing=14,
        ),
        width=780,
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=8,
        padding=ft.Padding.all(24),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=pal.shadow,
            offset=(0, 2),
        ),
    )

    update_step_view()

    return ft.Column(
        controls=[
            top_bar,
            ft.Container(
                content=card_container,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(horizontal=16, vertical=20),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
