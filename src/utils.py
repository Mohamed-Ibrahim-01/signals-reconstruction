import pandas as pd
import os
from PyQt5 import QtWidgets as qtw
import numpy as np


def is_csv(path):
    file_name = path.split(os.path.sep)[-1]
    return file_name.find(".csv") != -1


def open_csv(window):
    path, _ = qtw.QFileDialog.getOpenFileName(window, 'Open File')
    return load_csv(path)


def load_csv(path):
    name = path.split(os.path.sep)[-1]
    if name and name.__contains__('.csv'):
        loaded_data = pd.read_csv(path)
        time = loaded_data['time'].to_numpy()
        values = loaded_data['values'].to_numpy()
        return (True, name, (time, values))
    else:
        return (False, None, (None, None))