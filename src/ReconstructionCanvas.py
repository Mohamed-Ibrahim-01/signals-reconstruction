import matplotlib.gridspec as gridspec
import numpy as np
from scipy import signal
from scipy.constants import pi
from scipy.special import sinc
from matplotlib import pyplot as plt
plt.style.use('dark_background')

from matplotlib.backends.backend_qt5agg\
     import FigureCanvasQTAgg as FigureCanvas

class ReconstructionCanvas(FigureCanvas):

    def __init__(self, width=5, height=100, dpi=100):

        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = self.fig.add_subplot(211)
        self.axes2 = self.fig.add_subplot(212)
        self.grid = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.3)
        self.grid2 = gridspec.GridSpec(1, 1, height_ratios=[1])
        self.axes2_visible = True
        super().__init__(self.fig)

    def loadSignal(self, analog_time, signal_values):
        self.axes1.cla()
        self.drawContinuous(analog_time, signal_values, 'r-')
        self.draw()

    def drawRecovery(self, sampling_time, sampling_values, analog_time, recoverd_signal):
        self.drawContinuous(analog_time, recoverd_signal, 'y--')
        self.drawSamples(sampling_time, sampling_values)
        self.draw()

    def drawContinuous(self, time, signal, lineProps):
        if len(signal) > 0:
            self.axes1.plot(time, signal, lineProps)
        self.draw()

    def drawSamples(self, sampling_time, samples_values):
        if len(samples_values) > 0:
            self.axes1.scatter( sampling_time, samples_values)
        self.draw()

    def drawRecoveryOnly(self, analog_time, recoverd_signal):
        self.axes2.cla()
        if len(recoverd_signal) > 0:
            self.axes2.plot(analog_time, recoverd_signal, 'g-')
        self.draw()

    def clearCanvas(self):
        self.axes1.cla()
        self.axes2.cla()
        self.draw()

    def toggle_axes(self):
        self.axes2_visible = not self.axes2_visible
        self.axes2.set_visible(self.axes2_visible)
        if self.axes2_visible:
            self.axes1.set_position(self.grid[0].get_position(self.fig))
        else:
            self.axes1.set_position(self.grid2[0].get_position(self.fig))

        self.draw()

