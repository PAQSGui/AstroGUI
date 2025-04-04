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
class TargetData:
    layout: QHBoxLayout
    model: Model

    def __init__(self, model):
        self.model = model
        self.layout = QHBoxLayout()
        self.nbrLabel = QLabel("What is the DELTAMAG of\n-+ 2 neighbors on the CCD")
        self.targetLabel = QLabel()
        self.targetLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.layout.addWidget(self.nbrLabel)
        self.layout.addLayout(self.classProbLayout())
        self.layout.addWidget(self.targetLabel)
        self.updateTargetData()

    def classProbLayout(self):
        classProbLayout = QVBoxLayout()
        classProbLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        data = self.model.getState()
        l2_product = data.fitting

        classification = l2_product['zBestSubType']
        probability    = l2_product['zBestProb'] * 100

        clearLayout(classProbLayout)
        classProbLayout.addWidget(QLabel(classification + ': %.2f %%' % probability))

        subTypes = l2_product['zAltSubType']
        probabilities = l2_product['zAltProb']

        for i in range(1,len(subTypes)):
            probability = probabilities[i] * 100
            if probability > 10:
                text = subTypes[i] + ': %.2f %%' % probability
                classProbLayout.addWidget(QLabel(text))

        return classProbLayout


    # Is supposed to extract target data from FITS file and update the labels accordingly
    def updateTargetData(self):
        #hdu = fits.open(path, ignore_missing_simple=True)
        #name = hdu[0].header['NAME']
    
        # WHY IS THERE NO EBV CARD?
        #ebv = hdu[0].header['EBV']

        # WHERE IS THE MAGNITUDE?
        #mag = hdu[0].header['*MAG*']

        #hdu.close()
        #self.nbrLabel.setText("something with deltamag of neighbors")
        
        # Replace 'Nones' with data extracted from FITS file
        self.targetLabel.setText(f"Target metadata\nNAME: {None}\nMAG: {None}\nMAG TYPE: {None}\nEBV: {None}")

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()
