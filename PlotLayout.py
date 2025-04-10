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
    QPushButton
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

        zSlider = QSlider(Qt.Orientation.Horizontal)
        zSlider.setSingleStep(1)
        zSlider.setMinimum(0)
        zSlider.setMaximum(200)
        zSlider.setValue(model.getRedShift()*10)
        zSlider.sliderMoved.connect(self.sliderChanged)
        self.zSlider = zSlider

        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)
        self.dropdown.textActivated.connect(self.text_changed)

        signoiseButton = QPushButton("Toggle S/N spec")
        signoiseButton.clicked.connect(lambda: self.toggleSN())
        showskybutton = QPushButton("Toggle Sky")
        showskybutton.clicked.connect(lambda: self.toggleSky())

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.dropdown)
        sliderLayout.addWidget(zSlider)
        sliderLayout.addWidget(signoiseButton)
        sliderLayout.addWidget(showskybutton)

        plotLayout = QHBoxLayout()
        plotLayout.addWidget(fig)
        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.layout.addLayout(sliderLayout)
        self.update()

    def newFile(self):
        self.zSlider.setValue(self.model.getRedShift()*10)
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
        self.model.changeRedShift(float(self.zSlider.value())/10)
        self.update()
    
    def text_changed(self, s):

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
