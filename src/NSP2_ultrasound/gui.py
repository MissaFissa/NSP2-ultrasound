import sys
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QAction
import matplotlib.pyplot as plt
from nsp2_ultrasound.model import UltrasonicExperiment
from nsp2_ultrasound.ui_app import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib import cm
from matplotlib.ticker import LinearLocator

class UserInterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.vbox.addWidget(self.ui.canvas)

        self.toolbar = NavigationToolbar2QT(self.ui.canvas)

        self.ui.vbox.addWidget(self.toolbar)

        self.ui.start.setPlaceholderText("set start value")
      
        self.ui.stop.setPlaceholderText("set stop value")

        self.ui.name.setPlaceholderText("name of file")

        self.ui.plot_button.clicked.connect(self.plot_func)

        self.filemenu = self.ui.menubar.addMenu("File")

        self.saveAction = QAction("Save", self)

        self.saveAction.setShortcut("Ctrl+S")

        self.filemenu.addAction(self.saveAction)

        self.saveAction.triggered.connect(self.save)

        start_value = self.ui.start.text() or "60"
        stop_value = self.ui.stop.text() or "170"
        name_value = self.ui.name.currentText()

        self.experiment = UltrasonicExperiment(start_value, stop_value)

        self.experiment.scan(name_value)

    def save(self):

        filepath, _ = QFileDialog.getSaveFileName(self.ui.canvas, "Save Image", "/Users/meesh/Documents/GitHub/NSP2-ultrasound/images", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    
        if filepath:

            self.ui.canvas.figure.savefig(filepath)
        
        if filepath == "":

            return

        return filepath

    def plot_func(self):

        self.ui.figure.clear()
        plt.rcParams['font.family'] = 'sans-serif'
        # c = plt.pcolormesh(self.experiment.positions_cm, self.experiment.depths, np.array(self.experiment.amplitude_envelope_all).T, shading = 'gouraud', cmap = "inferno", antialiased = False)
        c = plt.pcolormesh(self.experiment.positions_cm, self.experiment.depths_water, np.array(self.experiment.amplitude_envelope_all_water).T, shading = 'gouraud', cmap = "inferno", antialiased = False)
        plt.colorbar(c)
        plt.title("Empty fish tank", fontsize = 13)
        plt.xlabel('Lateral direction (cm)', fontsize = 13)
        plt.ylabel('Axial direction (cm)', fontsize = 13)
        plt.tight_layout()

        self.ui.canvas.draw()

def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.plot_func()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()