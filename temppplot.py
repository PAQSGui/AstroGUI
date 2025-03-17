import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

from astropy.io.fits import getdata
from astropy.io.fits import getheader

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
    

DrawTemplate('QSO')