import matplotlib.pyplot as plt
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template
from Model import Model

"""
Templater uses xpca to draw a template over the plot
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
        if state.fitting is not None:
            spec = state.file
            l2_product = state.fitting
            
            l2_product['zBest'] = self.model.getRedShift()
            target=Target(uid=0, name='temp', spectrum=Spectrum(spec.Wavelength*Unit('AA'), spec.Flux*Unit('erg/(s cm2 AA)'), spec.Noise*Unit('erg/(s cm2 AA)')))
            
            l2_product['zBestSubType'] = state.category
            try:
                wave, model = template.create_PCA_model(target, l2_product)
            except FileNotFoundError:
                l2_product['zBestSubType'] = f'new-{state.category}'
                wave, model = template.create_PCA_model(target, l2_product)
                l2_product['zBestSubType'] = state.category

            
            return plt.plot(wave, model, color=self.model.getOption('TemplateColor'), lw=self.model.getOption('LineWidth'), alpha=0.7, label=state.category)
        else:
            return [None]