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

    def plotTemplate(self):

        state = self.model.getState()
        spec = state.file
        l2_product = state.fitting
        if l2_product['zBestSubType'].upper() != self.model.getCategory().upper():
            l2_product['zBestSubType'] = self.model.getCategory()
            for i in range(len(l2_product['zAlt'])):
                result=search(f'(NEW-)?(.+)', self.model.getCategory().upper())
                if l2_product['zAltSubType'][i]==result.group(2):
                    self.model.changeRedShift(l2_product['zAlt'][i])
                    l2_product['zBest'] = l2_product['zAlt'][i]
                    break
            try:
                l2_product['zBestPars'] = l2_product['zAltPars'][self.model.getCategory().upper()]
            except KeyError:
                result=search(f'NEW-(.+)', self.model.getCategory().upper())
                l2_product['zBestSubType'] = result.group(1)
                l2_product['zBestPars'] = l2_product['zAltPars'][result.group(1)]
        
        l2_product['zBest'] = self.model.getRedShift()
        #l2_product['zBestSubType'] = self.model.getCategory()
        #grism handling
        #if type(spec)==list:
        #    #This should add them together, or make sure to receive a single plot
        #    spec=spec[0]
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        
        try:
            wave, model = template.create_PCA_model(target, l2_product)
        except FileNotFoundError as e:
            name = l2_product['zBestSubType']
            l2_product['zBestSubType'] = f'new-{name}'
            wave, model = template.create_PCA_model(target, l2_product)

        label = l2_product['zBestSubType']
        return plt.plot(wave, model, color='r', lw=self.model.getOption('LineWidth'), alpha=0.7, label = label)

            

