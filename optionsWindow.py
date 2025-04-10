from Model import Model

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

class OptionsWindow(QWidget):
    model: Model

    def __init__(self, model, plo):
        super().__init__()

        self.model = model
        self.plo = plo


        layout = QVBoxLayout()

        self.label = QLabel("Options")
        layout.addWidget(QLabel("Plot Line Thickness"))


        layout.addWidget(self.label)
        self.setLayout(layout)

        #thickSlider=QSlider(Qt.Orientation.Horizontal)
        #thickSlider.setRange(1,15) #slider only takes integers
        #thickSlider.setSingleStep(1)
        #thickSlider.setValue(int(model.getOption('lineThickness')))
        #thickSlider.valueChanged.connect(lambda: model.setOptions('lineThickness', thickSlider.value()))

        #optsLayout.addWidget(thickSlider)


