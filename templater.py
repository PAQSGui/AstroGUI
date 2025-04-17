import matplotlib.pyplot as plt
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template
from Model import Model


class Templater:
    model: Model

    def __init__(self, model):
        self.model = model

    def plotTemplate(self):

        state = self.model.getState()
        spec = state.file
        l2_product = state.fitting
        l2_product['zBest'] = self.model.getRedShift()
        l2_product['zBestSubType'] = self.model.getCategory()

        if type(spec)==list:
            #This should add them together, or make sure to receive a single plot
            spec=spec[0]
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        
        try:
            print(l2_product)
            wave, model = template.create_PCA_model(target,l2_product)
        except FileNotFoundError as e:
            name = l2_product['zBestSubType']
            l2_product['zBestSubType']=f'new-{name}'
            wave, model = template.create_PCA_model(target,l2_product)
        plt.plot(wave, model, color='r', lw=self.model.lineThickness, alpha=0.7, label = l2_product['zBestSubType'])

            

