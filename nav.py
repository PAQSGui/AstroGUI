#from tkinter import filedialog as browse
import os
import Spec_tools as tool
from xpca.pipeline import Pipeline
import plotter
from fitter import Fitter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure

from PySide6.QtCore import (
    QSize,
    QDir,
    QDirIterator,
)

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog as browse,
    QTextEdit,
    QLabel,
    )

class Navigator:

    cursor: int
    files: list[str]
    directory: QDir
    current: tool.SDSS_spectrum
    layout: QHBoxLayout
    pipe: Pipeline
    fitter: Fitter

    def __init__(self, cursor, plotter, fitter):
        self.pipe=Pipeline()
        self.layout = QHBoxLayout()
        self.directory = QDir("./spectra")
        self.directory.setNameFilters(["([^.]*)","*.fits"])
        self.files = self.directory.entryList()
        self.cursor = cursor
        self.plotter = plotter
        self.fitter = fitter
        self.whyInput = QTextEdit()


        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: NavBtn(self, msg="Back",delta=-1))

        yesButton = QPushButton("Yes")
        yesButton.clicked.connect(lambda: NavBtn(self, msg="Yes",delta=1))

        noButton = QPushButton("No")
        noButton.clicked.connect(lambda: NavBtn(self, msg="No",delta=1))

        unsureButton = QPushButton("Unsure")
        unsureButton.clicked.connect(lambda: NavBtn(self, msg="Unsure",delta=1))

        whyLayout = QVBoxLayout()
        whyLayout.addWidget(QLabel("Why, or why not:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?"))
        whyLayout.addWidget(self.whyInput)
        self.layout.addLayout(whyLayout)

        self.layout.addWidget(backButton)
        self.layout.addWidget(yesButton)
        self.layout.addWidget(noButton)
        self.layout.addWidget(unsureButton)

    def Navigate(self, delta):
        print(self.files[self.cursor])
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
                print(str(self.directory))
                self.current = tool.SDSS_spectrum(self.directory.absoluteFilePath(self.getCurrentFile())) #not OS safe I think
                print("Current File: " + self.getCurrentFile())
                break
            except OSError:
                self.deleteFile(delta)
                continue
        self.UpdateGraph(self.current)

    def UpdateGraph(self, file):
        self.plotter.addFile(file)
        self.fitter.fitFile(self.getCurrentFilePath())

    def getUserInput(self):
        text = self.whyInput.toPlainText()
        self.whyInput.clear()
        return text


def NavBtn (navigator, msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' waith the target name once we can extract that information
        data = f"{navigator.getCurrentFile()},{msg}"
        usrinput = navigator.getUserInput()
        if usrinput != "":
            data += f",{usrinput}\n"
        else:
            data += ",NO_INPUT\n"
        f.write(data)
    navigator.updateCursor(delta)
    navigator.loadFile(delta)