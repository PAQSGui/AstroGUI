from astropy.io import fits

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

from Model import Model

# Class represents the top of the program and contains the labels used to display meta information
class InfoLayout:
    layout = QHBoxLayout()
    model: Model
    nbrLabel: QLabel
    classProbLayout = QVBoxLayout()
    targetLayout = QVBoxLayout()

    def __init__(self, model):

        self.model = model
        self.nbrLabel = QLabel("What is the DELTAMAG of\n-+ 2 neighbors on the CCD")
        self.targetLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.layout.addWidget(self.nbrLabel)
        self.layout.addLayout(self.classProbLayout)
        self.layout.addLayout(self.targetLayout)
        self.updateAll()
    
    def updateNbrLabel(self):
        self.nbrLabel = QLabel("What is the DELTAMAG of\n-+ 2 neighbors on the CCD")

    def updateClassProb(self):
        self.classProbLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        data = self.model.getState()
        l2_product = data.fitting

        classification = l2_product['zBestSubType']
        probability    = l2_product['zBestProb'] * 100

        clearLayout(self.classProbLayout)
        self.classProbLayout.addWidget(QLabel(classification + ': %.2f %%' % probability))

        subTypes = l2_product['zAltSubType']
        probabilities = l2_product['zAltProb']

        for i in range(1,len(subTypes)):
            probability = probabilities[i] * 100
            if probability > 10:
                text = subTypes[i] + ': %.2f %%' % probability
                self.classProbLayout.addWidget(QLabel(text))

        return self.classProbLayout
    
    def updateTarget(self):
        self.targetLayout.addWidget(QLabel("Target metadata:"))
        self.targetLayout.addWidget(QLabel("Mag"))
        self.targetLayout.addWidget(QLabel("MAG Type"))
        self.targetLayout.addWidget(QLabel("EBV"))

    def updateAll(self):
        self.updateNbrLabel()
        self.updateClassProb()
        self.updateTarget()

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()
