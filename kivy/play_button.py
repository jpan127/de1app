from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import BooleanProperty
from kivymd.color_definitions import colors, hue, palette
from kivymd.uix.button import MDFloatingActionButton
from kivymd.app import MDApp

class PlayButton(MDFloatingActionButton):
    """
    A button that toggles color + icon when clicked
    """
    RED = tuple(get_color_from_hex(colors["Red"]["A700"]))
    on = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._no_ripple_effect = True
        Clock.schedule_once(self.init)

    @property
    def primary_color(self):
        app = MDApp.get_running_app()
        return tuple(app.theme_cls.primary_color)

    def init(self, *args):
        self.icon = "play"
        self.md_bg_color = self.primary_color
        if self.on:
            self.toggle()

    def toggle(self):
        # Toggle color
        self.md_bg_color = list({
            self.primary_color : self.RED,
            self.RED           : self.primary_color,
        }[tuple(self.md_bg_color)])

        # Toggle icon
        self.icon = {
            "play" : "stop",
            "stop" : "play",
        }[self.icon]
