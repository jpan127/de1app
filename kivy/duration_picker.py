import datetime

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import OptionProperty, ListProperty, StringProperty, ColorProperty, BooleanProperty, ObjectProperty
from kivymd.uix.picker import CircularSelector, TimeInput, MDTimePicker, TimeInputTextField, AmPmSelector
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivymd.uix.relativelayout import MDRelativeLayout

Builder.load_string(
    """
<TimeCircularSelector>:
    selector_size: dp(30)

<MinuteTimeInput>
    size_hint: None, None
    _minute: minute
    _second: second

    MinuteTimeInputTextField:
        id: minute
        num_type: "minute"
        pos: 0, 0
        text_color: root.text_color
        disabled: root.disabled
        on_text: root.dispatch("on_time_input")
        radius: root.minute_radius
        on_select:
            root.dispatch("on_minute_select")
            root.state = "minute"
        fill_color:
            [*root.bg_color_active[:3], 0.5] \
            if root.state == "minute" else [*root.bg_color[:3], 0.5]

    MDLabel:
        text: ":"
        size_hint: None, None
        size: dp(24), dp(80)
        halign: "center"
        valign: "center"
        font_size: dp(50)
        pos: dp(96), 0
        theme_text_color: "Custom"
        text_color: root.text_color

    MinuteTimeInputTextField:
        id: second
        num_type: "second"
        pos: dp(120), 0
        text_color: root.text_color
        disabled: root.disabled
        on_text: root.dispatch("on_time_input")
        radius: root.second_radius
        on_select:
            root.dispatch("on_second_select")
            root.state = "second"
        fill_color:
            [*root.bg_color_active[:3], 0.5] \
            if root.state == "second" else [*root.bg_color[:3], 0.5]

<DurationPicker>
    auto_dismiss: True
    size_hint: None, None
    _time_input: _time_input
    _selector: _selector
    _minute_label: _minute_label
    _second_label: _second_label

    MDRelativeLayout:
        id: custom_layout
        canvas.before:
            Color:
                rgba:
                    root.primary_color \
                    if root.primary_color \
                    else root.theme_cls.bg_normal

            RoundedRectangle:
                size: self.size
                radius: root.radius

        MDLabel:
            id: label_title
            font_style: "Body2"
            bold: True
            theme_text_color: "Custom"
            size_hint_x: None
            width: root.width
            adaptive_height: True
            text: root.title
            font_name: root.font_name
            pos: (dp(24), root.height - self.height - dp(18))
            text_color:
                root.text_toolbar_color if root.text_toolbar_color \
                else root.theme_cls.text_color

        MinuteTimeInput:
            id: _time_input
            bg_color:
                root.accent_color if root.accent_color else \
                root.theme_cls.primary_light
            bg_color_active:
                root.selector_color if root.selector_color \
                else root.theme_cls.primary_color
            text_color:
                root.input_field_text_color if root.input_field_text_color else \
                root.theme_cls.text_color
            on_time_input: root._get_time_input(*self.get_time())
            on_minute_select:
                _selector.switch_mode("minute")
            on_second_select:
                _selector.switch_mode("second")
            minute_radius: root.minute_radius
            second_radius: root.second_radius

        TimeInputLabel:
            id: _minute_label
            text: "Minute"
            opacity: 0
            text_color:
                root.text_toolbar_color if root.text_toolbar_color else \
                root.theme_cls.secondary_text_color

        TimeInputLabel:
            id: _second_label
            text: "Second"
            opacity: 0
            text_color:
                root.text_toolbar_color if root.text_toolbar_color else \
                root.theme_cls.secondary_text_color

        TimeCircularSelector:
            id: _selector
            text_color:
                root.text_color if root.text_color else \
                root.theme_cls.text_color
            bg_color:
                root.accent_color if root.accent_color else \
                root.theme_cls.primary_light
            selector_color:
                root.selector_color if root.selector_color else \
                root.theme_cls.primary_color
            font_name: root.font_name
            on_selector_change: root._get_dial_time(_selector)

        MDIconButton:
            id: input_clock_switch
            icon: "keyboard"
            pos: dp(12), dp(8)
            theme_text_color: "Custom"
            user_font_size: "24dp"
            on_release: root._switch_input()
            text_color:
                root.text_toolbar_color if root.text_toolbar_color else \
                root.theme_cls.secondary_text_color

        MDFlatButton:
            id: cancel_button
            text: "CANCEL"
            on_release: root.dispatch("on_cancel", None)
            theme_text_color: "Custom"
            pos: root.width - self.width - ok_button.width - dp(10), dp(10)
            font_name: root.font_name
            text_color:
                root.theme_cls.primary_color \
                if not root.text_button_color else root.text_button_color

        MDFlatButton:
            id: ok_button
            width: dp(32)
            pos: root.width - self.width, dp(10)
            text: "OK"
            theme_text_color: "Custom"
            font_name: root.font_name
            text_color:
                root.theme_cls.primary_color \
                if not root.text_button_color else root.text_button_color
            on_release: root.dispatch("on_save", root._get_data())
""", filename="custom_picker.kv")

