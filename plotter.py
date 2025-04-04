import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
import Spec_tools as tool
from templater import Templater

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QSlider,
    QLabel,
    QWidget,
    )
from PySide6.QtGui import (
    Qt,
)

from PySide6.QtCore import QSize

class Plotter:

    layout: QVBoxLayout 
    file: tool.SDSS_spectrum
    bigFig : FigureCanvasQTAgg
    templater : Templater

    def __init__(self):
        self.layout = QVBoxLayout()


        plotLayout = QHBoxLayout()

        self.lineThickness=0.5
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.bigFig.setMinimumSize(QSize(560, 560))

        self.templater = Templater(self)
        self.layout.addLayout(self.templater.layout)
        
        plotLayout.addWidget(self.bigFig)
        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.l2_product = None

    def optionsWindow(self):
        self.optsWindow = QWidget()
        self.optsLayout = QVBoxLayout()
        self.optsLayout.addWidget(QLabel("Plot Line Thickness"))
        self.thickSlider=QSlider(Qt.Orientation.Horizontal)
        self.thickSlider.setRange(1,15) #slider only takes integers
        self.thickSlider.setSingleStep(1)
        self.thickSlider.setValue(int(self.lineThickness*10))
        self.thickSlider.valueChanged.connect(lambda: self.setThickness(self.thickSlider.value()))
        self.optsLayout.addWidget(self.thickSlider)
        self.optsWindow.setLayout(self.optsLayout)
        self.optsWindow.show()

    def setThickness(self, newValue):
        self.lineThickness=float(newValue)/10.0
        self.PlotFile()

    def addFile(self, file, l2_product = None):
        self.file = file
        self.l2_product = l2_product
        self.PlotFile()

    def PlotFile(self, l2 = None, first = True):
        if l2 == None:
            l2_product = self.l2_product
        else:
            l2_product = l2

        visrange = np.linspace(3800, 7500, 4)

        self.UpdateFigure('k')

        if l2_product != None:
            self.templater.plotTemplate(self.file, l2_product, firstLoad=first)
        plt.legend()
        self.bigFig.draw()

    def UpdateGrism(self, spectra):
        plt.figure('k')
        plt.clf() #clear figure
        colorcodes = ['k','r','g','b']
        for x in [0,1,2,3]:
            if spectra[x]!=None:
                plt.step(spectra[x].Wavelength, spectra[x].Flux, color = colorcodes[x], linewidth=self.lineThickness) #figure key is used for color
                plt.xlabel('Wavelength (Å)')
                plt.ylabel('Flux (erg/s/cm2/Å)')
                plt.step(spectra[x].Wavelength, spectra[x].Noise, label='Noise', color=colorcodes[x], alpha=0.5, linewidth=self.lineThickness)

        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key, limitPlot = False, range = [6250, 7400], file=None):
        if file==None:
            file=self.file
        plt.figure('k')
        plt.clf() #clear figure
        plt.step(file.Wavelength, file.Flux, color = key, linewidth=self.lineThickness) #figure key is used for color
        plt.step(file.Wavelength, file.Flux/file.Noise, label="Signal / Noise", linewidth=0.5)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(file.Wavelength, file.Noise, label='Noise', color=key, alpha=0.5, linewidth=self.lineThickness)

        if limitPlot:
            plt.xlim(range)
        else: 
            plt.title(file.Objectname)  

    # def ShowSN(file):
    #     fig = plt.figure()
    #     plt.step(file.Wavelength, file.Flux/file.Noise, linewidth=0.5)
    #     plt.xlabel('Wavelength (Å)')
    #     plt.ylabel('Flux/Noise Ratio')
    #     plt.title(file.Objectname+"S/N Spectrum")
    #     canv=FigureCanvasQTAgg(fig)
    #     canv.show()
