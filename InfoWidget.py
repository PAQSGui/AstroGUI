from Model import Model
from SkyGrabWidget import loadCoords

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QWidget,
    QGroupBox,
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
        central = QWidget()
        self.addWidget(central)

        margins = self.layout.contentsMargins()
        margins.setBottom(0)
        self.layout.setContentsMargins(margins)
        
        central.setLayout(self.layout)
        central.setMaximumSize(QSize(9999999, 150))

        self.model = model
        self.nbrLabel = QLabel("DELTAMAG of\n-+ 2 neighbors on the CCD")
        self.targetLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.classProbLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

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
        self.nbrLabel = QLabel("DELTAMAG of\n-+ 2 neighbors on the CCD")

    def updateClassProb(self):
        clearLayout(self.classProbLayout)
        layout = QVBoxLayout()
        groupBox = QGroupBox('Class, Probability:')
        groupBox.setLayout(layout)

        data = self.model.getState()
        l2_product = data.fitting
        if l2_product!=None:

            classification = l2_product['zBestSubType']
            probability    = l2_product['zBestProb'] * 100

            subTypes = l2_product['zAltSubType']
            probabilities = l2_product['zAltProb']

            layout.addWidget(QLabel(classification + ': %.2f %%' % probability))

            for i in range(1,len(subTypes)):
                if probabilities[i]!=None:
                    probability = probabilities[i] * 100
                    if probability > 10:
                        text = subTypes[i] + ': %.2f %%' % probability
                        layout.addWidget(QLabel(text))
        self.classProbLayout.addWidget(groupBox)
                        
    
    def updateTarget(self):
        clearLayout(self.targetLayout)
        layout = QGridLayout()
        groupBox = QGroupBox('Metadata')
        groupBox.setLayout(layout)

        layout.addWidget(QLabel("Mag"), 1, 1)
        layout.addWidget(QLabel("MAG Type"), 2, 1)
        layout.addWidget(QLabel("EBV"), 3, 1)
        ra, dec = loadCoords(self.model)
        layout.addWidget(QLabel(f"RA: {ra:.4f}"), 1, 2)
        layout.addWidget(QLabel(f"DEC: {dec:.4f}"), 2, 2)

        self.targetLayout.addWidget(groupBox)

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()
