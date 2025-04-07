from nav import Navigator
from ssPicture import LoadPicture
from fitter import Fitter
from InfoLayout import InfoLayout
from Model import Model
from PlotLayout import PlotLayout

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
                self.model = Model(folder_path, True)
            except FileNotFoundError:
                popup = QMessageBox()
                popup.setWindowTitle("Error")
                popup.setText("Folder does not contain any FITS files")
                popup.setIcon(QMessageBox.Icon.Critical)
                popup.exec()
            else:
                break

    def __init__(self, app):
        super().__init__()
        self.openFolder()
        self.setWindowTitle("AstroGUI")

        self.plotLayout = PlotLayout(self.model)
        self.infoLayout = InfoLayout(self.model)
        self.infoLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.navigator = Navigator(self.plotLayout, self.model)
        self.navigator.layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        mainLayout = QVBoxLayout()

        self.setStatusBar(QStatusBar(self))
        # add toolbar

        file_menu = self.menuBar()
        file_menu.setFont(QFont("",18))

        button_open = QAction("📂", self)
        button_open.setStatusTip("Open a folder and plot FITS files inside")
        button_open.triggered.connect(lambda: self.openFolder())
        file_menu.addAction(button_open)

        button_options = QAction("⚙️", self)
        button_options.setStatusTip("Open a window to configure the program")
        button_options.triggered.connect(lambda: self.plotLayout.optionsWindow())
        file_menu.addAction(button_options)

        button_stack = QAction("🥞", self)
        button_stack.setStatusTip("Load other spectra of the same object and overplot them for comparison")
        file_menu.addAction(button_stack)

        # configure the bottom layout
        botLayout = QHBoxLayout()
        botLayout.addLayout(self.navigator.layout)
        skygrabButton = QAction("🌌", self)
        skygrabButton.setStatusTip('Load image cutout from the Sloan Digital Sky Survey (SDSS)')
        skygrabButton.triggered.connect(lambda: LoadPicture(self.model))
        file_menu.addAction(skygrabButton)

        mainLayout.addLayout(self.infoLayout)
        mainLayout.addLayout(self.plotLayout.layout)
        mainLayout.addLayout(botLayout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
