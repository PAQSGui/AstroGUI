from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from matplotlib.pyplot import figure
from xpca import config
from os import listdir
import re
from plotter import Plotter

from PySide6.QtWidgets import (
    QLayout,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel,
    QComboBox,
    QLineEdit,
    QSizePolicy,
    QCheckBox,
)

from PySide6.QtGui import (
    Qt,
    QDoubleValidator,
)

from PySide6.QtCore import (
    QSize,
    Slot,
)

"""
The PlotLayout is responsible for the part of the window where the graph is located.
It should NOT plot or load files.
"""
class PlotLayout(QWidget):
    layout: QHBoxLayout
    model: Model
    plotter: Plotter
    zSlider: QSlider
    zTextBox: QLineEdit

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QVBoxLayout()

        fig = FigureCanvasQTAgg(figure('k'))
        fig.setMinimumSize(QSize(560, 560))
        self.plotter = Plotter(model, fig)

        redshiftResolution = self.model.getOption('zResolution') 
        redshiftMax = self.model.getOption('zMax')

        zSlider = QSlider(Qt.Orientation.Horizontal)
        zSlider.setSingleStep(1)
        zSlider.setMinimum(0)
        zSlider.setMaximum(redshiftMax*redshiftResolution)
        zSlider.setValue(model.getRedShift()*redshiftResolution)
        zSlider.sliderMoved.connect(self.sliderChanged)
        self.zSlider = zSlider

        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                text = file[:-5]
                self.dropdown.addItem(text)
        self.dropdown.textActivated.connect(self.dropboxSelect)
        self.dropdown.setCurrentText(str(self.model.getCategory()).lower())

        signoiseButton = QCheckBox("S/N spec")
        signoiseButton.clicked.connect(lambda: self.toggleSN())
        showskybutton = QCheckBox("Sky")
        showskybutton.clicked.connect(lambda: self.toggleSky())

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.dropdown)
        sliderLayout.addWidget(zSlider)

        sliderLayout.addWidget(QLabel("z ="))
        self.zTextBox=QLineEdit(text=str(round(model.getRedShift(),4)))
        self.zTextBox.setValidator(QDoubleValidator())
        self.zTextBox.editingFinished.connect(self.zTextInput)
        self.zTextBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sliderLayout.addWidget(self.zTextBox)

        sliderLayout.addWidget(signoiseButton)
        sliderLayout.addWidget(showskybutton)

        plotLayout = QHBoxLayout()
        plotLayout.addWidget(fig)
        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.layout.addLayout(sliderLayout)
        self.update()
        self.setLayout(self.layout)

    @Slot()
    def update(self):
        self.plotter.UpdateFigure()

    @Slot()
    def newFile(self):
        self.zSlider.setValue(self.model.getRedShift()*self.model.getOption('zResolution'))
        self.zTextBox.setText(str(round(self.model.getRedShift(),4)))
        self.dropdown.setCurrentText(str(self.model.getCategory()).lower())
        self.model.resetYLimit()
        self.update()

    def toggleSN(self):
        new = not self.model.getOption('ShowSN')
        self.model.setOption('ShowSN', new)
        self.update()

    def toggleSky(self):        
        new = not self.model.getOption('ShowSky')
        self.model.setOption('ShowSky', new)
        self.update()
    
    def getYLimit(self):
        return self.plotter.getYLim()

    def sliderChanged(self):
        self.model.changeRedShift(float(self.zSlider.value())/self.model.getOption('zResolution'))
        self.zTextBox.setText(str(self.model.getRedShift()))
        self.plotter.UpdateFigure()

    def zTextInput(self):
            input = float(self.zTextBox.text())
            if input > self.model.getOption('zMax'):
                input = self.model.getOption('zMax')
                self.zTextBox.setText(str(input))
            elif input < 0:
                input = 0
                self.zTextBox.setText(str(input))

            self.model.changeRedShift(input)
            self.zSlider.setValue(int(input*self.model.getOption('zResolution')))
            self.update()

    def dropboxSelect(self, s):

        result = re.search(f'template-(.+)', s)
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
