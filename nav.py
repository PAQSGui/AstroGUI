
from PlotLayout import PlotLayout
from Model import Model
import Spec_tools as tool

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    )

import re

class Navigator:

    layout: QHBoxLayout
    model: Model
    plotter: PlotLayout

    def __init__(self, plotter, model):
        self.model = model
        self.plotter = plotter
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        note = self.model.getNote()
        if note == "":
            whyInput.setPlaceholderText("Write your notes here")
        else:
            whyInput.setPlainText(note)
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

#    def grismArray(self, filename):
#        grisms = []
#        for x in ['','R','G','B']:
#            try:
#                nextGrism = tool.Osiris_spectrum(self.directory.absoluteFilePath(filename+x+".fits"))
#                grisms.append(nextGrism)
#            except FileNotFoundError:
#                grisms.append(None)
#        self.plotter.UpdateGrism(grisms)
 
    def NavBtn (self, msg, delta):
        if msg == "Yes":
            self.model.addDBEntry(True, self.whyInput.toPlainText())
        elif msg == "Unsure":
            self.model.addDBEntry(False, self.whyInput.toPlainText())

        self.model.updateCursor(delta)
        self.plotter.update()
        note = self.model.getNote()
        self.whyInput.setPlainText(note)
