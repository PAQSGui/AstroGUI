import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

from astropy.io.fits import getdata
from astropy.io.fits import getheader

from astropy import units as u

from xpca import config
from xpca.template import PCATemplate

def DrawTemplate(template):
    fileName = GetFileName(template)

    data = getdata(fileName)
    print(data)

    header = getheader(fileName)
    print(header)
    
    # adjust for redshift?


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
    

def create_PCA_model(spectrum, l2_product):
    """
    stolen from xpca
    """
    wavelength = spectrum.Wavelength
    name = l2_product['zBestSubType']
    z = l2_product['zBest']
    coeffs = l2_product['zBestPars']
    if '--' in name:
        name = name.replace('--', '-')
    fname = config.TEMPLATE_PATH / f'template-{name.lower()}.fits'
    coeffs = coeffs[coeffs.nonzero()[0]]
    try:
        best_fit = PCATemplate.read(fname)
    except FileNotFoundError:
        try:
            fname = config.TEMPLATE_PATH / f'template-new-{name.lower()}.fits'
            best_fit = PCATemplate.read(fname)
        except FileNotFoundError:
            fname = config.TEMPLATE_PATH / f'template-{l2_product['zBestType'].lower()}.fits'
            best_fit = PCATemplate.read(fname)
    #best_fit = best_fit.rebin(wavelength, z=z, N=config.MAX_COEFFS)

    # Prepare Chebyshev polynomials:
    x = np.linspace(-1, 1, len(wavelength))
    cheb = []
    for n_cheb in range(0, config.CHEB_ORDER):
        C_i = np.polynomial.Chebyshev([0] * n_cheb + [1])(x)
        cheb.append(C_i)
    cheb = np.array(cheb)
    #best_fit.flux = np.vstack([best_fit.flux, cheb]) #ValueError: all the input array dimensions except for the concatenation axis must match exactly, but along dimension 1, the array at index 0 has size 13637 and the array at index 1 has size 4605
    wave, model = best_fit(coeffs)

    chi2 = l2_product['zBestChi2'] / l2_product['zBestNfree']
    title_str += f"\n z = {z:.5f}  Class: {name}  $\\chi^2 = {chi2:.2f}$"
    plt.plot(wave, model, color='r', lw=1.0, alpha=0.7)

#DrawTemplate('QSO')