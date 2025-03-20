import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from xpca import plotting
from xpca.targets import Target
from xpca.spectrum import Spectrum
from astropy import units as u

from temppplot import create_PCA_model

def PlotFile(file,fit=None):

    visrange = np.linspace(3800, 7500, 4)

    UpdateFigure(file, 'k', fit=fit)
    UpdateFigure(file,'b', limitPlot = True, range = [visrange[0], visrange[1]])
    UpdateFigure(file,'g', limitPlot = True, range = [visrange[1], visrange[2]])
    UpdateFigure(file,'r', limitPlot = True, range = [visrange[2], visrange[3]])


def UpdateFigure(file, key, limitPlot = False, range = [6250, 7400],targetId=0,targetName="Unknown",fit=None):
    #Unsupported array type
    #targetSpec=Spectrum(u.Quantity(file.Wavelength,u.Angstrom),u.Quantity(file.Flux,u.erg/(u.s*u.cm**2*u.Angstrom)),u.Quantity(file.Noise,u.erg/(u.s*u.cm**2*u.Angstrom)))
    #target=Target(uid=targetId,name=targetName,spectrum=targetSpec)
    #fig=plotting.plot_target(target,fit)
    fig=plt.figure(key)
    plt.clf() #clear figure
    plt.step(file.Wavelength, file.Flux, color = key) #figure key is used for color
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.step(file.Wavelength,file.Noise,label='Noise',color='0.5')
    create_PCA_model(file,fit)
    plt.legend()
    canv=FigureCanvasQTAgg(fig)
    canv.show()

    if limitPlot:
        plt.xlim(range)
    else: 
        plt.title(file.Objectname)  

def ShowSN(file):
    fig = plt.figure()
    plt.step(file.Wavelength, file.Flux/file.Noise)
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux/Noise Ratio')
    plt.title(file.Objectname+" S/N Spectrum")
    canv=FigureCanvasQTAgg(fig)
    canv.show()
