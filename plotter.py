import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
import Spec_tools as tool
from templater import Templater
from Model import Model

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

    layout:     QVBoxLayout 
    file:       tool.SDSS_spectrum
    bigFig :    FigureCanvasQTAgg
    templater : Templater
    model:      Model

    def __init__(self, model):
        self.layout = QVBoxLayout()
        self.model = model

        plotLayout = QHBoxLayout()

        self.lineThickness=0.5
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.bigFig.setMinimumSize(QSize(560, 560))

        self.templater = Templater(self)
        self.layout.addLayout(self.templater.layout)
        print(type(self.bigFig))
        plotLayout.addWidget(self.bigFig)

        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.l2_product = None
        self.update()
        self.showSN = True

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
                plt.step(spectra[x].Wavelength, spectra[x].Flux, color = colorcodes[x], linewidth=self.lineThickness) #figure key is used for color
                plt.xlabel('Wavelength (Å)')
                plt.ylabel('Flux (erg/s/cm2/Å)')
                plt.step(spectra[x].Wavelength, spectra[x].Noise, label='Noise', color=colorcodes[x], alpha=0.5, linewidth=self.lineThickness)

        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key, file=None):
        if file==None:
            file=self.file
        plt.figure('k')
        plt.clf() #clear figure
        plt.step(file.Wavelength, file.Flux, color = key, linewidth=self.lineThickness) #figure key is used for color
        if self.showSN:
            plt.step(file.Wavelength, file.Flux/file.Noise, label="Signal / Noise", linewidth=0.5)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(file.Wavelength, file.Noise, label='Noise', color=key, alpha=0.5, linewidth=self.lineThickness)
        plt.title(file.Objectname)  

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

    def update(self):
        model = self.model
        data = Model.getState(model)
        self.file = data.file
        plt.figure('k')
        plt.clf() #clear figure
        plt.step(self.file.Wavelength, self.file.Flux, color = 'k', linewidth=self.lineThickness) #figure key is used for color
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.file.Wavelength, self.file.Noise, label='Noise', color='0.5', linewidth=self.lineThickness)
        plt.title(self.file.Objectname) 
        plt.legend()

        self.templater.plotTemplate(self.file, data.fitting)

        self.bigFig.draw()

    def toggleSN(self):
        self.showSN = not self.showSN
        self.UpdateFigure('k')
        self.PlotFile()
