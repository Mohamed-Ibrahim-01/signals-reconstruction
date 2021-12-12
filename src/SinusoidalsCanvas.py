import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg\
     import FigureCanvasQTAgg as FigureCanvas

class SinusoidalsCanvas(FigureCanvas):

    def __init__(self, width=5, height=100, dpi=100):

        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_axes(rect = (0.05,0.1,0.8,0.8))
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        super().__init__(self.fig)

        self.initGlobals()

        self.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event):
        legline = event.artist
        origline = self.lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)
        self.draw()

    def initGlobals(self):
        self.legend = None
        self.graphs = []
        self.lined = {}

    def updateLegend(self):
        self.legend = self.axes.legend(
            fancybox=True,
            shadow=True,
            bbox_to_anchor=(1.15, 1.13)
        )
        for legline, origline in zip(self.legend.get_lines(), self.graphs):
            legline.set_picker(True)
            self.lined[legline] = origline[0]

    def addGraph(self, new_sinusoidal):
        t, values = new_sinusoidal.time, new_sinusoidal.getValues()
        label = new_sinusoidal.getLabel()
        graph = self.axes.plot(t, values, label=label)
        self.graphs.append(graph)
        self.updateLegend()
        self.draw()

    def removeGraph(self, index):
        self.axes.lines.remove(self.axes.lines[index])
        self.graphs.remove(self.graphs[index])
        self.updateLegend()
        self.draw()

    def clearCanvas(self):
        self.initGlobals()
        self.axes.cla()
        self.draw()
