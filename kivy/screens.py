import kivy.uix.screenmanager
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.properties import BooleanProperty

class Screen(kivy.uix.screenmanager.Screen):
    pass
    # def on_enter(self, *args):
    #     app = MDApp.get_running_app()
    #     # On start up, rail is not initialized yet before entering the first screen
    #     # Skip here and let the rail initialize the highlights in [on_start]
    #     if not app.has_run_build:
    #         return
    #     # Update the item highlights for this screen's icon, and deactivate the others
    #     # app.rail.update_item_highlights(self.name)

class HomeScreen(Screen):
    pass
class FlushScreen(Screen):
    on = BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress_bar = None
        self.update_interval = None
        self.num_seconds_left = 0
        self.original_duration = 0
        self.tick_duration = 0.01
        Clock.schedule_once(self._init)

    def _init(self, *args):
        self.progress_bar = self.ids.progress_bar.__self__
        self.slider = self.ids.slider.__self__
        self.ids.main_layout.remove_widget(self.progress_bar)

    def toggle(self):
        # Turn off
        if self.on:
            if self.update_interval:
                self.update_interval.cancel()
                self.update_interval = None
            self.ids.main_layout.remove_widget(self.progress_bar)
            self.ids.main_layout.add_widget(self.slider)
            # Reset the values
            self.slider.value = self.original_duration
            self.progress_bar.value = self.original_duration
            self.ids.duration_label.text = "Duration"
        # Turn on
        else:
            self.ids.main_layout.remove_widget(self.slider)
            self.ids.main_layout.add_widget(self.progress_bar)
            self.num_seconds_left = self.slider.value
            self.original_duration = self.slider.value
            self.update_interval = Clock.schedule_interval(self.countdown, self.tick_duration)
        self.on = not self.on

    def set_duration_text(self):
        minutes = int(self.num_seconds_left / 60)
        seconds = int(self.num_seconds_left % 60)
        self.ids.duration_label.text = f"{minutes:02}:{seconds:02}"

    def countdown(self, *args):
        self.num_seconds_left -= self.tick_duration
        self.set_duration_text()
        self.slider.value = self.num_seconds_left
        self.progress_bar.value = self.num_seconds_left
        if self.num_seconds_left <= 0:
            self.update_interval.cancel()
            self.update_interval = None
            self.toggle()
            self.ids.play_button.toggle()

class WaterScreen(Screen):
    pass
class BrewScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init)
    def init(self, *args):
        # print(self.children)
        pass

class SteamScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init)
    def init(self, *args):
        # print(self.children)
        pass

