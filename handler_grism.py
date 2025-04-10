import matplotlib as plt
from Spec_tools import Osiris_spectrum, SDSS_spectrum
from re import search


def UpdateGrism(model, plotter, spectra=None):
    plt.figure('k')
    if spectra==None:
        spectra=model.getState().file
    plt.clf() #clear figure
    colorcodes = ['k','r','g','b']
    for x in [0,1,2,3]:
        if spectra[x]!=None:
            plotter.DrawPlot(spectra[x],colorcodes[x])

    plt.legend()
    plotter.figure.draw()

def grismArray(nav, filename):
    grisms = []
    for x in ['','R','G','B']:
        try:
            nextGrism = Osiris_spectrum(nav.directory.absoluteFilePath(filename+x+".fits"))
            grisms.append(nextGrism)
        except FileNotFoundError:
            grisms.append(None)
    nav.plotter.UpdateGrism(grisms)

def loadFile(nav, delta=1):
    print("Current File: " + nav.getCurrentFile())

    while True:
        try:
            nav.current = SDSS_spectrum(nav.directory.absoluteFilePath(nav.getCurrentFile()))
            print("Current File: " + nav.getCurrentFile())
            nav.UpdateGraph(nav.current)
            break
        except OSError as e:
            print("nav.py def loadFile OSError")
            print(e)
            nav.deleteFile(delta)
            continue
        except IndexError as e:
            print("nav.py def loadFile IndexError")
            print(e) #Osiris
            #check if there are other files with similar names
            result = search(f'(.+)([RGB]).fits', nav.getCurrentFile())
            if result != None:
                #Create a list of the files
                nav.grismArray(result.group(1))
            else:
                result = search(f'(.+).fits', nav.getCurrentFile())
                nav.grismArray(result.group(1))
            break
    nav.targetData.updateTargetData(nav.getCurrentFilePath()) # Updates target data labels