from astropy.io.fits import getheader
from matplotlib import pyplot as plt
from sdss import Region
import tkinter as tk
import matplotlib.backends.backend_tkagg as tkplot

def Show(region, rootFrame, band='all', figsize=None):
    #Shamelessly copied from Behrouz' own implementation
    if region.data is None:
        region.download_data()
    if isinstance(figsize, tuple) and len(figsize)==2:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()
    if band=='i':
        ax.imshow(region.data[:,:,0], cmap='gray')
    elif band=='r':
        ax.imshow(region.data[:,:,1], cmap='gray')
    elif band=='g':
        ax.imshow(region.data[:,:,2], cmap='gray')
    else:
        ax.imshow(region.data)
    plt.axis('off') # new
    canv=tkplot.FigureCanvasTkAgg(fig, rootFrame)
    canv.get_tk_widget().config(width = 200, height = 200)
    canv.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

def LoadPicture(tkroot, directory, files, cursor):
    header = getheader(directory+"/"+files[cursor])
    ra = header['RA']
    dec = header['DEC']
    #https://github.com/behrouzz/sdss
    reg = Region(ra, dec, fov=0.033)
    print(reg.nearest_objects())
    
    window = tk.Toplevel(tkroot)
    window.title('SDSS Image')
    Show(reg,window) #does not work for some reason
