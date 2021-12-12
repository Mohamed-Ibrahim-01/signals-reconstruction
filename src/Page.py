from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from Composer import Composer
from Sampler import Sampler


class Page(qtw.QTabWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("src/ui/page.ui", self)
        self.initGlobals()
        self.initBody()

    def initGlobals(self):
        pass

    def initBody(self):
        self.composer_tab = self.findChild(qtw.QWidget, "composer")
        self.sampler_tab = self.findChild(qtw.QWidget, "sampler")

        self.composer = Composer()
        self.sampler = Sampler()

        self.composer_tab.layout().addWidget(self.composer)
        self.sampler_tab.layout().addWidget(self.sampler)

        self.composer.samplingStarted.connect(self.sampleFromComposer)

    def sampleFromComposer(self, signal):
        self.setCurrentWidget(self.sampler_tab)
        self.sampler.loadFromComposer(signal)
