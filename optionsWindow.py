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
    QGroupBox,
)

"""
The option dialog opens in a new window so it's possible to see changes to the graph as they are made
This class should only update the options by calling the setOption() method from Model
"""
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

        colorsLayout = QHBoxLayout()
        colorsLayout.addWidget(self.colorChooser("Graph:",'GraphColor'))
        colorsLayout.addWidget(self.colorChooser("Template:",'TemplateColor'))
        colorsLayout.addWidget(self.colorChooser("Noise:",'NoiseColor'))
        colorsLayout.addWidget(self.colorChooser("S/N:", 'SNColor'))
        colorsLayout.addWidget(self.colorChooser("Sky:", 'SkyColor'))

        colors = QGroupBox('Colors')
        colors.setLayout(colorsLayout)

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

        layout.addWidget(colors)
        layout.addLayout(graphHeight)

        self.setLayout(layout)
        
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

    def updateOption(self, opt, val):
        self.model.setOption(opt, val)
        self.optionChanged.emit()


