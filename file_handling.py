from astropy.io import fits

filename = fits.open("spectra/spec-1222-52763-0091.fits", ignore_missing_simple=True)

with filename as hdul:
    print(hdul[2].data['PETROMAG'])