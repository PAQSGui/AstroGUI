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
    QToolBar,
    )
from PySide6.QtGui import (
    QAction,
    QIcon,
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
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        self.model = Model(folder_path, False)

    def __init__(self, app):
        super().__init__()

        self.openFolder()
        self.setWindowTitle("AstroGUI")

        self.plotLayout = PlotLayout(self.model)
        self.infoLayout = InfoLayout(self.model)
        self.navigator = Navigator(self.plotLayout, self.model)

        mainLayout = QVBoxLayout()

        # add toolbar

        file_menu = QToolBar("My main toolbar")
        file_menu.setIconSize(QSize(16, 16))
        self.addToolBar(file_menu)

        button_open = QAction(QIcon("img/fasil-freeicons.io-folder.png"), "Open Folder", self)
        button_open.setStatusTip("Open a folder and plot FITS files inside")
        button_open.triggered.connect(lambda: self.openFolder())
        file_menu.addAction(button_open)

        button_options = QAction(QIcon("img/fasil-freeicons.io-options.png"), "Options", self)
        button_options.setStatusTip("Open a window to configure the program")
        button_options.triggered.connect(lambda: self.plotLayout.optionsWindow())
        file_menu.addAction(button_options)

        # configure the bottom layout
        botLayout = QHBoxLayout()
        botLayout.addLayout(self.navigator.layout)
        
        rightButtons = QVBoxLayout()

        signoiseButton = QPushButton("Toggle S/N spec")
        signoiseButton.clicked.connect(lambda: self.plotLayout.toggleSN())

        skygrabButton = QPushButton('Image cutout (DSS) 100\"x100\"')        
        skygrabButton.clicked.connect(lambda: LoadPicture(self.navigator.directory, self.navigator.getCurrentFile()))

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        rightButtons.addWidget(signoiseButton)
        rightButtons.addWidget(skygrabButton)
        botLayout.addLayout(rightButtons)

        mainLayout.addLayout(self.infoLayout.layout)
        mainLayout.addLayout(self.plotLayout.layout)
        mainLayout.addLayout(botLayout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
