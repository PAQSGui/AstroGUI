from astropy.io import fits
import Spec_tools as tool
import os
import matplotlib.pyplot as plt

with fits.open("spec-1222-52763-0092.fits") as hdul:
    hdul.info()

my_file = tool.SDSS_spectrum("spec-1222-52763-0091.fits")

os.environ["XDG_SESSION_TYPE"] = "xcb"
my_file.Plot()
plt.show()



