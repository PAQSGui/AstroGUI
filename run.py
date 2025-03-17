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
    QPalette,
    QColor,
    Qt,
)
from PySide6.QtCore import (
    QSize,
)

from nav import Navigator
from ssPicture import LoadPicture
from plotter import ShowSN

# Layout should be top, middle, bottom
# Top is just meta data etc
# Middle is the plots and 'show' buttons
# Bottom is the 'Yes', 'No' etc buttons

class MainWindow(QMainWindow):
    navigator : Navigator
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AstroGUI")

        #layout1.setContentsMargins(0,0,0,0)
        #layout1.setSpacing(20)
        self.navigator = Navigator(0)

        mainLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0,0,0,0)
        topLayout.setSpacing(0)
        midLayout = QHBoxLayout()
        botLayout = self.navigator.layout

        plotLayout = QVBoxLayout()
        rightButtons = QVBoxLayout()

        magLabel = QLabel("What is the DELTA-MAG of -+2 neighbors on the CCD", self)
        magLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        metaLabel = QLabel("Target metadata:\nMAG, MAG_TYPE, target name,\nE(B-V)_gal")
        metaLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        metaLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        topLayout.addWidget(magLabel)
        topLayout.addWidget(metaLabel)
        

        mainLayout.addLayout(topLayout)
        
        midLayout.addLayout(plotLayout)

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        signoiseButton = QPushButton("Show S/N spec")
        rightButtons.addWidget(signoiseButton)
        signoiseButton.clicked.connect(lambda: ShowSN(self.navigator.current))
        
        skygrabButton = QPushButton('Button to grab: Image cutout (DSS) 100\"x100\"')
        rightButtons.addWidget(skygrabButton)
        skygrabButton.clicked.connect(lambda: LoadPicture(self.navigator.directory, self.navigator.getCurrentFile()))
        
        rightButtons.addWidget(self.navigator.info_2cp)
        rightButtons.addWidget(self.navigator.info_2xp)
        midLayout.addLayout(rightButtons)
        #midLayout.addWidget(Color('green'))
        #midLayout.addWidget(Color('teal'))

        mainLayout.addLayout(midLayout, 4)

        plotLayout.addWidget(self.navigator.bigFig) #should bigFig be in a Plotter instead of the Navigator?
        redshiftLayout = QHBoxLayout()
        plotLayout.addLayout(redshiftLayout)
        redshiftLayout.addWidget(QSlider(Qt.Orientation.Horizontal, self))
        templateDropdown = QComboBox()
        templateDropdown.addItem('galaxy-pass')
        templateDropdown.addItem('galaxy')
        templateDropdown.addItem('new-qso-lowz')
        templateDropdown.addItem('new-qso-midz')
        templateDropdown.addItem('qso')
        templateDropdown.addItem('star-A')#add dropdown with templates
        redshiftLayout.addWidget(templateDropdown)

        mainLayout.addLayout(botLayout, 2)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.setMinimumSize(QSize(600, 400))
        self.navigator.openFolder()

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication([])

window = MainWindow()
window.show()



app.exec()