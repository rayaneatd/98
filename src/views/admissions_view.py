import asyncio
import flet as ft
from src.theme import Palette


def build_admissions_portal_view(
    page: ft.Page,
    user_data: dict,
    on_submit_plan,
    on_logout,
    on_toggle_theme,
    is_dark: bool,
):
    """
    Study Plan Application Form.
    - Skills: Dynamic custom tags created on Enter.
    - Objective: Free text.
    - Background: Free text (past skills, academic/professional background).
    - Schedule: Free text + native file picker (Images/PDFs up to 5MB).
    - Duration Intent: Free text replacing rigid exam date.
    FilePicker registered in page.services as required by Flet 1.0.5.
    """
    pal = Palette(is_dark)
    user_email = user_data.get("email", "candidate@user.net")

    # ─── Skills Tag System ───────────────────────────────────────────────────
    skills_list = []
    tags_row = ft.Row(wrap=True, spacing=6, run_spacing=6)

    def render_tags():
        tags_row.controls.clear()
        for s in skills_list:
            tags_row.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(s, size=12, color=pal.text_title, weight=ft.FontWeight.W_500),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=12,
                                icon_color=pal.text_muted,
                                padding=0,
                                width=18,
                                height=18,
                                on_click=lambda e, name=s: remove_skill(name),
                            ),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                    bgcolor=pal.surface,
                    border=ft.Border.all(1, pal.border),
                    border_radius=4,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                )
            )
        page.update()

    def remove_skill(name):
        if name in skills_list:
            skills_list.remove(name)
            render_tags()

    def handle_skill_submit(e):
        raw = (skill_input.value or "").strip()
        if raw:
            for part in [p.strip() for p in raw.replace("+", ",").split(",") if p.strip()]:
                if part and part not in skills_list:
                    skills_list.append(part)
            skill_input.value = ""
            render_tags()
            skill_input.focus()

    skill_input = ft.TextField(
        hint_text="Type a skill and press Enter (e.g. Python, SQL, Docker)...",
        bgcolor=pal.input_bg,
        color=pal.text_body,
        text_size=13,
        border_color=pal.input_border,
        focused_border_color=pal.accent,
        border_radius=4,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        on_submit=handle_skill_submit,
    )

    # ─── Text Fields ─────────────────────────────────────────────────────────
    def make_textarea(hint, min_l=3, max_l=8):
        return ft.TextField(
            hint_text=hint,
            multiline=True,
            min_lines=min_l,
            max_lines=max_l,
            bgcolor=pal.input_bg,
            color=pal.text_body,
            text_size=13,
            border_color=pal.input_border,
            focused_border_color=pal.accent,
            border_radius=4,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        )

    objective_input = make_textarea(
        "What do you plan to build or achieve with these skills? Why learn them together?"
    )
    background_input = make_textarea(
        "Detail your current technical knowledge, academic/professional background, or anything you have self-taught so far."
    )
    schedule_input = make_textarea(
        "Describe when you work, your available windows (e.g. evenings Mon–Fri), and any constraints your Teacher must know."
    )
    duration_input = make_textarea(
        "How long would you like to spend mastering these skills? Describe your ideal learning pace, any fixed deadline you have in mind, or why you want to reach a certain level by a certain point.",
        min_l=2,
        max_l=5,
    )

    # ─── File Upload (Flet 1.0.5 Service Pattern) ────────────────────────────
    uploaded_files = []
    files_column = ft.Column(spacing=4)
    file_error_text = ft.Text("", size=11, color="#CF222E", visible=False)
    MAX_SIZE = 5 * 1024 * 1024  # 5 MB

    def render_uploaded_files():
        files_column.controls.clear()
        for f in uploaded_files:
            kb = f["size"] / 1024
            size_str = f"{kb:.0f} KB" if kb < 1024 else f"{kb / 1024:.1f} MB"
            ext = f["name"].rsplit(".", 1)[-1].lower()
            icon = ft.Icons.PICTURE_AS_PDF if ext == "pdf" else ft.Icons.IMAGE_OUTLINED
            files_column.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon, size=15, color=pal.accent),
                            ft.Text(f["name"], size=12, color=pal.text_title, weight=ft.FontWeight.W_500),
                            ft.Text(f"({size_str})", size=11, color=pal.text_muted),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_size=14,
                                icon_color="#CF222E",
                                tooltip="Remove",
                                padding=0,
                                width=18,
                                height=18,
                                on_click=lambda e, path=f["path"]: remove_uploaded(path),
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=pal.surface,
                    border=ft.Border.all(1, pal.border),
                    border_radius=4,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                )
            )
        page.update()

    def remove_uploaded(path):
        for f in list(uploaded_files):
            if f.get("path") == path:
                uploaded_files.remove(f)
        render_uploaded_files()

    def on_file_picked(e: ft.FilePickerResultEvent):
        file_error_text.visible = False
        if e.files:
            for f in e.files:
                if f.size > MAX_SIZE:
                    file_error_text.value = f"'{f.name}' exceeds the 5 MB limit and was skipped."
                    file_error_text.visible = True
                    continue
                if not any(item.get("path") == f.path for item in uploaded_files):
                    uploaded_files.append({
                        "name": f.name,
                        "size": f.size,
                        "path": f.path,
                    })
            render_uploaded_files()
        page.update()

    # In Flet 1.0.5, FilePicker is a Service — register in page.services
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.services.append(file_picker)

    pick_action = ft.PickFiles(
        file_picker=file_picker,
        dialog_title="Select schedule files (Images or PDFs, max 5 MB each)",
        allow_multiple=True,
        file_type=ft.FilePickerFileType.CUSTOM,
        allowed_extensions=["pdf", "png", "jpg", "jpeg", "webp"],
    )

    upload_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.UPLOAD_FILE, size=15, color=pal.text_title),
                ft.Text("Attach files (Images or PDF, up to 5 MB each)", size=12, color=pal.text_title),
            ],
            spacing=6,
        ),
        bgcolor=pal.surface,
        border=ft.Border.all(1, pal.border),
        border_radius=4,
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        ink=True,
        action=pick_action,
    )

    # ─── Validation & Submit ─────────────────────────────────────────────────
    error_banner = ft.Text("", size=12, color="#CF222E", visible=False)

    def handle_submit(e):
        if not skills_list:
            error_banner.value = "Add at least one skill (type and press Enter)."
            error_banner.visible = True
            page.update()
            return
        if not (objective_input.value or "").strip():
            error_banner.value = "Please fill in your learning objective."
            error_banner.visible = True
            page.update()
            return
        if not (background_input.value or "").strip():
            error_banner.value = "Please describe your current background."
            error_banner.visible = True
            page.update()
            return
        sched = (schedule_input.value or "").strip()
        if not sched and not uploaded_files:
            error_banner.value = "Describe your schedule or attach a file."
            error_banner.visible = True
            page.update()
            return

        error_banner.visible = False

        on_submit_plan({
            "skills": list(skills_list),
            "skills_raw": ", ".join(skills_list),
            "thesis": objective_input.value.strip(),
            "background": background_input.value.strip(),
            "schedule": sched,
            "files": list(uploaded_files),
            "duration_intent": (duration_input.value or "").strip(),
        })

    # ─── Layout ──────────────────────────────────────────────────────────────
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Ninety Eight", size=14, weight=ft.FontWeight.W_600, color=pal.text_title),
                        ft.Text("/", size=14, color=pal.text_muted),
                        ft.Text("Study Plan Application", size=14, color=pal.text_muted),
                    ],
                    spacing=6,
                ),
                ft.Row(
                    controls=[
                        ft.Text(user_email, size=12, color=pal.text_muted),
                        ft.IconButton(
                            icon=ft.Icons.LIGHT_MODE_OUTLINED if is_dark else ft.Icons.DARK_MODE_OUTLINED,
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

    def section(title, hint, control):
        return ft.Column(
            controls=[
                ft.Text(title, size=13, weight=ft.FontWeight.W_600, color=pal.text_title),
                ft.Text(hint, size=11, color=pal.text_muted) if hint else ft.Container(),
                control,
            ],
            spacing=4,
        )

    form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Study Plan Application", size=18, weight=ft.FontWeight.BOLD, color=pal.text_title),
                ft.Text(
                    "Your Teacher uses these details to build your curriculum and calibrate your daily workload.",
                    size=12,
                    color=pal.text_muted,
                ),
                ft.Divider(height=1, color=pal.border),
                error_banner,
                section(
                    "Skills to learn",
                    "Type any skill and press Enter to add it as a tag.",
                    ft.Column(controls=[skill_input, tags_row], spacing=8),
                ),
                section(
                    "Learning objective",
                    "What do you plan to build or achieve? Why these skills together?",
                    objective_input,
                ),
                section(
                    "Your background & existing skills",
                    "What do you already know? Include any work experience, degree, or self-taught skills.",
                    background_input,
                ),
                section(
                    "Schedule & availability",
                    "When can you study? Describe your routine and attach a calendar or timetable if you have one.",
                    ft.Column(
                        controls=[
                            schedule_input,
                            upload_btn,
                            file_error_text,
                            files_column,
                        ],
                        spacing=8,
                    ),
                ),
                section(
                    "How long do you want to take?",
                    "Describe your ideal learning pace or any deadline that matters to you.",
                    duration_input,
                ),
                ft.Divider(height=1, color=pal.border),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("Submit & Generate Curriculum", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                            bgcolor=pal.primary,
                            border_radius=4,
                            padding=ft.Padding.symmetric(horizontal=20, vertical=11),
                            ink=True,
                            on_click=handle_submit,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=14,
        ),
        width=720,
        bgcolor=pal.card,
        border=ft.Border.all(1, pal.border),
        border_radius=6,
        padding=ft.Padding.all(26),
    )

    return ft.Column(
        controls=[
            header,
            ft.ListView(
                controls=[
                    ft.Container(
                        content=form_card,
                        alignment=ft.Alignment.TOP_CENTER,
                        padding=ft.Padding.symmetric(vertical=24),
                    )
                ],
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )
