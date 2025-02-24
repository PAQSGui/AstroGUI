
import matplotlib.pyplot as plt

def PlotFile(file, fig, limitPlot=False, range=[6250, 7400]):
    plt.figure(fig)
    plt.clf() #clear figure
    plt.step(file.Wavelength,file.Flux,color=fig) #figure key is used for color
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux (erg/s/cm2/Å)')
    plt.step(file.Wavelength,file.Noise,label='Noise',color='0.5')
    plt.legend()
    if limitPlot:
        plt.xlim(range)
    else: 
        plt.title(file.Objectname)    

