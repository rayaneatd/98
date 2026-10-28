import flet as ft


class Palette:
    def __init__(self, is_dark: bool):
        self.is_dark = is_dark
        if is_dark:
            # Facebook Dark Mode Authentique
            self.bg = "#18191A"
            self.surface = "#242526"
            self.card = "#242526"
            self.primary = "#2D88FF"
            self.primary_hover = "#1877F2"
            self.secondary_green = "#42B72A"
            self.secondary_green_hover = "#36A420"
            self.border = "#3A3B3C"
            self.input_bg = "#3A3B3C"
            self.input_border = "#4E4F50"
            self.text_title = "#E4E6EB"
            self.text_body = "#E4E6EB"
            self.text_muted = "#B0B3B8"
            self.shadow = "#33000000"
        else:
            # Facebook Light Mode Authentique
            self.bg = "#F0F2F5"
            self.surface = "#FFFFFF"
            self.card = "#FFFFFF"
            self.primary = "#1877F2"
            self.primary_hover = "#166FE5"
            self.secondary_green = "#42B72A"
            self.secondary_green_hover = "#36A420"
            self.border = "#DADDE1"
            self.input_bg = "#FFFFFF"
            self.input_border = "#CCD0D5"
            self.text_title = "#1C1E21"
            self.text_body = "#1C1E21"
            self.text_muted = "#65676B"
            self.shadow = "#14000000"


def get_app_theme():
    return ft.Theme(
        font_family="Segoe UI, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif",
    )
