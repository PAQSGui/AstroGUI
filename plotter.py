import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from templater import Templater

"""
plotter is more tightly bound to the fits file format.
It should be able to plot files loaded by Spec_tools.py
The template is drawn by another class to achieve a level of modularity
"""
class Plotter:
    model:  Model   
    figure: FigureCanvasQTAgg  
    templater: Templater 

    def __init__(self, model, figure ):
        self.model = model
        self.templater = Templater(model)
        self.figure = figure

    def getYLim(self):
        return self.spectra.ylim()

    def UpdateFigure(self):
        file = self.model.getState().file
        options = self.model.getOptions()
        lineWidth = options['LineWidth']

        plt.figure('k', clear = True)

        if options['yLimit']:
            plt.ylim(int(options['ymin']), int(options['ymax']))        
        else:
            plt.ylim([0,np.max(file.Flux)])

        if options['ShowSN']:
            self.snPlot = plt.step(file.Wavelength, file.Flux/file.Noise, color = options['SNColor'], label="Signal / Noise",  alpha=0.25, linewidth=lineWidth)

        if options['ShowSky']:
            self.skyPlot = plt.step(file.Wavelength, file.Skybackground, color = options['SkyColor'], label="Sky Background",  alpha=0.25, linewidth=lineWidth)

        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')

        noise, = plt.plot(file.Wavelength, file.Noise, label='Noise', color = options['NoiseColor'], alpha=0.5, linewidth=lineWidth)
        spectra, = plt.plot(file.Wavelength, file.Flux, color = options['GraphColor'], linewidth=lineWidth, label = 'Spectra')

        if self.model.getState().fitting!=None:

            template, = self.templater.plotTemplate()
            hands=[spectra, template, noise]
        else:
            hands=[spectra, noise]

        plt.title(file.Objectname)         
        plt.legend(handles=hands)
        self.figure.draw()

