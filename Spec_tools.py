import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from spectres import spectres
from astropy.io.fits import getdata
from astropy.io.fits import getheader

class Alfosc_spectrum():
    """
    Dette er en klasse til håndtering af spektra fra det Nordisk Optiske Teleskop.
    Fits-filen forventes at have 4 extensions: 
    - flux (Horne extraction) 
    - flux (sum extraction) 
    - sky-background 
    - 1-sigma flux error    
    Klassen har følgende attributter:
    - Wavelength
    - Flux
    - Skybackground
    - 1 sigma noise
    - Object name
    and these methods:
    - rebin()
    - reset()
    - plot()
    """
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
        self.TCStarget = self.Header['TCSTGT']

        #Generate the wavelength array based on the HEADER
        Wavelength = []
        try: 
            startwavelength = self.Header['CRVAL1']
            dispersion = self.Header['CDELT1']
            for i in range(len(self.Flux)):
                Wavelength.append(self.Header['CRVAL1']+i*self.Header['CDELT1'])
            self.Wavelength = np.array(Wavelength)#convert from list to numpy array
        except KeyError:
            print('Wavelength calibration header keywords are not in the header')

    def Rebin(self,Factor):
        """
        Test tekst der beskriver rebin i klassen NOT-spektrum
        """
        #Rebin the spectrum using spectres
        newdisp = self.Header['CDELT1']*Factor
        newwave = np.arange(min(self.Wavelength), max(self.Wavelength), newdisp)
        fluxbin,noisebin = spectres(newwave,self.Wavelength,self.Flux,self.Noise,verbose=False)
        skybin = spectres(newwave,self.Wavelength,self.Skybackground,verbose=False)
        self.Wavelength = newwave
        self.Flux = fluxbin
        self.Noise = noisebin
        self.Skybackground = skybin
 
    def Reset(self):
        #Read the fits-file
        HDU = fits.open(self.Filename)
        data = HDU[0].data
        self.Flux = data[0,0,:]
        self.Fluxsum = data[1,0,:]
        self.skybackground = data[2,0,:]
        self.Noise = data[3,0,:]
        #Generate the wavelength array based on the HEADER
        Wavelength = []
        try: 
            startwavelength = self.Header['CRVAL1']
            dispersion = self.Header['CDELT1']
            for i in range(len(self.Flux)):
                Wavelength.append(self.Header['CRVAL1']+i*self.Header['CDELT1'])
            self.Wavelength = np.array(Wavelength)#convert from list to numpy array
        except KeyError:
            print('Wavelength calibration header keywords are not in the header')

    def Plot(self):
        plt.figure()
        plt.step(self.Wavelength,self.Flux,label='Flux')
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.Wavelength,self.Noise,label='Noise')
        plt.title(self.Objectname)
        plt.legend()

    def Writeascii(self):
        data_ny = np.column_stack((self.Wavelength,self.Flux,self.Noise))
        header = "Bølgelængde (Å)  flux"
        formats = ("%.2f", "%.0f")
        np.savetxt("self.Objectname"+".dat", data_ny, fmt=formats, header=header, comments="")


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

    def Rebin(self,Factor):
        #Rebin the spectrum using spectres
        olddisp = (max(self.Wavelength)-min(self.Wavelength))/len(self.Wavelength)
        newdisp = olddisp*Factor
        newwave = np.arange(min(self.Wavelength), max(self.Wavelength), newdisp)
        fluxbin,noisebin = spectres(newwave,self.Wavelength,self.Flux,self.Noise,verbose=False)
        skybin = spectres(newwave,self.Wavelength,self.Skybackground,verbose=False)
        self.Wavelength = newwave
        self.Flux = fluxbin
        self.Noise = noisebin
        self.Skybackground = skybin
 
    def Reset(self):
        #Read the fits-file
        data = getdata(self.Filename)
        self.Flux = data['flux']
        self.Wavelength = 10**data['loglam']
        self.Noise = 1./np.sqrt(data['ivar'])
        self.Skybackground = data['Sky']


    def Plot(self):
        plt.figure()
        plt.step(self.Wavelength,self.Flux,label='Flux')
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.step(self.Wavelength,self.Noise,label='Noise')
        plt.title(self.Objectname)
        plt.legend()

    def Writeascii(self):
        data_ny = np.column_stack((self.Wavelength,self.Flux,self.Noise))
        header = "Bølgelængde (Å)  flux"
        formats = ("%.2f", "%.0f")
        np.savetxt("self.Objectname"+".dat", data_ny, fmt=formats, header=header, comments="")

