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

        self.showSN = True
        self.showSky = True


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
                self.DrawPlot(spectra[x],colorcodes[x])

        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key, file=None):
        if file==None:
            file=self.file
        plt.figure('k')
        plt.clf() #clear figure
        self.DrawPlot(file,key)
        plt.title(file.Objectname)  

    def DrawPlot(self,data,colorcode):
        plt.step(data.Wavelength, data.Flux, color = colorcode, linewidth=self.lineThickness) #figure key is used for color
        if self.showSN:
            plt.step(data.Wavelength, data.Flux/data.Noise, label="Signal / Noise",  alpha=0.25, linewidth=self.lineThickness)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(data.Wavelength, data.Noise, label='Noise', color=colorcode, alpha=0.5, linewidth=self.lineThickness)

    def toggleSN(self):
        self.showSN = not self.showSN
        self.PlotFile()
    def toggleSky(self):
        self.showSky = not self.showSky
        self.PlotFile()
