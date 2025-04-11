from Model import Model

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
)

class OptionsWindow(QWidget):
    model: Model
    colors = ['Grey', 'Black','Purple', 'Blue', 'Green', 'Yellow', 'Orange', 'Red',]

    def __init__(self, model, plo):
        super().__init__()

        self.setWindowTitle("Options")
        self.model = model
        self.plo = plo

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

        layout = QVBoxLayout()
        layout.addLayout(lineWidth)

        layout.addWidget(QLabel('Colors'))
        layout.addWidget(graphColor)
        layout.addWidget(noiseColor)
        layout.addWidget(snColor)
        layout.addWidget(skyColor)
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
        self.plo.update()


