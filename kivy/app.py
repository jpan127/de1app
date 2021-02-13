
import kivy.uix.screenmanager
from kivymd.app import MDApp

import registration

class Application(MDApp):
    def __init__(self, **kwargs):
        # Flag for other widgets to understand when [build] has finished running or not
        # Lots of chances for widgets to invoke callbacks before then
        self.has_run_build = False
        super().__init__(**kwargs)

    @property
    def rail(self):
        """Helper for getting the rail instance"""
        return self.root.get_screen("Brew").ids.rail

    def build(self):
        """
        Main startup callback
        """
        root = kivy.uix.screenmanager.ScreenManager(
            transition=kivy.uix.screenmanager.FadeTransition())
        # After the screen manager is instantiated, build is "finished"
        self.has_run_build = True
        return root

    def on_start(self):
        """
        Callback after [build]
        """
        # Resize the rail to start closed and expand to 150 dp
        self.rail.set_width(minimized_width=0, maximized_width=150)

        # Highlight the right icon
        self.rail.update_item_highlights(self.root.current)

    def rail_open(self):
        """
        Toggle the rail state
        """
        self.rail.rail_state = {
            "open"  : "close",
            "close" : "open",
        }[self.rail.rail_state]

if __name__ == '__main__':
    Application().run()
