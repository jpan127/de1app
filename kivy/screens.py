import kivy.uix.screenmanager
from kivymd.app import MDApp

class Screen(kivy.uix.screenmanager.Screen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        # On start up, rail is not initialized yet before entering the first screen
        # Skip here and let the rail initialize the highlights in [on_start]
        if not app.has_run_build:
            return
        # Update the item highlights for this screen's icon, and deactivate the others
        app.rail.update_item_highlights(self.name)

class HomeScreen(Screen):
    pass
class BrewScreen(Screen):
    pass
class SteamScreen(Screen):
    pass
