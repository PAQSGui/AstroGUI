import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

from astropy.io.fits import getdata
from astropy.io.fits import getheader

from astropy import units as u

from xpca import config
from xpca.template import PCATemplate

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template

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
    

def plotTemplate(spec, l2_product):
    target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*u.Unit("AA"),spec.Flux*u.Unit("erg/(s cm2 AA)"),spec.Noise*u.Unit("erg/(s cm2 AA)")))
    try:
        wave, model = template.create_PCA_model(target,l2_product)
    except FileNotFoundError:
        print("not found, trying by appending new, this is a bad solution tho")
        name = l2_product['zBestSubType']
        l2_product['zBestSubType']=f'new-{name}'
        wave, model = template.create_PCA_model(target,l2_product)

    chi2 = l2_product['zBestChi2'] / l2_product['zBestNfree']
    #title_str += f"\n z = {z:.5f}  Class: {name}  $\\chi^2 = {chi2:.2f}$"
    plt.plot(wave, model, color='r', lw=1.0, alpha=0.7)


#DrawTemplate('QSO')