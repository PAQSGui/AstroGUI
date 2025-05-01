import numpy as np
from astropy.io.fits import getdata
from astropy.io.fits import getheader

"""
This file is a modified version of the file Spec_tools.py written by Fynbo
It Loads a fit-file based on the specific format:
4 extensions: flux (Horne extraction), flux (sum extraction), sky-background, 1-sigma flux error  
The file loaded should be plotable by Plotter.py 
"""
class SDSS_spectrum():
    def __init__(self, Filename):
        self.Filename = Filename

        data = getdata(Filename)
        header = getheader(Filename)

        self.Flux = data['flux']
        self.Wavelength = 10**data['loglam']
        self.Noise = 1./np.sqrt(data['ivar'])
        self.Skybackground = data['Sky']
        self.Objectname = 'SDSS'+header['Name']