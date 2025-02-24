import tkinter as tk
import Spec_tools as tool
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot

from tkinter import filedialog as browse
from plotter import PlotFile
from ssPicture import LoadPicture

global directory
files = []
cursor = 0 #cursor for which file the program is currently showing
directory = ""
bigFig = plt.figure('k') #due to matplotlib stupid, you have to give the figure a key, and it cannot be its own key
redFig = plt.figure('r')
greenFig = plt.figure('g')
blueFig = plt.figure('b')

def NavBtn (msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    global cursor
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' with the target name once we can extract that information
        f.write(f"{files[cursor]}, {msg}\n")
    cursor = cursor + delta
    LoadFile(delta)

def OpenFolder():
    #Tests: What if you cancel selecting a folder? What if the folder does not exist? What if it is the first time you select a folder?
    global files
    global cursor
    global directory
    directory = browse.askdirectory()
    files = os.listdir(directory) 
    cursor = 0
    LoadFile()

def LoadFile(delta=1):
    global cursor
    print("Current File: " + files[cursor])

    while True:
        try:
            my_file = tool.SDSS_spectrum(directory+"/"+files[cursor]) #not OS safe I think
            print("Current File: " + files[cursor])
            break
        except OSError:
            del files[cursor]
            if delta < 0:
                cursor = cursor-1
            print("skipping bad file\n")
            continue

    PlotFile(my_file)
    canvas.draw() 
    redCanvas.draw()
    greenCanvas.draw()
    blueCanvas.draw()

def CreateCanvas(fig,rootFrame, place = tk.TOP):
    canv=tkplot.FigureCanvasTkAgg(fig, rootFrame)
    canv.get_tk_widget().config(width = 200, height = 200)
    canv.get_tk_widget().pack(padx = 5, pady = 5,side = place, fill = tk.BOTH, expand = True)
    return canv

# The UI elements
root = tk.Tk()
root.minsize(400, 400)
data_frame = tk.Frame(root, bg="red")
data_frame.pack(padx = 5, pady = 5, side = tk.TOP, fill = tk.BOTH)

# FileMenu Dropdown
menubar = tk.Menu(root)
root.config(menu=menubar)

fileMenu = tk.Menu(menubar)
fileMenu.add_command(label="Exit", command=root.quit)
fileMenu.add_command(label="Open Folder", command=OpenFolder)
menubar.add_cascade(label="File", menu=fileMenu)

# Header with info about the file
tk.Label(data_frame, text = "What is the DELTA-MAG of ±2 neighbors on the CCD").pack(padx = 5, pady = 5, side = tk.LEFT)
tk.Label(data_frame, text = "Target metadata:\nMAG, MAG_TYPE, target name,\nE(B-V)_gal").pack(padx = 5, pady = 5,side = tk.RIGHT)

# The graphs
vis_frame = tk.Frame(root, bg="skyblue")
vis_frame.pack(padx = 5, pady = 5, side = tk.TOP, fill = tk.BOTH, expand = True)
spectrum_frame = tk.Frame(vis_frame, bg = "orange")
spectrum_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
canvas = CreateCanvas(bigFig, spectrum_frame)

colors_frame = tk.Frame(spectrum_frame, bg = "skyblue")
colors_frame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)
redCanvas   = CreateCanvas(redFig,colors_frame, tk.RIGHT)
greenCanvas = CreateCanvas(greenFig,colors_frame, tk.RIGHT)
blueCanvas  = CreateCanvas(blueFig,colors_frame, tk.RIGHT)

redshift_slide = tk.Button(spectrum_frame, text="Redshift slide, template drop-down").pack(padx = 5, pady = 5,side = tk.BOTTOM)

# Sidepanel with buttons
spectrum_buttons = tk.Frame(vis_frame, bg = "yellow")
spectrum_buttons.pack(side = tk.RIGHT, fill = tk.BOTH)
show_stack = tk.Button(spectrum_buttons, text = "SHOW spectra of STACK").pack(padx = 5, pady = 5, side = tk.TOP, fill = tk.BOTH)
show_sn = tk.Button(spectrum_buttons, text = "Show S/N spec").pack(padx = 5, pady = 5, side = tk.TOP, fill = tk.BOTH)
show_skyview = tk.Button(spectrum_buttons, text = "Button to grab: Image cutout (DSS) 100\"x100\"", command = lambda: LoadPicture(directory, files, cursor)).pack(padx=5, pady=5,side=tk.BOTTOM, fill=tk.BOTH)

# Navigation buttons in the bottom
opts_frame = tk.Frame(root, bg="limegreen")
opts_frame.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.BOTH)
tk.Button(opts_frame, text="Go Back", command = lambda: NavBtn(msg="Go Back",delta=-1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="Yes", command = lambda: NavBtn(msg="Yes",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="No", command = lambda: NavBtn(msg="No",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="Not sure", command = lambda: NavBtn(msg="Not sure",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Label(opts_frame, text="NO, but why:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?").pack(padx=5, pady=5,side=tk.RIGHT, fill=tk.BOTH)

OpenFolder()

files = os.listdir(directory) 
cursor = 0

root.mainloop()
