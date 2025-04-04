from nav import Navigator
from ssPicture import LoadPicture
from plotter import Plotter
from fitter import Fitter
from file_handling import TargetData
from Model import Model

from PySide6.QtWidgets import (
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    )
from PySide6.QtGui import (
    QAction,
)

# Layout should be top, middle, bottom
# Top is just meta data etc
# Middle is the plot
# Bottom is the navigation bottom

class MainWindow(QMainWindow):
    model:      Model
    navigator:  Navigator
    plotter:    Plotter
    fitter:     Fitter
    targetData: TargetData

    def __init__(self):
        super().__init__()

        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        self.model = Model(folder_path, True)
        self.setWindowTitle("AstroGUI")

        self.plotter = Plotter(self.model)
        self.targetData = TargetData(self.model.fitter)
        self.navigator = Navigator(self.plotter, self.model)

        mainLayout = QVBoxLayout()

        # add toolbar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        button_open = QAction("Open Folder", self)
        button_open.setStatusTip("Open a folder and plot FITS files inside")
        button_open.triggered.connect(lambda: self.navigator.openFolder())
        file_menu.addAction(button_open)

        button_options = QAction("Options", self)
        button_options.setStatusTip("Open a window to configure the program")
        button_options.triggered.connect(lambda: self.plotter.optionsWindow())
        file_menu.addAction(button_options)

        button_quit = QAction("Exit", self)
        button_quit.setStatusTip("Exit program")
        button_quit.triggered.connect(lambda: app.quit())
        file_menu.addAction(button_quit)

        # configure the middle layout
        midLayout = QHBoxLayout()
        midLayout.addLayout(self.plotter.layout)

        # configure the bottom layout
        botLayout = QHBoxLayout()
        botLayout.addLayout(self.navigator.layout)
        
        rightButtons = QVBoxLayout()

        signoiseButton = QPushButton("Toggle S/N spec")
        signoiseButton.clicked.connect(lambda: self.plotter.toggleSN())

        skygrabButton = QPushButton('Image cutout (DSS) 100\"x100\"')        
        skygrabButton.clicked.connect(lambda: LoadPicture(self.navigator.directory, self.navigator.getCurrentFile()))

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        rightButtons.addWidget(signoiseButton)
        rightButtons.addWidget(skygrabButton)
        botLayout.addLayout(rightButtons)

        mainLayout.addLayout(self.targetData.layout)
        mainLayout.addLayout(midLayout)
        mainLayout.addLayout(botLayout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
