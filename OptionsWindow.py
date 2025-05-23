from Model import Model
from PySide6.QtCore import Signal, Slot

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QPushButton,
    QGroupBox,
)

from PySide6.QtGui import QIntValidator

"""
The option dialog opens in a new window so it's possible to see changes to the graph as they are made
This class should only update the options by calling the setOption() method from Model
"""
class OptionsWindow(QWidget):
    optionChanged = Signal()
    model: Model
    colors = ['Grey', 'Black','Purple', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']

    lineWidthEdit: QLineEdit
    minEdit: QLineEdit
    maxEdit: QLineEdit
    colorLayout = QHBoxLayout()

    def __init__(self, model):
        super().__init__()

        self.setWindowTitle('Options')
        self.model = model

        lineWidthLayout = QHBoxLayout()
        lineWidthLayout.addWidget(QLabel('Line width'))

        self.lineWidthEdit = QLineEdit()
        self.lineWidthEdit.setValidator(QIntValidator(0, 9))
        self.lineWidthEdit.editingFinished.connect(lambda: self.updateOption('LineWidth', float(self.lineWidthEdit.text())/10))

        lineWidthLayout.addWidget(self.lineWidthEdit)

        graphHeight = QHBoxLayout()

        self.minEdit = QLineEdit()
        self.minEdit.setValidator(QIntValidator(0, 900))
        self.minEdit.editingFinished.connect(lambda: self.model.setOption('ymin', self.minEdit.text()))

        self.maxEdit = QLineEdit()
        self.maxEdit.setValidator(QIntValidator(0, 900))
        self.maxEdit.editingFinished.connect(lambda: self.model.setOption('ymax', self.maxEdit.text()))
        button = QPushButton('Adjust')
        button.clicked.connect(lambda: self.updateOption('yLimit', True))

        graphHeight.addWidget(QLabel('Y-axis:'))
        graphHeight.addWidget(self.minEdit)
        graphHeight.addWidget(self.maxEdit)
        graphHeight.addWidget(button)

        layout = QVBoxLayout()

        layout.addLayout(lineWidthLayout)
        layout.addWidget(QLabel('Colors'))
        layout.addLayout(self.colorLayout)
        layout.addLayout(graphHeight)

        self.setLayout(layout)
        
    @Slot()
    def setupSession(self,_):
        self.lineWidthEdit.setText(str(self.model.getOption('LineWidth')*10))
        self.minEdit.setText(str(self.model.getOption('ymin')))
        self.maxEdit.setText(str(self.model.getOption('ymax')))

        self.colorLayout.addWidget(self.colorChooser('Graph:', 'GraphColor'))
        self.colorLayout.addWidget(self.colorChooser('Template:', 'TemplateColor'))
        self.colorLayout.addWidget(self.colorChooser('Noise:', 'NoiseColor'))
        self.colorLayout.addWidget(self.colorChooser('S/N:', 'SNColor'))
        self.colorLayout.addWidget(self.colorChooser('Sky:', 'SkyColor'))

    @Slot()
    def shutDownSession(self, _):
        self.lineWidthEdit.setText('')
        self.colorLayout.clearLayout()
    
    def colorChooser(self, text, key):
        layout = QVBoxLayout()
        box = QGroupBox(text)
        box.setLayout(layout)

        colorGroup = QButtonGroup(box)

        current = self.model.getOption(key)

        for color in self.colors:
            button = QRadioButton(color)
            colorGroup.addButton(button)
            if color == current:
                button.setChecked(True)
            layout.addWidget(button)

        colorGroup.buttonClicked.connect(lambda button: self.updateOption(key, button.text()))
        return box

    def updateOption(self, option, value):
        self.model.setOption(option, value)
        self.optionChanged.emit()
