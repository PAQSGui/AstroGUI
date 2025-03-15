from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    )
from PySide6.QtGui import (
    #QFileDialog,
    QPalette,
    QColor,
)
from PySide6.QtCore import (
    QSize,
    QDir,
    QDirIterator,
)

from nav import Navigator

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
        midLayout = QHBoxLayout()
        botLayout = self.navigator.layout

        plotLayout = QVBoxLayout()
        rightButtons = QVBoxLayout()

        topLayout.addWidget(Color('green'))
        topLayout.addWidget(Color('yellow'))
        topLayout.addWidget(Color('purple'))

        mainLayout.addLayout(topLayout, 1)
        
        plotLayout.addWidget(Color('green'))
        midLayout.addLayout(plotLayout)

        rightButtons.addWidget(QPushButton("SHOW spectra of STACK"))
        rightButtons.addWidget(QPushButton("Show S/N spec"))
        rightButtons.addWidget(QPushButton('Button to grab: Image cutout (DSS) 100\"x100\"'))
        rightButtons.addWidget(QPushButton("2XP: best-fit template + 1.542..."))
        rightButtons.addWidget(QPushButton("2CP: QSO-MDZ, 0.69..."))
        midLayout.addLayout(rightButtons)
        #midLayout.addWidget(Color('green'))
        #midLayout.addWidget(Color('teal'))

        mainLayout.addLayout(midLayout, 4)

        plotLayout.addWidget(self.navigator.bigFig)

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