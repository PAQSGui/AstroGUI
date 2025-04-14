from Model import Model
from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QPushButton,
)

class OptionsWindow(QWidget):

    optionChanged = Signal()
    model: Model
    colors = ['Grey', 'Black','Purple', 'Blue', 'Green', 'Yellow', 'Orange', 'Red',]

    def __init__(self, model):
        super().__init__()

        self.setWindowTitle("Options")
        self.model = model

        lineWidth = QHBoxLayout()
        lineWidth.addWidget(QLabel('Line width'))
        ltEdit = QLineEdit()
        ltEdit.setText(str(model.getOption('LineWidth')*10))
        ltEdit.setInputMask('D')
        ltEdit.editingFinished.connect(lambda: self.updateOption('LineWidth', float(ltEdit.text())/10))
        lineWidth.addWidget(ltEdit)

        graphColor = self.colorChooser("Graph:",'GraphColor')
        noiseColor = self.colorChooser("Noise:",'NoiseColor')

        snColor = self.colorChooser("S/N:", 'SNColor')
        skyColor = self.colorChooser("Sky:", 'SkyColor')

        graphHeight = QHBoxLayout()
        minEdit = QLineEdit()
        minEdit.setText(str(model.getOption('ymin')))
        minEdit.setInputMask('900')
        minEdit.editingFinished.connect(lambda: self.model.setOption('ymin', minEdit.text()))
        maxEdit = QLineEdit()
        maxEdit.setText(str(model.getOption('ymax')))
        maxEdit.setInputMask('900')
        maxEdit.editingFinished.connect(lambda: self.model.setOption('ymax', maxEdit.text()))
        button = QPushButton('Adjust')
        button.clicked.connect(lambda: self.updateOption('yLimit', True))

        graphHeight.addWidget(QLabel('Y-axis:'))
        graphHeight.addWidget(minEdit)
        graphHeight.addWidget(maxEdit)
        graphHeight.addWidget(button)

        layout = QVBoxLayout()
        layout.addLayout(lineWidth)

        layout.addWidget(QLabel('Colors'))
        layout.addWidget(graphColor)
        layout.addWidget(noiseColor)
        layout.addWidget(snColor)
        layout.addWidget(skyColor)
        layout.addLayout(graphHeight)

        self.setLayout(layout)
        
    def colorChooser(self, text, key):
        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        colorGroup = QButtonGroup(widget)

        layout.addWidget(QLabel(text))

        current = self.model.getOption(key)

        for color in self.colors:
            button = QRadioButton(color)
            colorGroup.addButton(button)
            if color == current:
                button.setChecked(True)
            layout.addWidget(button)

        colorGroup.buttonClicked.connect(lambda button: self.updateOption(key, button.text()))
        return widget

    def updateOption(self, opt, val):
        self.model.setOption(opt, val)
        self.optionChanged.emit()


