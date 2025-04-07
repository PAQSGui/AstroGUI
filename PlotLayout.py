import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
from templater import Templater
from Model import Model

from plotter import Plotter

from PySide6.QtWidgets import (
    QLayout,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel,
    QComboBox,
    )

from PySide6.QtGui import (
    Qt,
)

from PySide6.QtCore import QSize
from xpca import config
#https://www.geeksforgeeks.org/list-all-files-of-certain-type-in-a-directory-using-python/
from os import listdir
import re

class PlotLayout:
    layout: QHBoxLayout
    model: Model
    plotter: Plotter
    showSN = True

    def __init__(self, model):
        self.model = model
        self.layout = QVBoxLayout()

        plotLayout = QHBoxLayout()

        self.lineThickness=0.5
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.bigFig.setMinimumSize(QSize(560, 560))

        self.templater = Templater()
        self.layout.addLayout(self.templater.layout)
        plotLayout.addWidget(self.bigFig)

        self.zSlider = QSlider(Qt.Orientation.Horizontal)
        self.zSlider.setSingleStep(1)
        self.zSlider.sliderMoved.connect(self.slider_changed)
        self.zSlider.sliderReleased.connect(self.sliderrelease)
        self.layout.addWidget(self.zSlider)
        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)
        self.layout.addWidget(self.dropdown)

        self.dropdown.textActivated.connect(self.text_changed)

        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.l2_product = None
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

    def sliderrelease(self):
        self.l2_current['zBest']=float(self.zSlider.value())/100
        self.setMiddle(self.l2_current)
        self.plotter.PlotFile(self.l2_current)
        
    def setMiddle(self,l2_product):
        newMiddle = l2_product['zBest']*100
        self.zSlider.setMinimum(newMiddle-100)
        self.zSlider.setMaximum(newMiddle+100)
        self.zSlider.setValue(newMiddle)
    
    def slider_changed(self,s):
        self.l2_current['zBest']=float(self.zSlider.value())/100

        self.plotter.PlotFile(self.l2_current, first = False)

    def text_changed(self, s):

        result = re.search(f'template-(.+).fits', s)
        self.l2_current['zBestSubType']=result.group(1)
        
        try:
            self.plotter.PlotFile(self.l2_current)
        except FileNotFoundError as e:
            print("templater.py def text_changed FileNotFoundError")  
            print(e)
            for file in listdir(config.TEMPLATE_PATH):
                if file.lower()==s:
                    result = re.search(f'template-(.+).fits', file)
                    self.l2_current['zBestSubType']=result.group(1)
                    self.plotter.PlotFile(self.l2_current)
                    break

    def drawTemplate(self):
        firstLoad = True
        state = self.model.getState()
        file = state.file
        fitting = state.fitting
        self.templater.plotTemplate(file, fitting)
        #set combobox text:
        best = fitting['zBestSubType'].lower()
        #print(f'template-%s' % best)
        self.dropdown.setCurrentText(f'template-%s.fits' % best)
        self.spec_current=file
        self.l2_current=fitting
        if firstLoad:
            self.setMiddle(fitting)