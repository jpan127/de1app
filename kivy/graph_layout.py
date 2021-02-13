import math
import random

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy_garden.graph import Graph, MeshLinePlot
from kivymd.uix.boxlayout import MDBoxLayout

def _make_graph():
    graph = Graph(
        xlabel='X',
        ylabel='Y',
        x_ticks_minor=5,
        x_ticks_major=25,
        y_ticks_major=1,
        y_grid_label=True,
        x_grid_label=True,
        padding=5,
        x_grid=True,
        y_grid=True,
        xmin=0,
        xmax=100,
        ymin=-1,
        ymax=10)
    graph.background_color=[1, 1, 1, 1]
    plot = MeshLinePlot(color=[0.1, 0.1, 1, 1])
    plot.points = [(0, random.random() % 10)]
    graph.add_plot(plot)
    return graph

class GraphLayout(MDBoxLayout):
    num_graphs = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init)
        self.update_interval = Clock.schedule_interval(self.update, 1 / 5)

    def init(self, *args):
        self.n = 1
        self.graphs = [_make_graph() for _ in range(self.num_graphs)]
        for graph in self.graphs:
            self.add_widget(graph)

    def toggle(self):
        if self.update_interval is not None:
            self.update_interval.cancel()
            self.update_interval = None
        else:
            self.update_interval = Clock.schedule_interval(self.update, 1 / 5)

    def update(self, *args):
        self.n += 1
        for graph in self.graphs:
            graph.plots[0].points.append((self.n, random.randint(0, 10)))
            graph.xmax = max(graph.xmax, self.n)
            graph.ymax = max(graph.ymax, max(graph.plots[0].points, key=lambda xy: xy[1])[1])
