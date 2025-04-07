from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from matplotlib.pyplot import figure

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
from os import listdir
import re

class PlotLayout:
    layout: QHBoxLayout
    model: Model
    plotter: Plotter
    zSlider: QSlider 

    def __init__(self, model):
        self.model = model
        self.layout = QVBoxLayout()

        fig = FigureCanvasQTAgg(figure('k'))
        fig.setMinimumSize(QSize(560, 560))
        self.plotter = Plotter(model, fig)

        sliderLayout = QHBoxLayout()

        zSlider = QSlider(Qt.Orientation.Horizontal)
        zSlider.setSingleStep(1)
        zSlider.sliderMoved.connect(self.slider_changed)
        #zSlider.sliderReleased.connect(self.sliderrelease)
        self.zSlider = zSlider
        sliderLayout.addWidget(zSlider)

        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)

        sliderLayout.addWidget(self.dropdown)

        self.dropdown.textActivated.connect(self.text_changed)

        plotLayout = QHBoxLayout()
        plotLayout.addWidget(fig)
        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.layout.addLayout(sliderLayout)
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

    def update(self):
        self.plotter.UpdateFigure()
        self.setMiddle()

    def toggleSN(self):
        self.plotter.showSN = not self.plotter.showSN
        self.update()

    def toggleSky(self):
        self.plotter.showSky = not self.plotter.showSky
        self.update()

    def sliderrelease(self):
        self.model.changeRedShift(float(self.zSlider.value())/100)
        self.setMiddle()
        self.update()

    def slider_changed(self):
        self.model.changeRedShift(float(self.zSlider.value())/100)
        self.setMiddle()
        self.update()

    def setMiddle(self):
        redshift = self.model.getRedShift()
        newMiddle = redshift*100
        self.zSlider.setMinimum(newMiddle-100)
        self.zSlider.setMaximum(newMiddle+100)
        self.zSlider.setValue(newMiddle)
    
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