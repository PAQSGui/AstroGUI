import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

from astropy.io.fits import getdata
from astropy.io.fits import getheader

def PlotFile(file, template):

    visrange = np.linspace(3800, 7500, 4)

    UpdateFigure(file, 'k', template)
    UpdateFigure(file,'b', template, limitPlot = True, range = [visrange[0], visrange[1]])
    UpdateFigure(file,'g', template, limitPlot = True, range = [visrange[1], visrange[2]])
    UpdateFigure(file,'r', template, limitPlot = True, range = [visrange[2], visrange[3]])


def UpdateFigure(file, key, template, limitPlot = False, range = [6250, 7400]):
    plt.figure(key)
    plt.clf() #clear figure
    plt.step(file.Wavelength, file.Flux, color = key) #figure key is used for color
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.step(file.Wavelength,file.Noise,label='Noise',color='0.5')
    DrawTemplate(key, template)
    plt.legend()

    if limitPlot:
        plt.xlim(range)
    else: 
        plt.title(file.Objectname)  


def ShowSN(file,tkroot):
    rootFrame = tk.Toplevel(tkroot)
    rootFrame.title('S/N Spectrum')
    fig = plt.figure()
    plt.step(file.Wavelength, file.Flux/file.Noise)
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux/Noise Ratio')
    plt.title(file.Objectname+" S/N Spectrum")
    canv=tkplot.FigureCanvasTkAgg(fig, rootFrame)
    canv.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

def DrawTemplate(key, template): # add filename
    plt.figure(key)
    file = "/home/sofus/Documents/bach/AstroGUI/templates/template-galaxy.fits"

    # adjust for redshift?



def GetFileName(template):
    if template == 'GALAXY':
        return "templates/template-galaxy-pass.fits"
    elif template == 'GALAXY-PASS':
        return "templates/template-galaxy.fits"
    elif template == 'QSO-LOWZ':
        return  "templates/template-new-qso-lowz.fits"
    elif template == 'QSO-MIDZ':
        return "templates/template-new-qso-midz.fits"
    elif template == 'QSO':
        return "templates/template-qso.fits"
    else:
        return "templates/template-star-A.fits"