#from tkinter import filedialog as browse
import os
import Spec_tools as tool
from xpca.pipeline import Pipeline
import plotter
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
    bigFig : FigureCanvasQTAgg
    info_2xp : QLabel
    info_2cp : QLabel

    def __init__(self, cursor, plotter):
        self.pipe=Pipeline()
        self.layout = QHBoxLayout()
        self.directory = QDir("./spectra")
        self.directory.setNameFilters(["([^.]*)","*.fits"])
        self.files = self.directory.entryList()
        self.cursor = cursor
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.plotter = plotter

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: NavBtn(self, msg="Back",delta=-1))

        yesButton = QPushButton("Yes")
        yesButton.clicked.connect(lambda: NavBtn(self, msg="Yes",delta=1))

        noButton = QPushButton("No")
        noButton.clicked.connect(lambda: NavBtn(self, msg="No",delta=1))

        unsureButton = QPushButton("Unsure")
        unsureButton.clicked.connect(lambda: NavBtn(self, msg="Unsure",delta=1))

        whyLayout = QVBoxLayout()
        whyInput = QTextEdit()
        whyLayout.addWidget(QLabel("Why, or why not:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?"))
        whyLayout.addWidget(whyInput)
        self.layout.addLayout(whyLayout)

        self.info_2xp=QLabel("2XP: best-fit template + Z\_BEST (plus lines)")
        self.info_2cp=QLabel("2CP: CLASS, PROB, CLASS2, PROB2")

        self.layout.addWidget(backButton)
        self.layout.addWidget(yesButton)
        self.layout.addWidget(noButton)
        self.layout.addWidget(unsureButton)

    def Navigate(self, delta):
        print(self.files[self.cursor])
        self.cursor += delta
    
    def getCurrentFile(self):
        return self.files[self.cursor]
        
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
        self.pipe.run(self.directory.absoluteFilePath(self.getCurrentFile()),source='sdss')
        #print(pipe.catalog_items)
        ZBEST=self.pipe.catalog_items[0]['zBest']
        CLASS=self.pipe.catalog_items[0]['zBestSubType']
        PROB=self.pipe.catalog_items[0]['zBestProb']
        self.info_2xp.setText("2XP: best-fit template + "+ str(ZBEST) +" (plus lines)")
        self.info_2cp.setText("2CP: "+ CLASS +", "+ str(PROB) +", CLASS2, PROB2")
        #plotter.PlotFile(file)
        self.bigFig.draw()

def NavBtn (navigator, msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' waith the target name once we can extract that information
        f.write(f"{navigator.getCurrentFile()}, {msg}\n")
    navigator.updateCursor(delta)
    navigator.loadFile(delta)