class Fies_spectrum():
    """
    Dette er en klasse til håndtering af reducerede spektra fra det Nordisk Optiske Teleskop.
    Fits-filen forventes at have 1 extension: 
    - flux 
    Klassen har følgende attributter:
    - Wavelength
    - Flux
    - Object name
    and these methods:
    - rebin()
    - reset()
    - plot()
    - writeascii()
    """
    def __init__(self,Filename):
        self.Filename = Filename

        #Read the fits-file
        HDU = fits.open(Filename)
        data = HDU[0].data
        self.Flux = data[:]
        #Read in the Header
        self.Header = HDU[0].header
        try:
            self.Objectname = self.Header['OBJECT']
        except KeyError:
            print('OBJECT keyword not in the header') 
        self.TCStarget = self.Header['TCSTGT']

        #Generate the wavelength array based on the HEADER
        Wavelength = []
        try: 
            startwavelength = self.Header['CRVAL1']
            dispersion = self.Header['CDELT1']
            for i in range(len(self.Flux)):
                Wavelength.append(self.Header['CRVAL1']+i*self.Header['CDELT1'])
            self.Wavelength = np.array(Wavelength)#convert from list to numpy array
        except KeyError:
            print('Wavelength calibration header keywords are not in the header')

    def Rebin(self,Factor):
        """
        Test tekst der beskriver rebin i klassen NOT-spektrum
        """
        #Rebin the spectrum using spectres
        newdisp = self.Header['CDELT1']*Factor
        newwave = np.arange(min(self.Wavelength), max(self.Wavelength), newdisp)
        fluxbin,noisebin = spectres(newwave,self.Wavelength,self.Flux,self.Noise,verbose=False)
        skybin = spectres(newwave,self.Wavelength,self.Skybackground,verbose=False)
        self.Wavelength = newwave
        self.Flux = fluxbin
        self.Noise = noisebin
        self.Skybackground = skybin
 
    def Reset(self):
        #Read the fits-file
        HDU = fits.open(self.Filename)
        data = HDU[0].data
        self.Flux = data[0,0,:]
        self.Fluxsum = data[1,0,:]
        self.skybackground = data[2,0,:]
        self.Noise = data[3,0,:]
        #Generate the wavelength array based on the HEADER
        Wavelength = []
        try: 
            startwavelength = self.Header['CRVAL1']
            dispersion = self.Header['CDELT1']
            for i in range(len(self.Flux)):
                Wavelength.append(self.Header['CRVAL1']+i*self.Header['CDELT1'])
            self.Wavelength = np.array(Wavelength)#convert from list to numpy array
        except KeyError:
            print('Wavelength calibration header keywords are not in the header')

    def Plot(self):
        plt.figure()
        plt.step(self.Wavelength,self.Flux,label='Flux')
        plt.xlabel('Wavelength (Å)')
        plt.ylabel('Flux (erg/s/cm2/Å)')
        plt.title(self.Objectname)
        plt.legend()

    def Writeascii(self):
        data_ny = np.column_stack((self.Wavelength,self.Flux))
        header = "Bølgelængde (Å)  flux"
        formats = ("%.2f", "%.0f")
        np.savetxt("self.Objectname"+".dat", data_ny, fmt=formats, header=header, comments="")
