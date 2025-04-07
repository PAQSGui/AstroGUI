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
    QCheckBox,
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
    showSN:     bool

    snToggler : QCheckBox
    skyToggler : QCheckBox

    def __init__(self, model):
        self.layout = QVBoxLayout()
        self.model = model

        plotLayout = QHBoxLayout()

        self.lineThickness=0.5
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.bigFig.setMinimumSize(QSize(560, 560))

        self.templater = Templater(self)
        self.layout.addLayout(self.templater.layout)

        self.skyToggler = QCheckBox()
        self.snToggler = QCheckBox()
        self.skyToggler.stateChanged.connect(lambda:  self.PlotFile())
        self.snToggler.stateChanged.connect(lambda:  self.PlotFile())
       
        togglelayout = QHBoxLayout()
        togglelayout.addWidget(QLabel("Toggle Sky"))
        togglelayout.addWidget(self.skyToggler)
        togglelayout.addWidget(QLabel("Toggle S/N"))
        togglelayout.addWidget(self.snToggler)
        
        plotLayout.addWidget(self.bigFig)

        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.templater.layout.addLayout(togglelayout)
        self.l2_product = None

        self.showSN = False
        self.showSky = False

        self.update()


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
        try:
            self.UpdateFigure('k')
        except AttributeError as e:
            print("plotter.py def PlotFile AttributeError")  
            print(e)
            self.UpdateGrism()

        if l2_product != None:
            self.templater.plotTemplate(self.file, l2_product, firstLoad=first)
        plt.legend()
        self.bigFig.draw()

    def UpdateGrism(self, spectra=None):
        plt.figure('k')
        if spectra==None:
            spectra=self.file
        plt.clf() #clear figure
        colorcodes = ['k','r','g','b']
        for x in [0,1,2,3]:
            if spectra[x]!=None:
                self.DrawPlot(spectra[x],colorcodes[x])

        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key='k', file=None):
        if file==None:
            file=self.file
        plt.figure('k')
        plt.clf() #clear figure
        self.DrawPlot(file,key)
        plt.title(file.Objectname)  
        plt.title(self.file.Objectname)  

    def update(self):
        model = self.model
        data = Model.getState(model)
        file = data.file
        self.file = file
        plt.figure('k')
        plt.clf() #clear figure
        plt.step(self.file.Wavelength, self.file.Flux, color = 'k', linewidth=self.lineThickness) #figure key is used for color
        if self.showSN:
            plt.step(file.Wavelength, file.Flux/file.Noise, label="Signal / Noise", linewidth=0.5)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.file.Wavelength, self.file.Noise, label='Noise', color='0.5', linewidth=self.lineThickness)
        plt.title(self.file.Objectname) 

        self.templater.plotTemplate(self.file, data.fitting)

        plt.legend()
        self.bigFig.draw()

    def toggleSN(self):
        self.showSN = not self.showSN
        self.update()
        
    def DrawPlot(self,data,colorcode):
        plt.step(data.Wavelength, data.Flux, color = colorcode, linewidth=self.lineThickness) #figure key is used for color
        if self.snToggler.isChecked():
            plt.step(data.Wavelength, data.Flux/data.Noise, label="Signal / Noise",  alpha=0.25, linewidth=self.lineThickness)
        if self.skyToggler.isChecked():
            plt.step(data.Wavelength, data.Skybackground, label="Sky Background",  alpha=0.25, linewidth=self.lineThickness)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.ylim([0,np.max(data.Flux)])
        plt.step(data.Wavelength, data.Noise, label='Noise', color=colorcode, alpha=0.5, linewidth=self.lineThickness)
