
from PlotLayout import PlotLayout
from Model import Model
import Spec_tools as tool

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    )

import re
from PySide6.QtCore import QSize


class Navigator:

    layout: QHBoxLayout
    model: Model
    plotlayout: PlotLayout

    def __init__(self, plotlayout, model):
        self.model = model
        self.plotlayout = plotlayout
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        whyInput.setPlaceholderText("Write your notes here")
        whyInput.setMaximumSize(QSize(9999999, 50))
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
        if msg == "Yes":
            self.model.addDBEntry(True, self.whyInput.toPlainText())
        elif msg == "Unsure":
            self.model.addDBEntry(False, self.whyInput.toPlainText())

        self.whyInput.setPlainText("")
        self.model.updateCursor(delta)
        self.plotlayout.newFile()
