from astropy import coordinates as coords
from astropy.io.fits import getheader
from astropy import units as u
from urllib.parse import urlencode
from urllib.request import urlretrieve
from IPython.display import Image

def LoadPicture(directory, files, cursor):
    header = getheader(directory+"/"+files[cursor])
    ra_u = header['RA']*u.deg
    dec_u = header['DEC']*u.deg
    pos = coords.SkyCoord(ra_u, dec_u)
    print(pos)

    im_size = 3 * u.arcmin # get a 25 arcmin square
    im_pixels = 1024
    cutoutbaseurl = 'http://skyservice.pha.jhu.edu/DR12/ImgCutout/getjpeg.aspx'
    query_string = urlencode(dict(ra = ra_u,
                        dec = dec_u,
                        width = im_pixels, height = im_pixels,
                        scale = im_size.to(u.arcsec).value/im_pixels))
    url = cutoutbaseurl + '?' + query_string

    # this downloads the image
    image_name = files[cursor] + '_cutout.jpg'
    urlretrieve(url, image_name)
    Image(image_name) #load the image into the notebook
