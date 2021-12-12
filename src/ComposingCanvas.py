import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from matplotlib.backends.backend_qt5agg\
     import FigureCanvasQTAgg as FigureCanvas

class ComposingCanvas(FigureCanvas):

    def __init__(self, width=5, height=100, dpi=100):

        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_axes(rect = (0.05,0.1,0.8,0.8))
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        super().__init__(self.fig)

        self.initGlobals()
        self.initSetters()

    def initGlobals(self):
        self.composed_signal = []
        self.time = []
        pass

    def initSetters(self):
        pass

    def constructComposedSignal(self, time, composed_signal):
        self.axes.cla()
        self.time = time
        self.composed_signal = composed_signal
        if composed_signal.any():
            self.axes.plot(self.time, self.composed_signal)
        self.draw()

    def clearCanvas(self):
        self.axes.cla()
        self.draw()
