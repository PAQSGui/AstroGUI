import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from templater import Templater

class Plotter:
    model:  Model   
    figure: FigureCanvasQTAgg  
    templater: Templater 

    def __init__(self, model, figure ):
        self.model = model
        self.templater = Templater(model)
        self.figure = figure

    def getYLim(self):
        return plt.ylim()

    def UpdateFigure(self, key='k'):
        file = self.model.getState().file
        plt.figure('k')
        plt.clf()
        self.DrawPlot(file)
        self.templater.plotTemplate()
        plt.title(file.Objectname)  
        plt.legend()
        self.figure.draw()
        
    def DrawPlot(self, data):
        options = self.model.getOptions()

        lineWidth = options['LineWidth']

        if options['yLimit']:
            plt.ylim(int(options['ymin']), int(options['ymax']))

        plt.step(data.Wavelength, data.Flux, color = options['GraphColor'], linewidth=lineWidth)

        if options['ShowSN']:
            plt.step(data.Wavelength, data.Flux/data.Noise, color = options['SNColor'], label="Signal / Noise",  alpha=0.25, linewidth=lineWidth)

        if options['ShowSky']:
            plt.step(data.Wavelength, data.Skybackground, color = options['SkyColor'], label="Sky Background",  alpha=0.25, linewidth=lineWidth)

        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')

        if not options['yLimit']:
            plt.ylim([0,np.max(data.Flux)])
        plt.step(data.Wavelength, data.Noise, label='Noise', color = options['NoiseColor'], alpha=0.5, linewidth=lineWidth)
