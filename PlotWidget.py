from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from matplotlib.pyplot import figure
from xpca import config
from os import listdir
from re import search
from Plotter import Plotter

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
    QLocale,
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
    signoiseButton: QCheckBox
    showskyButton: QCheckBox
    dropdown: QComboBox

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QVBoxLayout()

        fig = FigureCanvasQTAgg(figure('k'))
        fig.setMinimumSize(QSize(560, 560))
        self.plotter = Plotter(model, fig)

        self.model.openedSession[int].connect(self.setupSession)
        self.model.closedSession[int].connect(self.shutDownSession)

        zSlider = QSlider(Qt.Orientation.Horizontal)
        zSlider.setSingleStep(1)
        zSlider.setMinimum(0)
        self.zSlider = zSlider

        self.dropdown = QComboBox()
        self.dropdown.setMinimumWidth(95)

        self.signoiseButton = QCheckBox('Toggle S/N spec')
        self.showskyButton = QCheckBox('Toggle Sky')

        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.dropdown)
        sliderLayout.addWidget(zSlider)

        sliderLayout.addWidget(QLabel('z ='))
        self.zTextBox = QLineEdit()
        self.zTextBox.setValidator(QDoubleValidator(notation=QDoubleValidator.Notation.StandardNotation))
        self.zTextBox.validator().setLocale(QLocale.Language.English)
        self.zTextBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sliderLayout.addWidget(self.zTextBox)

        sliderLayout.addWidget(self.signoiseButton)
        sliderLayout.addWidget(self.showskyButton)

        plotLayout = QHBoxLayout()
        plotLayout.addWidget(fig)
        plotLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.layout.addLayout(plotLayout)
        self.layout.addLayout(sliderLayout)
        self.setLayout(self.layout)

    @Slot()
    def setupSession(self, _):
        redshiftResolution = self.model.getOption('zResolution') 
        redshiftMax = self.model.getOption('zMax')

        self.zSlider.setMaximum(redshiftMax*redshiftResolution)
        self.zSlider.setValue(self.model.getRedShift()*redshiftResolution)
        self.zSlider.sliderMoved.connect(self.sliderChanged)

        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith('.fits'):
                result = search(f'template-(new-)?(.+).fits', file)
                text = result[2]
                self.dropdown.addItem(text)
        self.dropdown.textActivated.connect(self.dropboxSelect)
        self.dropdown.setCurrentText(str(self.model.getCategory()).lower())

        self.signoiseButton.clicked.connect(lambda: self.toggleSN())
        self.showskyButton.clicked.connect(lambda: self.toggleSky())

        self.zTextBox.setText(str(round(self.model.getRedShift(), 4)))
        self.zTextBox.editingFinished.connect(self.zTextInput)
        self.update()

    @Slot()
    def shutDownSession(self, _):
        self.zSlider.sliderMoved.disconnect()

        self.dropdown.textActivated.disconnect()
        self.dropdown.clear()

        self.signoiseButton.clicked.disconnect()
        self.showskyButton.clicked.disconnect()

        self.zTextBox.setText('')
        self.zTextBox.editingFinished.disconnect()

    @Slot()
    def update(self):
        self.plotter.UpdateFigure()

    @Slot()
    def newFile(self):
        self.zSlider.setValue(self.model.getRedShift() * self.model.getOption('zResolution'))
        self.zTextBox.setText(str(round(self.model.getRedShift(), 4)))
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
        self.model.changeRedShift(float(self.zSlider.value()) / self.model.getOption('zResolution'))
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
            self.zSlider.setValue(int(input * self.model.getOption('zResolution')))
            self.update()

    def dropboxSelect(self, category):
        redshiftResolution = self.model.getOption('zResolution')
        self.model.changeCategory(category)
        self.update()
        self.zSlider.setValue(int(self.model.getRedShift() * redshiftResolution))
        self.zTextBox.setText(str(round(self.model.getRedShift(), 4)))