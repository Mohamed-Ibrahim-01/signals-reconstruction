import numpy as np
class Sinusoidal:
    def __init__(self,time=[], amplitude=1, frequency=1, phase=0, kind="SIN"):
        self.time = time
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.kind = kind
        self.sinusoidal_values = []

    def makeSinusoidal(self):
        t, a, f, p = self.time, self.amplitude, self.frequency, self.phase
        if(self.kind == "SIN") : self.sinusoidal_values = a*np.sin(2*np.pi*(f*t) + p)
        else : self.sinusoidal_values = a*np.cos(2*np.pi*(f*t) + p)
        return self.sinusoidal_values

    def getValues(self):
        if not self.time.any(): return []
        self.makeSinusoidal()
        return self.sinusoidal_values

    def getLabel(self):
        return f'{self.amplitude}@{self.frequency} HZ + {self.phase}'

    def getDict(self):
        return {
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase
        }
