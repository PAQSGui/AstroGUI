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
    QPushButton,
    QLineEdit,
    )

from PySide6.QtGui import (
    Qt,
    QDoubleValidator,
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
    zTextBox: QLineEdit

    def __init__(self, model):
        self.model = model
        self.layout = QVBoxLayout()

        fig = FigureCanvasQTAgg(figure('k'))
        fig.setMinimumSize(QSize(560, 560))
        self.plotter = Plotter(model, fig)

        zSlider = QSlider(Qt.Orientation.Horizontal)
        zSlider.setSingleStep(1)
        zSlider.setMinimum(0)
        zSlider.setMaximum(self.model.redshiftMax*self.model.redshiftRez)
        zSlider.setValue(model.getRedShift()*self.model.redshiftRez)
        zSlider.sliderMoved.connect(self.sliderChanged)
        self.zSlider = zSlider

        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)
        self.dropdown.textActivated.connect(self.dropboxSelect)

        signoiseButton = QPushButton("Toggle S/N spec")
        signoiseButton.clicked.connect(lambda: self.toggleSN())
        showskybutton = QPushButton("Toggle Sky")
        showskybutton.clicked.connect(lambda: self.toggleSky())

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.dropdown)
        sliderLayout.addWidget(zSlider)

        self.zTextBox=QLineEdit(text=str(model.getRedShift()))
        self.zTextBox.setValidator(QDoubleValidator())
        self.zTextBox.editingFinished.connect(self.zTextInput)
        sliderLayout.addWidget(self.zTextBox)

        sliderLayout.addWidget(signoiseButton)
        sliderLayout.addWidget(showskybutton)

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
        self.thickSlider.setValue(int(self.model.lineThickness*10))
        self.thickSlider.valueChanged.connect(lambda: self.setThickness(self.thickSlider.value()))
        self.optsLayout.addWidget(self.thickSlider)
        self.optsWindow.setLayout(self.optsLayout)
        self.optsWindow.show()

    def setThickness(self, newValue):
        self.model.lineThickness=float(newValue)/10.0
        self.plotter.UpdateFigure()

    def newFile(self):
        self.zSlider.setValue(self.model.getRedShift()*self.model.redshiftRez)
        self.update()

    def update(self):
        self.plotter.UpdateFigure()

    def toggleSN(self):
        self.plotter.showSN = not self.plotter.showSN
        self.update()

    def toggleSky(self):
        self.plotter.showSky = not self.plotter.showSky
        self.update()

    def sliderChanged(self):
        self.model.changeRedShift(float(self.zSlider.value())/self.model.redshiftRez)
        self.zTextBox.setText(str(self.model.getRedShift()))
        self.update()

    def zTextInput(self):
            conv=float(self.zTextBox.text())
            if conv>self.model.redshiftMax:
                conv=self.model.redshiftMax
                self.zTextBox.setText(str(conv))
            elif conv<self.model.redshiftMin:
                conv=self.model.redshiftMin
                self.zTextBox.setText(str(conv))

            self.model.changeRedShift(conv)
            self.zSlider.setValue(int(conv*self.model.redshiftRez))
            self.update()

    
    def dropboxSelect(self, s):

        result = re.search(f'template-(.+).fits', s)
        self.model.changeCategory(result.group(1))
        
        try:
            self.update()
        except FileNotFoundError as e:
            for file in listdir(config.TEMPLATE_PATH):
                if file.lower()==s:
                    result = re.search(f'template-(.+).fits', file)
                    self.l2_current['zBestSubType']=result.group(1)
                    self.plotter.PlotFile(self.l2_current)
                    break
