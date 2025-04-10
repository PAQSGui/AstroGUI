import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from Model import Model
from templater import Templater

class Plotter:
    model:  Model   
    figure: FigureCanvasQTAgg  
    templater: Templater 
    showSN = True
    showSky = True

    def __init__(self, model, figure ):
        self.model = model
        self.templater = Templater(model)
        self.figure = figure

    def UpdateGrism(self, spectra=None):
        plt.figure('k')
        if spectra==None:
            spectra=self.model.getState().file
        plt.clf() #clear figure
        colorcodes = ['k','r','g','b']
        for x in [0,1,2,3]:
            if spectra[x]!=None:
                self.DrawPlot(spectra[x],colorcodes[x])

        plt.legend()
        self.figure.draw()

    def UpdateFigure(self, key='k'):
        file = self.model.getState().file
        plt.figure('k')
        plt.clf()
        self.DrawPlot(file,key)
        self.templater.plotTemplate()
        plt.title(file.Objectname)  
        plt.legend
        self.figure.draw()
        
    def DrawPlot(self,data,colorcode):
        lineWidth = self.model.getOption('LineWidth')
        plt.step(data.Wavelength, data.Flux, color = self.model.getOption('GraphColor'), linewidth=lineWidth) #figure key is used for color

        if self.showSN:
            plt.step(data.Wavelength, data.Flux/data.Noise, color = self.model.getOption('SNColor'), label="Signal / Noise",  alpha=0.25, linewidth=lineWidth)

        if self.showSky:
            plt.step(data.Wavelength, data.Skybackground, color = self.model.getOption('SkyColor'), label="Sky Background",  alpha=0.25, linewidth=lineWidth)

        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')

        plt.ylim([0,np.max(data.Flux)])
        plt.step(data.Wavelength, data.Noise, label='Noise', color = self.model.getOption('NoiseColor'), alpha=0.5, linewidth=lineWidth)
