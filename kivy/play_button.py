from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors, hue, palette
from kivymd.uix.button import MDFloatingActionButton

class PlayButton(MDFloatingActionButton):
    """
    A button that toggles color + icon when clicked
    """
    RED = tuple(get_color_from_hex(colors["Red"]["A700"]))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "stop"
        self._no_ripple_effect = True
        self.md_bg_color = self.RED

    def toggle(self, app):
        # Toggle color
        primary_color = tuple(app.theme_cls.primary_color)
        self.md_bg_color = list({
            primary_color : self.RED,
            self.RED      : primary_color,
        }[tuple(self.md_bg_color)])

        # Toggle icon
        self.icon = {
            "play" : "stop",
            "stop" : "play",
        }[self.icon]
