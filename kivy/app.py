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

class HomeScreen(kivy.uix.screenmanager.Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def switch_to_brew(self):
        self.manager.current = "brew"

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

class BrewScreen(kivy.uix.screenmanager.Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def switch_to_home(self):
        self.manager.current = "home"

class MyScreenManager(kivy.uix.screenmanager.ScreenManager):
    pass

class Application(MDApp):
    @property
    def rail(self):
        return self.root.get_screen("brew").ids.rail
    def build(self):
        return MyScreenManager()
    def on_start(self):
        self.rail.set_width(width=75, factor=2)
    def rail_open(self):
        TRANSITIONS = {
            "open": "close",
            "close": "open",
        }
        self.rail.rail_state = TRANSITIONS[self.rail.rail_state]

if __name__ == '__main__':
    Application().run()
