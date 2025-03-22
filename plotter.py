import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
import Spec_tools as tool
import templater

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    )

class Plotter:

    layout: QHBoxLayout 
    file: tool.SDSS_spectrum
    bigFig : FigureCanvasQTAgg

    def __init__(self):
        self.layout = QHBoxLayout()
        self.bigFig = FigureCanvasQTAgg(figure('k'))
        self.layout.addWidget(self.bigFig)


    def addFile(self, file, template):
        self.file = file
        self.PlotFile(template)

    def PlotFile(self, template = 'EMPTY'):

        visrange = np.linspace(3800, 7500, 4)

        self.UpdateFigure('k')
        #self.UpdateFigure(self.file,'b', limitPlot = True, range = [visrange[0], visrange[1]])
        #self.UpdateFigure(self.file,'g', limitPlot = True, range = [visrange[1], visrange[2]])
        #self.UpdateFigure(self.file,'r', limitPlot = True, range = [visrange[2], visrange[3]])

        if template != 'EMPTY':
            templater.DrawTemplate(template, 'k')
        plt.legend()
        self.bigFig.draw()


    def UpdateFigure(self, key, limitPlot = False, range = [6250, 7400]):
        plt.figure(key)
        plt.clf() #clear figure
        plt.step(self.file.Wavelength, self.file.Flux, color = key) #figure key is used for color
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.file.Wavelength, self.file.Noise, label='Noise', color='0.5')

        if limitPlot:
            plt.xlim(range)
        else: 
            plt.title(self.file.Objectname)  

    def ShowSN(file):
        fig = plt.figure()
        plt.step(file.Wavelength, file.Flux/file.Noise)
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux/Noise Ratio')
        plt.title(file.Objectname+" S/N Spectrum")
        canv=FigureCanvasQTAgg(fig)
        canv.show()
