import numpy as np
import json
import matplotlib
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from Sinusoidal import Sinusoidal
from SinusoidalsCanvas import SinusoidalsCanvas
from ComposingCanvas import ComposingCanvas

matplotlib.use('Qt5Agg')

global PLOT_NUM_POINTS
PLOT_NUM_POINTS = 100000

class Composer(qtw.QWidget):

    samplingStarted = qtc.pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/composer.ui", self)
        self.initGlobals()

        self.sinusoidals_layout = self.findChild( qtw.QVBoxLayout, "sinusoidals_area")
        self.composing_layout = self.findChild( qtw.QVBoxLayout, "composing_area")
        self.component_list = self.findChild( qtw.QComboBox, "componentList")

        self.sinusoidals_canvas = SinusoidalsCanvas()
        self.composing_canvas = ComposingCanvas()

        self.composing_layout.addWidget(self.composing_canvas)
        self.sinusoidals_layout.addWidget(self.sinusoidals_canvas)

        self.connectActions()
        self.loadExamples()

    def connectActions(self):
        self.saveExampleBtn.clicked.connect(self.saveExample)
        self.examplesMenu.currentIndexChanged.connect(self.loadCurrExample)
        self.addComponentBtn.clicked.connect(self.addComponent)
        self.deleteComponentBtn.clicked.connect(self.removeComponent)
        self.startSamplingBtn.clicked.connect(self.startSampling)

    def initGlobals(self):
        self.time = np.linspace(0, 4, PLOT_NUM_POINTS)
        self.sinusoidals = []
        self.f_max = 0
        self.composed_signal = []
        self.num_examples = 0
        self.examples = {}

    def loadExamples(self):
        with open('data/examples.json') as file:
          self.examples = json.load(file)
          self.num_examples = len(self.examples.keys())
          for key in sorted(self.examples.keys()):
              self.examplesMenu.addItem(key)

    def loadCurrExample(self):
        self.clearAll()
        curr_example = self.examplesMenu.currentText()
        for component_key in self.examples[curr_example]:
            component = self.examples[curr_example][component_key]
            self.newComponent(**component)

    def saveExample(self):
        example = {}
        for sinusoidal in self.sinusoidals:
            example[sinusoidal.getLabel()] = sinusoidal.getDict()
        key = f"example_{self.num_examples+1}"
        self.examples[key] = example
        with open('data/examples.json', 'w', encoding='utf-8') as file:
            json.dump(self.examples, file, ensure_ascii=False, indent=4)
        self.clearAll()
        self.examplesMenu.addItem(key)

    def updateComposedGraph(self):
        _, self.composed_signal = self.composeSignals()
        self.composing_canvas.constructComposedSignal(self.time, self.composed_signal)

    def composeSignals(self):
        signalComponents = [sinusoidal.getValues() for sinusoidal in self.sinusoidals]
        self.composed_signal = np.sum(signalComponents, axis=0)
        return (self.time, self.composed_signal)

    def startSampling(self):
        self.samplingStarted.emit((self.time, self.composed_signal, self.getFmax()))

    def getFmax(self):
        frequncies = [sinusoidal.frequency for sinusoidal in self.sinusoidals]
        return max(frequncies) if len(frequncies) > 0 else 0

    def addComponent(self):
        amplitude, frequency, phase = self.getSinusoidalParameters()
        self.newComponent(frequency=frequency, amplitude=amplitude, phase=phase)

    def newComponent(self, frequency=1, amplitude=1, phase=0):
        new_sinusoidal = Sinusoidal(self.time, amplitude, frequency, phase)
        self.sinusoidals.append(new_sinusoidal)
        self.sinusoidals_canvas.addGraph(new_sinusoidal)
        self.component_list.addItem(new_sinusoidal.getLabel())
        self.updateComposedGraph()

    def removeComponent(self):
        if len(self.sinusoidals) > 0:
            curr_index = self.component_list.currentIndex()
            self.component_list.removeItem(curr_index)
            self.sinusoidals.remove(self.sinusoidals[curr_index])
            self.sinusoidals_canvas.removeGraph(curr_index)
            self.updateComposedGraph()
            if len(self.sinusoidals) == 0: self.sinusoidals_canvas.clearCanvas()
        else : self.sinusoidals_canvas.clearCanvas()

    def getSinusoidalParameters(self):
        amplitude = self.amplitude_input.value()
        frequency = self.frequency_input.value()
        phase = self.phase_input.value()
        return (amplitude, frequency, phase)

    def clearAll(self):
        self.sinusoidals = []
        self.f_max = 0
        self.composed_signal = []
        self.sinusoidals_canvas.clearCanvas()
        self.component_list.clear()
