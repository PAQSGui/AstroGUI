import matplotlib.pyplot as plt
from Spec_tools import Fies_spectrum
import numpy as np

from astropy.io.fits import getdata
from astropy.io.fits import getheader
from astropy.io import fits

def DrawTemplate(template):

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

    plt.figure()
    plt.step(Wavelength, Flux, label = 'Flux')
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.title('test')
    plt.show()


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
        return "templates/template-star-A.fits"
    