import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
import Spec_tools as tool
import templater

from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QLabel,
    QWidget,
    QMainWindow,
    )
from PySide6.QtGui import (
    Qt,
)

class Plotter:

    layout: QHBoxLayout 
    file: tool.SDSS_spectrum
    bigFig : FigureCanvasQTAgg

    def __init__(self):
        self.layout = QHBoxLayout()
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.layout.addWidget(self.bigFig)
        self.lineThickness=0.5

    def optionsWindow(self):
        optsLayout = QVBoxLayout()
        optsLayout.addWidget(QLabel("Plot Line Thickness"))
        thickSlider=QSlider(Qt.Orientation.Horizontal)
        thickSlider.setRange(1,15) #slider only takes integers
        thickSlider.setSingleStep(1)
        thickSlider.setValue(int(self.lineThickness*10))
        thickSlider.valueChanged.connect(lambda: self.setThickness(thickSlider.value()))
        optsLayout.addWidget(thickSlider)
        thickSlider.show()

    def setThickness(self,newValue):
        self.lineThickness=float(newValue)/10.0

    def addFile(self, file, l2_product):
        self.file = file
        self.PlotFile(l2_product)

    def PlotFile(self, l2_product = None):

        visrange = np.linspace(3800, 7500, 4)

        self.UpdateFigure('k')
        #self.UpdateFigure(self.file,'b', limitPlot = True, range = [visrange[0], visrange[1]])
        #self.UpdateFigure(self.file,'g', limitPlot = True, range = [visrange[1], visrange[2]])
        #self.UpdateFigure(self.file,'r', limitPlot = True, range = [visrange[2], visrange[3]])

        if l2_product != None:
            templater.plotTemplate(self.file,l2_product)
        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key, limitPlot = False, range = [6250, 7400]):
        plt.figure(key)
        plt.clf() #clear figure
        plt.step(self.file.Wavelength, self.file.Flux, color = key, linewidth=self.lineThickness) #figure key is used for color
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.file.Wavelength, self.file.Noise, label='Noise', color='0.5', linewidth=self.lineThickness)

        if limitPlot:
            plt.xlim(range)
        else: 
            plt.title(self.file.Objectname)  

    def ShowSN(file):
        fig = plt.figure()
        plt.step(file.Wavelength, file.Flux/file.Noise, linewidth=0.5)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux/Noise Ratio')
        plt.title(file.Objectname+"S/N Spectrum")
        canv=FigureCanvasQTAgg(fig)
        canv.show()
