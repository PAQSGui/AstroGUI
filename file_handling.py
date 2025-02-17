from astropy.io import fits

hdul = fits.open("data/spec-2237-53828-0531.fits", ignore_missing_simple=True)

for k in hdul[0].header:
    print(k)


def getTargetData():
    name = hdul[0].header['NAME']
    
    # WHY IS THERE NO EBV CARD?
    #ebv = hdul[0].header['EBV']

    # WHERE IS THE MAGNITUDE? :(
    #mag = hdul[0].header['*MAG*']


    return name