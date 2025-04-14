from astropy.io.fits import getheader
from matplotlib import pyplot as plt
from sdss import Region
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtCore import QDir

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)

class SkygrabWindow(QWidget):
    ax: plt.Axes
    coords: QLabel
    canv: FigureCanvasQTAgg

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDSS Sky Picture")
        fig, self.ax = plt.subplots()
        #if isinstance(figsize, tuple) and len(figsize)==2:
        #    fig, self.ax = plt.subplots(figsize=figsize)
        #else:
        #    fig, self.ax = plt.subplots()
        self.canv=FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        #add labels describing the object and its coordinates
        self.coords=QLabel("Write the object's coords here")
        layout.addWidget(self.canv)
        layout.addWidget(self.coords)
        self.setLayout(layout)

    def LoadPicture(self,model):
        dir = QDir(model.path)
        file = model.getState().name
        header = getheader(dir.absoluteFilePath(file))
        ra = header['PLUG_RA']
        dec = header['PLUG_DEC']
        self.coords.setText(f"RA: {ra}, DEC: {dec}")
        #https://github.com/behrouzz/sdss
        reg = Region(ra, dec, fov=0.033)
        
        self.Update(reg)

        self.show()

    
    def Update(self, region, band='all'):
        #Shamelessly copied from Behrouz' own implementation
        if region.data is None:
            region.download_data()
        if band=='i':
            self.ax.imshow(region.data[:,:,0], cmap='gray')
        elif band=='r':
            self.ax.imshow(region.data[:,:,1], cmap='gray')
        elif band=='g':
            self.ax.imshow(region.data[:,:,2], cmap='gray')
        else:
            self.ax.imshow(region.data)
        plt.axis('off') # new
        self.canv.draw()