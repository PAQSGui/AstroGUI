from astropy.io import fits
import Spec_tools as tool
import os
import matplotlib.pyplot as plt
from pyhamimports import *
from spectrum import Spectrum

from pathlib import Path

spectraPath="./spectra/spec-1222-52763-0091.fits"


#plot stuff
my_file = tool.SDSS_spectrum(spectraPath)

os.environ["XDG_SESSION_TYPE"] = "xcb"
my_file.Plot()
plt.show()


#Pyhammer stuff
spec = Spectrum()

message, ftype = spec.readFile(spectraPath, 'fits')

spec.calcSN()
