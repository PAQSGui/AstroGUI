from astropy.io import fits

hdul = fits.open("data/spec-2237-53828-0531.fits", ignore_missing_simple=True)

# data = hdul[0].data
# header = hdul[0].header
# print(data)
# print(header)
#print(hdul.info())
#print(hdul[0].header['NAME'])

for k in hdul[0].header:
    print(k)


def getTargetData():
    name = hdul[0].header['NAME']

    return name