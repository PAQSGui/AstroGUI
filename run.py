from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    )
from PySide6.QtGui import (
    QAction,
    Qt,
)
from nav import Navigator
from ssPicture import LoadPicture
from plotter import Plotter
from fitter import Fitter

# Layout should be top, middle, bottom
# Top is just meta data etc
# Middle is the plots and 'show' buttons
# Bottom is the 'Yes', 'No' etc buttons

class MainWindow(QMainWindow):
    navigator:  Navigator
    plotter:    Plotter
    fitter:     Fitter

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AstroGUI")
        self.plotter = Plotter()
        self.fitter = Fitter()
        self.navigator = Navigator(0, self.plotter, self.fitter)

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


        # configure the top layout
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0,0,0,0)
        topLayout.setSpacing(0)

        magLabel = QLabel("What is the DELTA-MAG of -+2 neighbors on the CCD", self)
        magLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        metaLabel = QLabel("Target metadata:\nMAG, MAG_TYPE, target name,\nE(B-V)_gal")
        metaLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        metaLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        topLayout.addWidget(magLabel)
        topLayout.addWidget(metaLabel)
        
        # configure the middle layout
        midLayout = QHBoxLayout()

        rightButtons = QVBoxLayout()

        signoiseButton = QPushButton("Show S/N spec")
        signoiseButton.clicked.connect(lambda: Plotter(self.navigator.current).showSN())

        skygrabButton = QPushButton('Image cutout (DSS) 100\"x100\"')        
        skygrabButton.clicked.connect(lambda: LoadPicture(self.navigator.directory, self.navigator.getCurrentFile()))

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        rightButtons.addWidget(signoiseButton)
        rightButtons.addWidget(skygrabButton)
        rightButtons.addLayout(self.fitter.layout)

        midLayout.addLayout(self.plotter.layout)
        midLayout.addLayout(rightButtons) 

        # configure the bottom layout
        botLayout = self.navigator.layout

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(midLayout)
        mainLayout.addLayout(botLayout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.navigator.openFolder()

app = QApplication([])

window = MainWindow()
window.show()

app.exec()