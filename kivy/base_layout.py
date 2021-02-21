from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import CircularRippleBehavior, HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

Builder.load_string(
    """
<BaseLayout>:
    orientation: "vertical"
    MDToolbar:
        title: "Decent Espresso"
        md_bg_color: rail.md_bg_color
        left_action_items: [["menu", lambda x: app.rail_open()]]
    MDBoxLayout:
        orientation: "horizontal"
        NavigationRail:
            id: rail
            md_bg_color: get_color_from_hex("#344954")
            color_normal: get_color_from_hex("#718089")
            color_active: get_color_from_hex("#f3ab44")
            use_resizeable: True
            _no_ripple_effect: True
            text_title: ""
            MDNavigationRailItem:
                icon: "coffee"
                text: "Brew"
            MDNavigationRailItem:
                icon: "kettle-steam"
                text: "Steam"
            MDNavigationRailItem:
                icon: "cup-water"
                text: "Water"
            MDNavigationRailItem:
                icon: "water"
                text: "Flush"
        ScreenManager:
            id: screen_manager
""")

# class BrewLayout(MDBoxLayout):

# class SteamLayout(MDBoxLayout):


class BaseLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init)
    def init(self, *args):
        # self.ids.rail.add_widget()
        pass
