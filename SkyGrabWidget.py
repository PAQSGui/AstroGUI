from astropy.io.fits import getheader
from matplotlib import pyplot as plt
from sdss import Region
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtCore import QDir, Slot
from Model import Model

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

"""
This class is responsible for grabbing an image of the sky from sdss, with the currently viewed object centered
"""
class SkygrabWindow(QWidget):
    ax: plt.Axes
    canv: FigureCanvasQTAgg
    model: Model
    loadedFile=None

    def __init__(self, model):
        super().__init__()
        self.model = model
        fig, self.ax = plt.subplots()
        self.canv=FigureCanvasQTAgg(fig)
        layout = QVBoxLayout()
        #add labels describing the object and its coordinates
        layout.addWidget(self.canv)
        self.setLayout(layout)

    @Slot()
    def LoadPicture(self, visible):
        file = self.model.getState().file
        if not visible or file==self.loadedFile:
            return
        ra,dec=loadCoords(self.model)
        #https://github.com/behrouzz/sdss
        reg = Region(ra, dec, fov=0.033)
        
        self.Update(reg)

        plt.title(file.Objectname)  
        self.canv.draw()
        self.loadedFile=file
        #self.show()

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

def loadCoords(model):
        dir = QDir(model.path)
        file = model.getState().path
        header = getheader(file)
        ra = header['PLUG_RA']
        dec = header['PLUG_DEC']
        return ra,dec
