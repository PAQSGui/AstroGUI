from astropy.io import fits

filename = fits.open("spectra/._spec-1222-52763-0091.fits", ignore_missing_simple=True)

with fits.open(filename) as hdul:
    hdul.info()