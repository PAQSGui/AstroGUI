
from plotter import Plotter
from Model import Model

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    )

class Navigator:

    layout: QHBoxLayout
    model: Model
    plotter: Plotter

    def __init__(self, plotter, model):
        self.model = model
        self.plotter = plotter
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        whyInput.setPlaceholderText("Type your reason for choosing 'unsure'")
        self.whyInput = whyInput

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.NavBtn(msg="Back",delta=-1))

        yesButton = QPushButton("Yes")
        yesButton.clicked.connect(lambda: self.NavBtn( msg="Yes",delta=1))

        unsureButton = QPushButton("Unsure")
        unsureButton.clicked.connect(lambda: self.NavBtn(msg="Unsure",delta=1))

        self.layout.addWidget(backButton)
        self.layout.addWidget(yesButton)
        self.layout.addWidget(unsureButton)
        self.layout.addWidget(self.whyInput)

    def NavBtn (self, msg, delta):
        if msg == "Back":
            pass
        elif msg == "Yes":
            pass
            # add in model database
            #self.database.addEntry(self.getCurrentFile(), self.fitter.best, "None", self.fitter.redshift)
        elif msg == "Unsure":
            pass
            # addd in model database
            #self.database.addEntry(self.getCurrentFile(), "None", self.whyInput.toPlainText(), 0.0)
            #self.whyInput.setPlainText("")

        self.model.updateCursor(delta)
        self.plotter.update()
