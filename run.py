from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QComboBox,
    QSizePolicy,
    )
from PySide6.QtGui import (
    Qt,
)
from PySide6.QtCore import (
    QSize,
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

        plotLayout = QVBoxLayout()

        redshiftLayout = QHBoxLayout()
        
        redshiftLayout.addWidget(QSlider(Qt.Orientation.Horizontal, self))
        templateDropdown = QComboBox()
        dropdown_opts = ['galaxy-pass', 'galaxy', 'new-qso-lowz', 'new-qso-midz', 'qso', 'star-A']
        for opt in dropdown_opts:
            templateDropdown.addItem(opt)
        redshiftLayout.addWidget(templateDropdown)

        plotLayout.addLayout(redshiftLayout)
        plotLayout.addLayout(self.plotter.layout)

        rightButtons = QVBoxLayout()

        label_2cp = QLabel(self.fitter.info_2cp, wordWrap=True)
        label_2xp = QLabel(self.fitter.info_2xp, wordWrap=True)

        signoiseButton = QPushButton("Show S/N spec")
        signoiseButton.clicked.connect(lambda: Plotter(self.navigator.current).showSN())

        skygrabButton = QPushButton('Image cutout (DSS) 100\"x100\"')        
        skygrabButton.clicked.connect(lambda: LoadPicture(self.navigator.directory, self.navigator.getCurrentFile()))

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        rightButtons.addWidget(signoiseButton)
        rightButtons.addWidget(skygrabButton)
        rightButtons.addWidget(label_2cp)
        rightButtons.addWidget(label_2xp)

        midLayout.addLayout(plotLayout)
        midLayout.addLayout(rightButtons)     

        # configure the bottom layout
        botLayout = self.navigator.layout

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(midLayout)
        mainLayout.addLayout(botLayout)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        #self.setMinimumSize(QSize(800, 800))
        self.navigator.openFolder()

app = QApplication([])

window = MainWindow()
window.show()



app.exec()