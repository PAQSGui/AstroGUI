
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

from ssPicture import SkygrabWindow

class Navigator:

    layout: QHBoxLayout
    model: Model
    plotlayout: PlotLayout
    skygrabWindow: SkygrabWindow

    def __init__(self, plotlayout, infoLayout, model):
        self.model = model
        self.plotlayout = plotlayout
        self.layout = QHBoxLayout()
        self.infoLayout=infoLayout

        self.skygrabWindow = SkygrabWindow()

        whyInput = QPlainTextEdit()
        note = self.model.getNote()
        if note == "":
            whyInput.setPlaceholderText("Write your notes here")
        else:
            whyInput.setPlainText(note)
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

        self.model.updateCursor(delta)
        self.plotlayout.update()
        note = self.model.getNote()
        self.whyInput.setPlainText(note)
        self.plotlayout.newFile()
        self.infoLayout.updateAll()
        if (self.skygrabWindow.isHidden()):
            self.model.skygrabNotLoaded=True
        else:
            self.skygrabWindow.LoadPicture(self.model)
