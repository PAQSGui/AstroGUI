from nav import Navigator
from ssPicture import LoadPicture
from fitter import Fitter
from InfoLayout import InfoLayout
from Model import Model
from PlotLayout import PlotLayout
from optionsWindow import OptionsWindow

from PySide6.QtWidgets import (
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QStatusBar,
    QLayout,
    )
from PySide6.QtGui import (
    QAction,
    QFont,
)

from PySide6.QtCore import QSize

# Layout should be top, middle, bottom
# Top is just meta data etc
# Middle is the plot
# Bottom is the navigation bottom

class MainWindow(QMainWindow):
    model:      Model
    navigator:  Navigator
    plotLayout: PlotLayout
    fitter:     Fitter
    infoLayout: InfoLayout



    def openFolder(self):
        while True:
            try:
                folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
                if folder_path == "":
                    # Hacky way of exiting program of dialog is cancelled
                    exit()
                self.model = Model(folder_path, True) #We have to make something that actually checks if it has already preprocessed. I spent way too long trying to figure out why my program wasn't working.
            except FileNotFoundError:
                popup = QMessageBox()
                popup.setWindowTitle("Error")
                popup.setText("Folder does not contain any FITS files")
                popup.setIcon(QMessageBox.Icon.Critical)
                popup.exec()
            else:
                break

    def closeEvent(self, ev):
        self.optionsWindow.close()
        
    def __init__(self, app):
        super().__init__()
        self.openFolder()
        self.setWindowTitle("AstroGUI")

        self.plotLayout = PlotLayout(self.model)
        self.infoLayout = InfoLayout(self.model)
        self.infoLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.navigator = Navigator(self.plotLayout, self.infoLayout, self.model)
        self.optionsWindow = OptionsWindow(self.model, self.plotLayout)
        self.navigator.layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        mainLayout = QVBoxLayout()

        self.setStatusBar(QStatusBar(self))
        # add toolbar

        file_menu = self.menuBar()
        file_menu.setFont(QFont("",18))

        def addButton(emoji,tooltip,func=None):
            button = QAction(emoji, self)
            button.setStatusTip(tooltip)
            if func != None:
                button.triggered.connect(func)
            file_menu.addAction(button)


        addButton("📂","Open a folder and plot FITS files inside",lambda: self.openFolder())
        addButton("⚙️","Open a window to configure the program",lambda: self.optionsWindow.show())
        addButton("🌌","Load image cutout from the Sloan Digital Sky Survey (SDSS)",lambda: LoadPicture(self.model))
        
        file_menu.addAction(QAction("ᴹⁱˢˢⁱⁿᵍ⌥", self))
        
        addButton("💾","Save current workspace")
        addButton("📜","Review evaluated spectra")
        addButton("🥞","Load other spectra of the same object and overplot them for comparison")
        addButton("🌇","Open a window to correct for telluric absorption and interstellar extinction")
        addButton("🌈","Open a wizard to merge a set of grisms into a single spectrum")
        addButton("🏭","Open a wizard to process targets using xpca")
        addButton("🗠","Open a window to manually adjust the template parameters")
        
        mainLayout.addLayout(self.infoLayout)
        mainLayout.addLayout(self.plotLayout.layout)
        mainLayout.addLayout(self.navigator.layout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
