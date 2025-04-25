import matplotlib.pyplot as plt
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template
from Model import Model

from re import search
"""
templater uses xpca to draw a template over the plot
"""
class Templater:
    model: Model

    def __init__(self, model):
        self.model = model

    """
    Tries to find a redshift matching the selected category in zAlt.
    """

    def plotTemplate(self):

        state = self.model.getState()
        spec = state.file
        l2_product = state.fitting
        
        l2_product['zBest'] = self.model.getRedShift()
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        
        try:
            wave, model = template.create_PCA_model(target, l2_product)
        except FileNotFoundError as e: #replace with a file exists check
            name = l2_product['zBestSubType']
            l2_product['zBestSubType'] = f'new-{name}'
            wave, model = template.create_PCA_model(target, l2_product)

        label = l2_product['zBestSubType']
        return plt.plot(wave, model, color=self.model.getOption('TemplateColor'), lw=self.model.getOption('LineWidth'), alpha=0.7, label = label)

            

