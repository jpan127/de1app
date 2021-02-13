from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.navigationrail import MDNavigationRail

class NavigationRail(MDNavigationRail):
    def __init__(self, **kwargs):
        super(MDCard, self).__init__(**kwargs)
        self.floating_action_button = None
        self.elevation = 0

        self.register_event_type("on_action_button")
        self.register_event_type("on_item_switch")
        self.register_event_type("on_open")
        self.register_event_type("on_close")
        self.set_width() # Unscheduled this so it can be predictably reset after init

        Clock.schedule_once(self.set_items_visible)
        Clock.schedule_once(self.set_action_icon_button)
        Clock.schedule_once(self.set_action_text_button)
        Clock.schedule_once(self.set_box_title_size)
        Clock.schedule_once(self.set_action_color_button)
        Clock.schedule_once(self.set_items_color)

    def set_width(self, interval=None, width=50, factor=4):
        self.size_hint_x = None
        self.width = dp(width)
        self.closed_width = dp(width)
        self.open_width = self.closed_width * factor

    def on_item_switch(self, item):
        print(item.text)

    def open(self):
        def set_opacity_title_component(*args):
            if self.use_title:
                Animation(opacity=1, d=0.2).start(
                    self.ids.box_title.children[0].ids.lbl_title
                )
                Animation(opacity=1, d=0.2).start(
                    self.ids.box_title.children[0].ids.icon_settings
                )

        if self.use_resizeable:
            # print("open     ", hex(id(self)), self.width)
            # print("o", f"{self.width} => {self.open_width}")
            anim = Animation(width=self.open_width, d=0.2) # Changed the width here
            anim.bind(on_complete=set_opacity_title_component)
            anim.start(self)
            # print("a\t", f"{self.width}")

            if self.floating_action_button:
                Animation(
                    _canvas_width=self.floating_action_button.width + dp(124),
                    _padding_right=dp(8),
                    _alpha=1,
                    d=0.2,
                ).start(self.floating_action_button)
            self.dispatch("on_open")

    def close(self):
        if self.use_resizeable:
            # print("c", f"{self.width} => {self.closed_width}")
            Animation(width=self.closed_width, d=0.2).start(self)  # Changed the width here
            if self.use_title:
                Animation(opacity=0, d=0.2).start(
                    self.ids.box_title.children[0].ids.lbl_title
                )
                Animation(opacity=0, d=0.02).start(
                    self.ids.box_title.children[0].ids.icon_settings
                )
            if self.floating_action_button:
                Animation(
                    _canvas_width=0,
                    _padding_right=0,
                    d=0.2,
                    _alpha=0,
                ).start(self.floating_action_button)
            self.dispatch("on_close")