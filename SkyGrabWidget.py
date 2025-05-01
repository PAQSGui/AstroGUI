from astropy.io.fits import getheader
from matplotlib import pyplot as plt
from sdss import Region
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from Model import Model

from PySide6.QtCore import Slot

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

"""
This class is responsible for grabbing an image of the sky from sdss, with the currently viewed object centered
"""
class SkygrabWindow(QWidget):
    axis: plt.Axes
    canvas: FigureCanvasQTAgg
    model: Model
    loadedFile = None

    def __init__(self, model):
        super().__init__()
        self.model = model
        fig, self.axis = plt.subplots()
        self.canvas = FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    @Slot()
    def loadPicture(self, visible):
        file = self.model.getState().file
        if not visible or file == self.loadedFile:
            return
        ra, dec = loadCoords(self.model)
        reg = Region(ra, dec, fov=0.033)
        
        self.update(reg)

        plt.title(file.Objectname)  
        self.canvas.draw()
        self.loadedFile = file

    """
    Copied from Behrouz' implementation:
    https://github.com/behrouzz/sdss
    """
    def update(self, region, band='all'):
        if region.data is None:
            region.download_data()
        if band == 'i':
            self.axis.imshow(region.data[:,:,0], cmap='gray')
        elif band == 'r':
            self.axis.imshow(region.data[:,:,1], cmap='gray')
        elif band == 'g':
            self.axis.imshow(region.data[:,:,2], cmap='gray')
        else:
            self.axis.imshow(region.data)
        plt.axis('off')

def loadCoords(model):
        file = model.getState().path
        header = getheader(file)
        ra = header['PLUG_RA']
        dec = header['PLUG_DEC']
        return ra, dec
