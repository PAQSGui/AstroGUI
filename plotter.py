import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

def PlotFile(file):

    visrange = np.linspace(3800, 7500, 4)

    UpdateFigure(file, 'k')
    UpdateFigure(file,'b', limitPlot = True, range = [visrange[0], visrange[1]])
    UpdateFigure(file,'g', limitPlot = True, range = [visrange[1], visrange[2]])
    UpdateFigure(file,'r', limitPlot = True, range = [visrange[2], visrange[3]])


def UpdateFigure(file, key, limitPlot = False, range = [6250, 7400], width = 0.5):
    plt.figure(key)
    plt.clf() #clear figure
    plt.step(file.Wavelength, file.Flux, color = key, linewidth=width) #figure key is used for color
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.step(file.Wavelength,file.Noise,label='Noise',color='0.5', linewidth=width)
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
