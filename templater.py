import matplotlib.pyplot as plt
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template


class Templater:

    def __init__(self):
        pass

    def plotTemplate(self, spec, l2_product):

        if type(spec)==list:
            #This should add them together, or make sure to receive a single plot
            spec=spec[0]
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        
        try:
            wave, model = template.create_PCA_model(target,l2_product)
        except FileNotFoundError as e:
            print("templater.py def plotTemplate FileNotFoundError")  
            print(e)
            name = l2_product['zBestSubType']
            print(name)
            l2_product['zBestSubType']=f'new-{name}'
            wave, model = template.create_PCA_model(target,l2_product)
        plt.plot(wave, model, color='r', lw=1.0, alpha=0.7, label = l2_product['zBestSubType'])

            

