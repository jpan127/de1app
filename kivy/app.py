import random

from kivy.lang import Builder
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import kivy.uix.screenmanager
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.factory import Factory
from kivy.metrics import dp

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

# Register custom elements
from kivy.factory import Factory
r = Factory.register
r("NavigationRail", module="navigation_rail")
r("PlayButton", module="play_button")

class GraphLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n = 1
        self.graphs = [self.make_graph() for _ in range(3)]
        for graph in self.graphs:
            self.add_widget(graph)
        self.update_interval = Clock.schedule_interval(self.update, 1 / 5)

    def toggle(self):
        if self.update_interval is not None:
            self.update_interval.cancel()
            self.update_interval = None
        else:
            self.update_interval = Clock.schedule_interval(self.update, 1 / 5)

    def make_graph(self):
        # @TODO: Move out
        import math
        graph = Graph(
            xlabel='X', ylabel='Y', x_ticks_minor=5,
            x_ticks_major=25, y_ticks_major=1,
            y_grid_label=True, x_grid_label=True, padding=5,
            x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=-1, ymax=10)
        graph.background_color=[1, 1, 1, 1]
        plot = MeshLinePlot(color=[0.1, 0.1, 1, 1])
        plot.points = [(0, random.random() % 10)]
        graph.add_plot(plot)
        return graph

    def update(self, *args):
        self.n += 1
        for graph in self.graphs:
            graph.plots[0].points.append((self.n, random.randint(0, 10)))
            graph.xmax = max(graph.xmax, self.n)
            graph.ymax = max(graph.ymax, max(graph.plots[0].points, key=lambda xy: xy[1])[1])

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
