from Model import Model

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QProgressBar,
)

from PySide6.QtCore import Slot, Signal

from PySide6.QtGui import QIntValidator

"""
This widget is responsible for letting the user run xpca
"""
class XpcaWidget(QWidget):
    model: Model
    numberBox: QLineEdit
    startButton: QPushButton
    selectButton: QPushButton
    progressBar: QProgressBar
    xpcaDone = Signal(int)

    def __init__(self, model):
        super().__init__()

        self.setWindowTitle('XPCA Wizard')
        self.model = model

        layout = QVBoxLayout()

        self.startButton = QPushButton('Start')
        self.selectButton = QPushButton('Select folder to analyze (may be slow)')
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        self.numberBox = QLineEdit()
        self.numberBox.setValidator(QIntValidator())

        layout.addWidget(QLabel('Run xpca on this amount of files'))
        layout.addWidget(self.numberBox)
        layout.addWidget(self.startButton)
        layout.addWidget(self.selectButton)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

        self.model.openedSession[int].connect(self.setupSession)

    def openFiles(self):
            folder_path = QFileDialog.getExistingDirectory(None, 'Select Folder')
            self.model.fitter.openFiles(folder_path)
            self.close()

    def start(self):
        amount = int(self.numberBox.text())
        self.progressBar.setMaximum(amount)
        self.model.fitter.populate(objs=self.model.objects, N=amount)
        self.xpcaDone.emit(0)
        self.close()
        self.progressBar.setValue(0)
        
    @Slot()
    def setupSession(self, _):
        self.startButton.clicked.connect(lambda: self.start())
        self.selectButton.clicked.connect(lambda: self.openFiles())
        self.model.fitter.fileFitted.connect(self.progressBar.setValue)
        self.numberBox.setValidator(QIntValidator(0, len(self.model.objects)))