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
    def findRedshiftForTemplate(self, l2_product):
        #for i in range(len(l2_product['zAlt'])):
        #        result=search(f'(NEW-)?(.+)', self.model.getCategory().upper())
        #        if l2_product['zAltSubType'][i]==result.group(2):
        #            return l2_product['zAlt'][i]
        return None

    def plotTemplate(self):

        state = self.model.getState()
        spec = state.file
        l2_product = state.fitting
        #if l2_product['zBestSubType'].upper() != self.model.getCategory().upper():
        #    l2_product['zBestSubType'] = self.model.getCategory()
        #    newRedshift=self.findRedshiftForTemplate(l2_product)
        #    if newRedshift is not None:
        #        self.model.changeRedShift(newRedshift)
        #        l2_product['zBest'] = newRedshift
        #    try:
        #        l2_product['zBestPars'] = l2_product['zAltPars'][self.model.getCategory().upper()]
        #    except Exception: #replace with a contains check
        #        result=search(f'NEW-(.+)', self.model.getCategory().upper())
        #        l2_product['zBestSubType'] = result.group(1)
        #        l2_product['zBestPars'] = l2_product['zAltPars'][result.group(1)]
        
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

            

