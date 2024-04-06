from common.structs.airport import Experiment
from build.ui import GUI
import matplotlib.pyplot as plt


N_RUNWAYS = 3

class App:
    def __init__(self, filepath: str, name: str, n_runways: int):
        self.ui = GUI(title=name, size=(960, 540), background='#E3E1E1', experiment=Experiment(filepath, name, n_runways))
        self.ui.run()

app = App('test.csv', 'test', N_RUNWAYS)
