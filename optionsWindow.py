from Model import Model

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QRadioButton,
    QButtonGroup,
)

class OptionsWindow(QWidget):
    model: Model

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

        graphColor = self.colorChooser("Graph",'GraphColor')

        noiseColor = self.colorChooser("Noise",'NoiseColor')





        layout = QVBoxLayout()
        layout.addLayout(lineWidth)

        layout.addWidget(QLabel('Colors'))
        layout.addLayout(graphColor)
        layout.addLayout(noiseColor)
        self.setLayout(layout)


        #thickSlider=QSlider(Qt.Orientation.Horizontal)
        #thickSlider.setRange(1,15) #slider only takes integers
        #thickSlider.setSingleStep(1)
        #thickSlider.setValue(int(model.getOption('lineWidth')))
        #thickSlider.valueChanged.connect(lambda: model.setOptions('lineWidth', thickSlider.value()))

        #optsLayout.addWidget(thickSlider)

        #"lineWidth": 3,
        #"GraphColor": "Black",
        #"TemplateColor" : "Red",
        #"NoiseColor" : "Grey",
        #"SNColor": "Blue",
        #"skyColor": "Orange"
    
    def colorChooser(self, text, key):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(text))
        colors = QButtonGroup()
        #colors.addButton(QRadioButton('Green'))
        #colors.addButton(QRadioButton('Orange'))
        blue = QRadioButton('Blue')
        red = QRadioButton('Red')

        colors.addButton(blue)
        colors.addButton(red)

        layout.addWidget(blue)
        layout.addWidget(red)
        #layout.addWidget(colors)
        return layout

    def updateOption(self, opt, val):
        self.model.setOptions(opt, val)
        self.plo.update()