class MinuteTimeInputTextField(TimeInputTextField):
    num_type = OptionProperty("minute", options=["minute", "second"])

class MinuteTimeInput(MDRelativeLayout, EventDispatcher):
    bg_color = ColorProperty()
    bg_color_active = ColorProperty()
    text_color = ColorProperty()
    disabled = BooleanProperty(True)
    minute_radius = ListProperty([0, 0, 0, 0])
    second_radius = ListProperty([0, 0, 0, 0])
    state = StringProperty("minute")
    _minute = ObjectProperty()
    _second = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_time_input")
        self.register_event_type("on_minute_select")
        self.register_event_type("on_second_select")

    def set_time(self, time_list):
        minute, second = time_list
        self._minute.text = minute
        self._second.text = second

    def get_time(self):
        minute = self._minute.text.strip()
        second = self._second.text.strip()
        return [minute, second]

    def _update_padding(self, *args):
        self._minute.on_text()
        self._second.on_text()

    def on_time_input(self, *args):
        pass

    def on_minute_select(self, *args):
        pass

    def on_second_select(self, *args):
        pass

class TimeCircularSelector(CircularSelector):
    selected_second = StringProperty("0")
    mode = OptionProperty("minute", options=["minute", "second"])

    def __init__(self, **kwargs):
        print("child")
        super().__init__(**kwargs)
        self.switch_mode("minute")
        self.bind(
            selected_second=self.update_time,
        )
        Clock.schedule_interval(self.foobar, 1.)

    def foobar(self, *args):
        pass
        # print(self.selected_second)
        # if (int(self.selected_second) > 0):
        #     self.set_time(str(int(self.selected_second) - 1))

    def set_time(self, selected):
        if self.mode != "second":
            super().set_time(selected)
            return
        self.selected_second = selected
    def update_time(self, *args):
        if self.mode != "second":
            super().update_time(*args)
            return
        self.set_selector(self.selected_second)

    def _update_labels(self, animate=True, *args):
        if self.mode != "second":
            super()._update_labels(animate, *args)
            return
        param = (0, 59, 5)
        self.degree_spacing = 6
        self.start_from = 90

        if animate:
            anim = Animation(content_scale=0, t=self.t, d=self.d)
            anim.bind(on_complete=lambda *args: self._add_items(*param))
            anim.start(self)
        else:
            self._add_items(*param)

class DurationPicker(MDTimePicker):
    # Radius of the minute input field.
    second_radius = ListProperty([dp(5)])
    second = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_time(datetime.time(minute=0, second=1))
        # Clock.schedule_once(self.init)

    def init(self, *args):
        # Remove MDTimePicker's layout
        for c in self.children:
            if c != self.ids.custom_layout:
                self.remove_widget(c)

    def _set_am_pm(self, selected):
        pass

    def _set_dial_time(self, minute, second):
        self._selector.selected_second = second
        self._selector.selected_minute = minute

    def _set_time_input(self, minute, second):
        minute = f"{int(minute):02d}"
        second = f"{int(second):02d}"
        if self._state != "input":
            self._time_input.set_time([minute, second])

    def _get_time_input(self, minute, second):
        if minute:
            self.minute = f"{int(minute):01d}"
        if second:
            self.second = f"{int(second):01d}"
        self._set_dial_time(self.minute, self.second)

    def _get_dial_time(self, instance):
        mode = instance.mode
        if mode == "second":
            self.second = instance.selected_second
        elif mode == "minute":
            self.minute = instance.selected_minute
        else:
            return
        self._set_time_input(self.minute, self.second)
