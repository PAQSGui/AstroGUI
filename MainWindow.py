from NavigateWidget import Navigator
from Fitter import Fitter
from InfoWidget import InfoLayout
from Model import Model
from PlotWidget import PlotLayout
from OptionsWindow import OptionsWindow
from SkyGrabWidget import SkygrabWindow
from xpcaWidget import XpcaWidget

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
    QIcon
)

"""
The main window is responsible for initializing all other classes and linking them.
Model is used to share data and state between the different modules.
Buttons in one class should be linked to methods in other classes via Signals and Slots
This ensures a low level of coupling neccessary for changing out components
"""
class MainWindow(QMainWindow):
    model:          Model
    navigateWidget: Navigator
    plotWidget:     PlotLayout
    fitter:         Fitter
    infoWidget:     InfoLayout
    optionsWindow:  OptionsWindow
    skygrabTab:     SkygrabWindow
    xpcaWindow:     XpcaWidget
        
    def __init__(self, app):
        super().__init__()
        self.model = Model()
        self.setWindowTitle('AstroGUI')

        self.plotWidget = PlotLayout(self.model)
        self.infoWidget = InfoLayout(self.model)
        self.infoWidget.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.navigateWidget = Navigator(self.model)
        self.navigateWidget.layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize) 

        self.optionsWindow = OptionsWindow(self.model)
        self.skygrabTab = SkygrabWindow(self.model)
        self.xpcaWindow = XpcaWidget(self.model)

        self.optionsWindow.optionChanged.connect(self.plotWidget.update)

        self.navigateWidget.navigated.connect(lambda: self.skygrabTab.loadPicture(self.skygrabTab.isVisible()))
        self.navigateWidget.navigated.connect(self.infoWidget.updateAll)
        self.navigateWidget.navigated.connect(self.plotWidget.newFile)

        self.xpcaWindow.xpcaDone.connect(self.infoWidget.updateAll)
        self.xpcaWindow.xpcaDone.connect(self.plotWidget.newFile)

        self.model.openedSession.connect(self.optionsWindow.setupSession)

        mainLayout = QVBoxLayout()
        self.setStatusBar(QStatusBar(self))

        file_menu = self.menuBar()
        file_menu.setNativeMenuBar(False)

        def auxAddButton(icon, tooltip, func):
            button = QAction(icon, tooltip, self)
            button.setStatusTip(tooltip)
            button.setToolTip(tooltip) #seemingly not working, at least not on Linux
            button.triggered.connect(func)
            file_menu.addAction(button)

        auxAddButton(QIcon('icons/folder.png'), 'Open a folder and plot FITS files inside', lambda: self.openFolder())
        auxAddButton(QIcon('icons/hammer.png'), 'Open a window to configure the program', lambda: self.optionsWindow.show())
        auxAddButton(QIcon('icons/robot.png'), 'Open a wizard to process targets using xpca', lambda: self.xpcaWindow.show())
        
        tabs = QTabWidget()
        tabs.addTab(self.plotWidget,'Spectrum Plot')
        tabs.addTab(self.skygrabTab,'SDSS Photo')
    
        tabs.tabBarClicked.connect(lambda: self.skygrabTab.loadPicture(True))

        mainLayout.addLayout(self.infoWidget, stretch=0)
        mainLayout.addWidget(tabs, stretch=5)
        mainLayout.addLayout(self.navigateWidget.layout, stretch=0)
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def openFolder(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(None, 'Select Folder')
            self.model.openFolder(folderPath)
        except FileNotFoundError as error:
            popup = QMessageBox()
            popup.setWindowTitle('Error')
            popup.setText(str(error))
            popup.setIcon(QMessageBox.Icon.Critical)
            popup.exec()

    def closeEvent(self, _):
        self.optionsWindow.close()
        self.xpcaWindow.close()
