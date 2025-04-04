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

# Class represents the top of the program and contains the labels used to display meta information
class TargetData:
    def __init__(self, fitter):
        self.layout = QHBoxLayout()
        self.nbrLabel = QLabel("What is the DELTAMAG of\n-+ 2 neighbors on the CCD")
        self.targetLabel = QLabel()
        self.targetLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.layout.addWidget(self.nbrLabel)
        self.layout.addLayout(fitter.layout)
        self.layout.addWidget(self.targetLabel)

    # Is supposed to extract target data from FITS file and update the labels accordingly
    def updateTargetData(self, path):
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