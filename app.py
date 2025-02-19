import tkinter as tk
import Spec_tools as tool
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot
from tkinter import filedialog as browse

files=[]
cursor=0#cursor for which file the program is currently showing
bigFig=plt.figure('k')#due to matplotlib stupid, you have to give the figure a key, and it cannot be its own key
redFig=plt.figure('r')
bluFig=plt.figure('b')
grnFig=plt.figure('g')
def NavBtn (msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    global cursor
    cursor=cursor+delta
    print("Current File: " + files[cursor])

def CreatePlot(file,fig,limitPlot=False, range=[6250, 7400]):
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

def OpenFolder():
    #Tests: What if you cancel selecting a folder? What if the folder does not exist? What if it is the first time you select a folder?
    global files
    global cursor
    directory=browse.askdirectory()
    files=os.listdir(directory) 
    cursor=0
    print("Current File: " + files[cursor])
    while True:
        try:
            my_file = tool.SDSS_spectrum(directory+"/"+files[cursor]) #not OS safe
            print("Current File: " + files[cursor])
            break
        except OSError:
            del files[cursor]
            print("skipping bad file\n")
            continue
    #generate 4 steps in visible spectrum
    visrange=np.linspace(3800,7500,4)
    CreatePlot(my_file,'k')
    CreatePlot(my_file,'b',limitPlot=True, range=[visrange[0], visrange[1]])
    CreatePlot(my_file,'g',limitPlot=True, range=[visrange[1], visrange[2]])
    CreatePlot(my_file,'r',limitPlot=True, range=[visrange[2], visrange[3]])
    canvas.update_idletasks() #this doesn't work, only resizing the window refreshes right now
    bluCanvas.update_idletasks()
    grnCanvas.update_idletasks()
    redCanvas.update_idletasks()

def CreateCanvas(fig,rootFrame,place=tk.TOP):
    canv=tkplot.FigureCanvasTkAgg(fig,rootFrame).get_tk_widget()
    canv.config(width=200,height=200)
    canv.pack(padx=5, pady=5,side=place, fill=tk.BOTH, expand=True)
    return canv


root = tk.Tk()

root.minsize(400, 400)
# Create two labels
data_frame = tk.Frame(root, bg="red")
data_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.BOTH, expand=True)

tk.Label(data_frame, text="What is the DELTA-MAG of ±2 neighbors on the CCD").pack(padx=5, pady=5,side=tk.LEFT)

# display info from the header in this button
tk.Label(data_frame, text="Target metadata:\nMAG, MAG_TYPE, target name,\nE(B-V)_gal").pack(padx=5, pady=5,side=tk.RIGHT)

vis_frame = tk.Frame(root, bg="skyblue")
vis_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.BOTH, expand=True)
spectrum_frame = tk.Frame(vis_frame, bg="orange")
spectrum_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas=CreateCanvas(bigFig,spectrum_frame)
#spectrum=tk.Label(spectrum_frame, text="L1J spectrum\nL2XP: best-fit template + Z_BEST (plus lines)\nL2CP: CLASS, PROB, CLASS2, PROB2, ...\nOverplot sky spectrum\nOverplot telluric abs.")
#spectrum.pack(padx=5, pady=5,side=tk.TOP)

colors_frame = tk.Frame(spectrum_frame, bg="skyblue")
colors_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
redCanvas=CreateCanvas(redFig,colors_frame,tk.RIGHT)
grnCanvas=CreateCanvas(grnFig,colors_frame,tk.RIGHT)
bluCanvas=CreateCanvas(bluFig,colors_frame,tk.RIGHT)

redshift_slide = tk.Button(spectrum_frame, text="Redshift slide, template drop-down").pack(padx=5, pady=5,side=tk.BOTTOM)

spectrum_buttons = tk.Frame(vis_frame, bg="yellow")
spectrum_buttons.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
show_stack = tk.Button(spectrum_buttons, text="SHOW spectra of STACK").pack(padx=5, pady=5,side=tk.TOP, fill=tk.BOTH, expand=True)
show_sn = tk.Button(spectrum_buttons, text="Show S/N spec").pack(padx=5, pady=5,side=tk.TOP, fill=tk.BOTH, expand=True)
show_skyview = tk.Button(spectrum_buttons, text="Button to grab: Image cutout (DSS) 100\"x100\"").pack(padx=5, pady=5,side=tk.BOTTOM, fill=tk.BOTH, expand=True)


opts_frame = tk.Frame(root, bg="limegreen")
opts_frame.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Go Back", command = lambda: NavBtn(msg="Go Back",delta=-1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Yes", command = lambda: NavBtn(msg="Yes",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="No", command = lambda: NavBtn(msg="No",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Not sure", command = lambda: NavBtn(msg="Not sure",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(opts_frame, text="NO, but why:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?").pack(padx=5, pady=5,side=tk.RIGHT, fill=tk.BOTH, expand=True)

#Menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

fileMenu = tk.Menu(menubar)
fileMenu.add_command(label="Exit", command=root.quit)
fileMenu.add_command(label="Open Folder", command=OpenFolder)
menubar.add_cascade(label="File", menu=fileMenu)

OpenFolder()

root.mainloop()