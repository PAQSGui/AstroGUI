from Navigator import Navigator
from fitter import Fitter
from Layout_Info import InfoLayout
from Model import Model
from PlotLayout import PlotLayout
from optionsWindow import OptionsWindow
from ssPicture import SkygrabWindow

from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QStatusBar,
    QLayout,
    QTabWidget,
    )
from PySide6.QtGui import (
    QAction,
    QFont,
    QIcon
)

from handler_xpca import xpcaWindow

"""
The main window is resposinble for initializing all other classes and linking them.
Model is used to share data and state between the different modules.
Buttons in one class should be linked to methods in other classes via Signals and Slots
This ensures a low level of coupling neccessary for changing out components
"""
class MainWindow(QMainWindow):

    model:          Model
    navigator:      Navigator
    plotLayout:     PlotLayout
    fitter:         Fitter
    infoLayout:     InfoLayout
    optionsWindow:  OptionsWindow
    skygrabTab:     SkygrabWindow

    def openFolder(self):
                folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
                if folder_path == "":
                    # Hacky way of exiting program if dialog is cancelled
                    exit()
                self.model = Model(folder_path) #We have to make something that actually checks if it has already preprocessed. I spent way too long trying to figure out why my program wasn't working.

    def openFiles(self):
            files = QFileDialog.getOpenFileNames(None, "Select Files")
            self.model.openFiles(files[0])

    def saveFiles(self):
            path = QFileDialog.getSaveFileName(None, "Save as...")
            with open(path[0], 'w') as file:
                self.model.preProcess.savedataFrameToFile(file)

    def closeEvent(self, ev):
        self.optionsWindow.close()
        self.xpcaWindow.close()
        
    def __init__(self, app):
        super().__init__()
        self.model = Model()
        #self.openFiles()
        self.setWindowTitle("AstroGUI")

        self.plotLayout = PlotLayout(self.model)
        self.infoLayout = InfoLayout(self.model)
        self.infoLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.navigator = Navigator(self.model)
        self.navigator.layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.navigator.navigated.connect(self.infoLayout.updateAll)
        self.navigator.navigated.connect(self.plotLayout.newFile)
        self.model.xpcaDone.connect(self.infoLayout.updateAll)
        self.model.xpcaDone.connect(self.plotLayout.newFile)

        self.optionsWindow = OptionsWindow(self.model)
        self.optionsWindow.optionChanged.connect(self.plotLayout.update)
        self.skygrabTab = SkygrabWindow(self.model)
        self.navigator.navigated.connect(self.skygrabTab.LoadPicture)

        self.xpcaWindow = xpcaWindow(self.model)
        mainLayout = QVBoxLayout()

        self.setStatusBar(QStatusBar(self))

        file_menu = self.menuBar()
        file_menu.setFont(QFont("",18))

        def addButton(icon,tooltip,func=None):
            button = QAction(icon,tooltip, self)
            button.setStatusTip(tooltip)
            button.setToolTip(tooltip) #seemingly not working, at least not on Linux
            if func != None:
                button.triggered.connect(func)
            file_menu.addAction(button)


        addButton(QIcon("icons/folder.png"),"Open a folder and plot FITS files inside",lambda: self.openFiles())
        addButton(QIcon("icons/hammer.png"),"Open a window to configure the program",lambda: self.optionsWindow.show())
        
        #file_menu.addAction(QAction("ᴹⁱˢˢⁱⁿᵍ⌥", self))
        
        addButton(QIcon("icons/floppy.png"),"Save current workspace",lambda: self.saveFiles())
        #addButton("📜","Review evaluated spectra")
        #addButton("🥞","Load other spectra of the same object and overplot them for comparison")
        #addButton("🌇","Open a window to correct for telluric absorption and interstellar extinction")
        #addButton("🌈","Open a wizard to merge a set of grisms into a single spectrum")
        addButton(QIcon("icons/robot.png"),"Open a wizard to process targets using xpca",lambda: self.xpcaWindow.show())
        #addButton("🗠","Open a window to manually adjust the template parameters")
        
        mainLayout.addLayout(self.infoLayout)
        tabs = QTabWidget()
        tabs.addTab(self.plotLayout,"Spectrum Plot")
        tabs.addTab(self.skygrabTab,"SDSS Photo")
    
        tabs.tabBarClicked.connect(self.skygrabTab.LoadPicture)
        mainLayout.addWidget(tabs)
        mainLayout.addLayout(self.navigator.layout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
