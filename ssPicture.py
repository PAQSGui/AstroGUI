from astropy.io.fits import getheader
from matplotlib import pyplot as plt
from sdss import Region
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide6.QtCore import QDir
def Show(region, band='all', figsize=None):
    #Shamelessly copied from Behrouz' own implementation
    if region.data is None:
        region.download_data()
    if isinstance(figsize, tuple) and len(figsize)==2:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()
    if band=='i':
        ax.imshow(region.data[:,:,0], cmap='gray')
    elif band=='r':
        ax.imshow(region.data[:,:,1], cmap='gray')
    elif band=='g':
        ax.imshow(region.data[:,:,2], cmap='gray')
    else:
        ax.imshow(region.data)
    plt.axis('off') # new
    canv=FigureCanvasQTAgg(fig)
    canv.show()

def LoadPicture(model):
    dir = QDir(model.path)
    file = model.getState().name
    header = getheader(dir.absoluteFilePath(file))
    ra = header['RA']
    dec = header['DEC']
    #https://github.com/behrouzz/sdss
    reg = Region(ra, dec, fov=0.033)
    print(reg.nearest_objects())
    
    Show(reg)