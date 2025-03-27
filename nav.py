
import Spec_tools as tool
from xpca.pipeline import Pipeline
from fitter import Fitter
from database import Database

from PySide6.QtCore import (
    QDir,
)

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QFileDialog as browse,
    QPlainTextEdit,
    )

class Navigator:

    cursor: int
    files: list[str]
    directory: QDir
    current: tool.SDSS_spectrum
    layout: QHBoxLayout
    pipe: Pipeline
    fitter: Fitter
    database: Database

    def __init__(self, cursor, plotter, fitter, targetData):
        self.pipe=Pipeline()
        self.layout = QHBoxLayout()
        self.directory = QDir("./spectra")
        self.directory.setNameFilters(["([^.]*)","*.fits"])
        self.files = self.directory.entryList()
        self.cursor = cursor
        self.plotter = plotter
        self.fitter = fitter
        self.targetData = targetData
        self.database = Database("data.csv")

        whyInput = QPlainTextEdit()
        whyInput.setPlaceholderText("Type your reason for choosing 'unsure'")
        self.whyInput = whyInput


        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.NavBtn(msg="Back",delta=-1))

        yesButton = QPushButton("Yes")
        yesButton.clicked.connect(lambda: self.NavBtn( msg="Yes",delta=1))

        unsureButton = QPushButton("Unsure")
        unsureButton.clicked.connect(lambda: self.NavBtn(msg="Unsure",delta=1))

        #whyLayout = QVBoxLayout()
        ##whyLayout.addWidget(QLabel("Why, or why not:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?"))
        #whyLayout.addWidget(self.whyInput)
        #self.layout.addLayout(whyLayout)

        self.layout.addWidget(backButton)
        self.layout.addWidget(yesButton)
        self.layout.addWidget(unsureButton)
        self.layout.addWidget(self.whyInput)

    def Navigate(self, delta):
        self.cursor += delta
    
    def getCurrentFile(self):
        return self.files[self.cursor]
    
    def getCurrentFilePath(self):
        return self.directory.absoluteFilePath(self.getCurrentFile())  
        
    def updateCursor(self, delta):
        self.cursor = self.cursor + delta
    
    def deleteFile(self, delta):
        del self.files[self.cursor]
        if delta < 0:
            self.updateCursor(-1)
        print("skipping bad file\n")

    def openFolder(self):
        #Tests: What if you cancel selecting a folder? What if the folder does not exist? What if it is the first time you select a folder?
        
        folder_path = browse.getExistingDirectory(None, "Select Folder")
        if folder_path:
            self.directory = QDir(folder_path)
        self.files = self.directory.entryList()
        self.cursor = 0
        self.loadFile()

    def loadFile(self, delta=1):
        print("Current File: " + self.getCurrentFile())

        while True:
            try:
                self.current = tool.SDSS_spectrum(self.directory.absoluteFilePath(self.getCurrentFile())) #not OS safe I think
                print("Current File: " + self.getCurrentFile())
                break
            except OSError:
                self.deleteFile(delta)
                continue
        self.UpdateGraph(self.current)
        self.targetData.updateTargetData(self.getCurrentFilePath()) # Updates target data labels

    def UpdateGraph(self, file):
        self.fitter.fitFile(self.getCurrentFilePath())
        self.plotter.addFile(file, self.fitter.getl2_product())

    def getUserInput(self):
        text = self.whyInput.toPlainText()
        self.whyInput.clear()
        return text


    def NavBtn (self, msg, delta):
        if msg == "Back":
            pass
        elif msg == "Yes":
            self.database.addEntry(self.getCurrentFile(), self.fitter.best, "None", self.fitter.redshift)
        elif msg == "Unsure":
            self.database.addEntry(self.getCurrentFile(), "None", self.whyInput.toPlainText(), 0.0)
            self.whyInput.setPlainText("")

        self.updateCursor(delta)
        self.loadFile(delta)

#XPCA error with sdss
#File "/home/artemis/Documents/AstroGUI/AstroGUI/.venv/lib/python3.12/site-packages/xpca/targets.py", line 140, in read_sdss_spectrum
#    row = QTable.read(filename, 1)
#astropy.io.registry.base.IORegistryError: Format could not be identified based on the file name or contents, please provide a 'format' argument.