
from plotter import Plotter
from Model import Model

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    )

import re

class Navigator:

    layout: QHBoxLayout
    model: Model
    plotter: Plotter

    def __init__(self, plotter, model):
        self.model = model
        self.plotter = plotter
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        whyInput.setPlaceholderText("Write your notes here")
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

    def loadFile(self, delta=1):
        print("Current File: " + self.getCurrentFile())

        while True:
            try:
                self.current = tool.SDSS_spectrum(self.directory.absoluteFilePath(self.getCurrentFile()))
                print("Current File: " + self.getCurrentFile())
                self.UpdateGraph(self.current)
                break
            except OSError:
                self.deleteFile(delta)
                continue
            except IndexError: #Osiris
                #check if there are other files with similar names
                result = re.search(f'(.+)([RGB]).fits', self.getCurrentFile())
                if result != None:
                    #Create a list of the files
                    self.grismArray(result.group(1))
                else:
                    result = re.search(f'(.+).fits', self.getCurrentFile())
                    self.grismArray(result.group(1))
                break
        self.targetData.updateTargetData(self.getCurrentFilePath()) # Updates target data labels
 
    def NavBtn (self, msg, delta):
        if msg == "Yes":
            self.model.addDBEntry(True, self.whyInput.toPlainText())
        elif msg == "Unsure":
            self.model.addDBEntry(False, self.whyInput.toPlainText())

        self.whyInput.setPlainText("")
        self.model.updateCursor(delta)
        self.plotter.update()
