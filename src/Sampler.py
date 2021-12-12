import numpy as np
import matplotlib
import librosa
import utils
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from scipy import signal
from scipy.constants import pi
from scipy.special import sinc
from ReconstructionCanvas import ReconstructionCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from scipy.constants import pi

matplotlib.use('Qt5Agg')

global PLOT_NUM_POINTS
PLOT_NUM_POINTS = 100000

class Sampler(qtw.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/sampler.ui", self)
        self.reconstruct_canvas = ReconstructionCanvas()
        self.toolbar = NavigationToolbar( self.reconstruct_canvas, self)

        self.main_reconstruct.addWidget(self.reconstruct_canvas)
        self.layout().insertWidget(0, self.toolbar)

        self.sampling_slider.valueChanged.connect(self.updateReconstruction)
        self.load_btn.clicked.connect(self.loadSignal)
        self.hide_secondary.clicked.connect(self.toggleSecondary)

        self.fmax = 0
        self.time_interval = 0
        self.analog_time = []
        self.originalSignal = []
        self.loaded = False

    def updateReconstruction(self):
        factor = self.sampling_slider.value()/4
        sampling_freq = factor * self.fmax
        self.sliderLabel.setText(f'{factor} fmax')
        self.reconstructSignal(self.originalSignal, self.analog_time, sampling_freq)

    def loadSignal(self):
        self.loaded, name, (self.analog_time, self.originalSignal) = utils.open_csv(self)
        if self.loaded:
            self.fmax = self.fmaxInput.value()
            self.time_interval = self.analog_time[-1]
            self.reconstruct_canvas.loadSignal(self.analog_time,self.originalSignal)

    def loadFromComposer(self, signal):

        if signal[0].any():
            self.analog_time, self.originalSignal, self.fmax = signal
            self.fmaxInput.setValue(self.fmax)
            self.time_interval = self.analog_time[-1]
            self.reconstruct_canvas.loadSignal(self.analog_time,self.originalSignal)
            self.loaded = True

    def toggleSecondary(self):
        self.reconstruct_canvas.toggle_axes()

    def reconstructSignal(self, originalSignal, analog_time, sampling_freq):
        if self.loaded:
            sampling_time, sampling_values = self.sample(
                originalSignal, sampling_freq, analog_time
            )
            if len(sampling_values) > 0:
                recoverd_signal = signal.resample(sampling_values, len(originalSignal))
                self.reconstruct_canvas.loadSignal(analog_time, originalSignal)
                self.reconstruct_canvas.drawRecovery(
                    sampling_time, sampling_values, analog_time, recoverd_signal
                )
                self.reconstruct_canvas.drawRecoveryOnly( analog_time, recoverd_signal)

    def sample(self, originalSignal, sampling_freq, analog_time):
        time_interval = analog_time[-1]
        nsamples = int(np.floor(sampling_freq * time_interval))
        if nsamples > 0:
            sampling_time = np.arange(0, time_interval, 1/sampling_freq)
            sampling_values = [ originalSignal[ np.searchsorted(analog_time, t)] for t in sampling_time ]
            return (sampling_time, sampling_values)
        return ([], [])

    def sinc_interpolation(self, samples_values,samples_time,sampling_rate):
        X, t, sr = samples_values, samples_time, sampling_rate
        nsamples = len(samples_values)
        y_reconstructed = [X[n] * sinc((t-n*sr)/sr) for n in range(nsamples)]
        y_reconstructed = np.sum(y_reconstructed, axis=0)
        return y_reconstructed

    def testSignal(self,sampling_time):
        return self.composedSignal(sampling_time, [3, 2, 4, 1, 13])
