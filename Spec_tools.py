import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from spectres import spectres
from astropy.io.fits import getdata
from astropy.io.fits import getheader

class SDSS_spectrum():
    def __init__(self,Filename):
        self.Filename = Filename

        #Read the fits-file
        data = getdata(Filename)
        header = getheader(Filename)

        self.Flux = data['flux']
        self.Wavelength = 10**data['loglam']
        self.Noise = 1./np.sqrt(data['ivar'])
        self.Skybackground = data['Sky']
        self.Objectname = 'SDSS'+header['Name']

class Osiris_spectrum():
    #The fits file is expected to have 4 extensions: flux (Horne extraction), flux (sum extraction), sky-background, 1-sigma flux error    
    def __init__(self,Filename):
        self.Filename = Filename

        #Read the fits-file
        HDU = fits.open(Filename)
        data = HDU[0].data

        self.Flux = data[0,0,:]
        self.Fluxsum = data[1,0,:]
        self.Skybackground = data[2,0,:]
        self.Noise = data[3,0,:]
        
        #Read in the Header
        self.Header = HDU[0].header
        try:
            self.Objectname = self.Header['OBJECT']
        except KeyError:
            print('OBJECT keyword not in the header') 
        #self.TCStarget = self.Header['TCSTGT']

        #Generate the wavelength array based on the HEADER
        Wavelength = []
        try: 
            startwavelength = self.Header['CRVAL1']
            dispersion = self.Header['CD1_1']
            crpix = self.Header['CRPIX1']
            self.Wavelength = (np.arange(self.Header['NAXIS1']) - (crpix-1)) * dispersion + startwavelength
        except KeyError:
            print('Wavelength calibration header keywords are not in the header')