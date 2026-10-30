import flet as ft


class Palette:
    def __init__(self, is_dark: bool):
        self.is_dark = is_dark
        if is_dark:
            # Authentic GitHub / Linear dark UI
            self.bg = "#0D1117"
            self.surface = "#161B22"
            self.card = "#161B22"
            self.sidebar = "#0D1117"
            self.border = "#30363D"
            self.input_bg = "#0D1117"
            self.input_border = "#30363D"
            self.primary = "#238636"              # GitHub submit green
            self.primary_hover = "#2EA043"
            self.secondary_green = "#238636"      # Backward compatibility
            self.secondary_green_hover = "#2EA043"
            self.accent = "#58A6FF"
            self.text_title = "#F0F6FC"
            self.text_body = "#C9D1D9"
            self.text_muted = "#8B949E"
            self.link = "#58A6FF"
            self.shadow = "#24000000"
        else:
            # Authentic GitHub / Government portal light UI (crisp, zero glow)
            self.bg = "#F6F8FA"
            self.surface = "#FFFFFF"
            self.card = "#FFFFFF"
            self.sidebar = "#F6F8FA"
            self.border = "#D0D7DE"
            self.input_bg = "#FFFFFF"
            self.input_border = "#D0D7DE"
            self.primary = "#1F883D"              # Solid functional green
            self.primary_hover = "#1A7F37"
            self.secondary_green = "#1F883D"      # Backward compatibility
            self.secondary_green_hover = "#1A7F37"
            self.accent = "#0969DA"               # Standard functional blue
            self.text_title = "#1F2328"
            self.text_body = "#1F2328"
            self.text_muted = "#656D76"
            self.link = "#0969DA"
            self.shadow = "#08000000"


def get_app_theme():
    return ft.Theme(
        font_family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    )
