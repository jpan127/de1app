from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.navigationrail import MDNavigationRail
import kivy.uix.scrollview
import kivymd.uix.list

_ANIMATION_DURATION_S = 0.2

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

    def update_item_highlights(self, screen_name):
        for item in self.rail_items:
            if item.text != screen_name:
                item.visible = ""
            else:
                item.visible = "Selected"
            self.set_color_menu_item(item)

    def set_width(self, interval=None, minimized_width=50, maximized_width=None):
        """
        Sets the open/closed width of the rail

        interval: First paramter, to match the signature of the clock callbacks
        minimized_width: The width in pixels when the rail is minimized
        maximized_width: The width in pixels when the rail is maximized
        """
        self.size_hint_x = None
        self.width = dp(minimized_width)
        self.closed_width = dp(minimized_width)
        self.open_width = dp(maximized_width or minimized_width * 4)

    @property
    def rail_items(self):
        """
        Gets the nested rail items, that is nested 3 layers deep (self.children[0].children[0].children)
        """
        find_first = lambda it, t: next(filter(lambda x: isinstance(x, t), it), None)
        if not (children := self.children):
            return None
        if not (scroll_view := find_first(children, kivy.uix.scrollview.ScrollView)):
            return None
        if not (item_list := find_first(scroll_view.children, kivymd.uix.list.MDList)):
            return None
        return item_list.children

    def set_item_width(self, width):
        """
        Unfortunately the child rail items do not seem to change their size dynamically
        Therefore, this sets their width
        """
        for item in self.rail_items:
            item.size = (width, width)

    def open(self):
        def set_opacity_title_component(*args):
            if self.use_title:
                Animation(opacity=1, d=_ANIMATION_DURATION_S).start(
                    self.ids.box_title.children[0].ids.lbl_title
                )
                Animation(opacity=1, d=_ANIMATION_DURATION_S).start(
                    self.ids.box_title.children[0].ids.icon_settings
                )

        self.set_item_width(self.open_width)
        if self.use_resizeable:
            # print("open     ", hex(id(self)), self.width)
            # print("o", f"{self.width} => {self.open_width}")
            anim = Animation(width=self.open_width, d=_ANIMATION_DURATION_S) # Changed the width here
            anim.bind(on_complete=set_opacity_title_component)
            anim.start(self)
            # print("a\t", f"{self.width}")

            if self.floating_action_button:
                Animation(
                    _canvas_width=self.floating_action_button.width + dp(124),
                    _padding_right=dp(8),
                    _alpha=1,
                    d=_ANIMATION_DURATION_S,
                ).start(self.floating_action_button)
            self.dispatch("on_open")
        self.set_items_visible(None)

    def close(self):
        if self.use_resizeable:
            Clock.schedule_once(lambda _: self.set_item_width(self.closed_width), _ANIMATION_DURATION_S)
            Animation(width=self.closed_width, d=_ANIMATION_DURATION_S).start(self)  # Changed the width here
            if self.use_title:
                Animation(opacity=0, d=_ANIMATION_DURATION_S).start(
                    self.ids.box_title.children[0].ids.lbl_title
                )
                Animation(opacity=0, d=0.02).start(
                    self.ids.box_title.children[0].ids.icon_settings
                )
            if self.floating_action_button:
                Animation(
                    _canvas_width=0,
                    _padding_right=0,
                    d=_ANIMATION_DURATION_S,
                    _alpha=0,
                ).start(self.floating_action_button)
            self.dispatch("on_close")
