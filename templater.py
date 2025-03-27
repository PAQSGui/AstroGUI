import matplotlib.pyplot as plt
from Spec_tools import Fies_spectrum
import numpy as np

from astropy.io.fits import getdata
from astropy.io.fits import getheader
from astropy.io import fits
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template

def DrawTemplate(template, key):

    fileName = GetFileName(template)

    HDU = fits.open(fileName)
    data = HDU[0].data
    Flux = data[:].flatten()
    Header = HDU[0].header

    Wavelength = []
    startwavelength = Header['CRVAL1']
    dispersion = 10**Header['CDELT1']

    totalDispersion = dispersion
    Wavelength.append(startwavelength)

    for _ in range(1, len(Flux)):
        totalDispersion = totalDispersion + dispersion 
        Wavelength.append(startwavelength + totalDispersion)

    Wavelength = np.array(Wavelength) #convert from list to numpy array
    plt.figure(key)
    plt.step(Wavelength, Flux, label = 'Template')
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.title('test')
    #plt.show()

def plotTemplate(spec, l2_product):
    target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
    try:
        wave, model = template.create_PCA_model(target,l2_product)
    except FileNotFoundError:
        print("not found, trying by appending new, this is a bad solution tho")
        name = l2_product['zBestSubType']
        l2_product['zBestSubType']=f'new-{name}'
        wave, model = template.create_PCA_model(target,l2_product)

    plt.plot(wave, model, color='r', lw=1.0, alpha=0.7, label = 'Template')

def GetFileName(template):
    if template == 'GALAXY':
        return "templates/template-galaxy-pass.fits"
    elif template == 'GALAXY-PASS':
        return "templates/template-galaxy.fits"
    elif template == 'QSO-LOWZ':
        return  "templates/template-new-qso-lowz.fits"
    elif template == 'QSO-MIDZ':
        return "templates/template-new-qso-midz.fits"
    elif template == 'QSO':
        return "templates/template-qso.fits"
    else:
        return "templates/template-qso.fits"

    