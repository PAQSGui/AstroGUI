from Model import Model
from ssPicture import loadCoords

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from PySide6.QtGui import (
    Qt,
)

from PySide6.QtCore import QSize, Slot
"""
This component is placed at the top of the window and displays meta-data from the file.
It should handle files as loaded by Spec_tools.py
"""
class InfoLayout(QHBoxLayout):
    layout = QHBoxLayout()
    model: Model
    nbrLabel: QLabel
    classProbLayout = QVBoxLayout()
    targetLayout = QVBoxLayout()

    def __init__(self, model):
        super().__init__()
        central=QWidget()
        self.addWidget(central)
        
        central.setLayout(self.layout)
        central.setMaximumSize(QSize(9999999, 150))

        self.model = model
        self.nbrLabel = QLabel("What is the DELTAMAG of\n-+ 2 neighbors on the CCD")
        self.targetLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.layout.addWidget(self.nbrLabel)
        self.layout.addLayout(self.classProbLayout)
        self.layout.addLayout(self.targetLayout)
        self.model.openedSession[list].connect(self.updateAll)
    
    @Slot()
    def updateAll(self):
        self.updateNbrLabel()
        self.updateClassProb()
        self.updateTarget()

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
            if probabilities[i]!=None:
                probability = probabilities[i] * 100
                if probability > 10:
                    text = subTypes[i] + ': %.2f %%' % probability
            else:
                text = "%s: NaN" % subTypes[i]
            self.classProbLayout.addWidget(QLabel(text))

        return self.classProbLayout
    
    def updateTarget(self):
        clearLayout(self.targetLayout)
        self.targetLayout.addWidget(QLabel("Target metadata:"))
        self.targetLayout.addWidget(QLabel("Mag"))
        self.targetLayout.addWidget(QLabel("MAG Type"))
        self.targetLayout.addWidget(QLabel("EBV"))
        ra,dec=loadCoords(self.model)
        self.targetLayout.addWidget(QLabel(f"RA: {ra:.4f}, DEC: {dec:.4f}"))

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()
