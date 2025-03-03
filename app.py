import tkinter as tk
import Spec_tools as tool
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot

from tkinter import filedialog as browse
from plotter import PlotFile
from nav import NavBtn, Navigator
from ssPicture import LoadPicture

navigator = Navigator("",[],0)
bigFig = plt.figure('k') #due to matplotlib stupid, you have to give the figure a key, and it cannot be its own key
redFig = plt.figure('r')
greenFig = plt.figure('g')
blueFig = plt.figure('b')

def OpenFolder():
    #Tests: What if you cancel selecting a folder? What if the folder does not exist? What if it is the first time you select a folder?
    global navigator
    navigator.directory = browse.askdirectory()
    navigator.files = os.listdir(navigator.directory) 
    navigator.cursor = 0
    LoadFile()

def LoadFile(delta=1):
    global navigator
    print("Current File: " + navigator.files[navigator.cursor])

    while True:
        try:
            my_file = tool.SDSS_spectrum(navigator.directory+"/"+navigator.files[navigator.cursor]) #not OS safe I think
            print("Current File: " + navigator.files[navigator.cursor])
            break
        except OSError:
            del navigator.files[navigator.cursor]
            if delta < 0:
                navigator.cursor = navigator.cursor-1
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
tk.Button(opts_frame, text="Go Back", command = lambda: NavBtn(navigator, LoadFile, msg="Go Back",delta=-1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="Yes", command = lambda: NavBtn(navigator, LoadFile, msg="Yes",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="No", command = lambda: NavBtn(navigator, LoadFile, msg="No",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Button(opts_frame, text="Not sure", command = lambda: NavBtn(navigator, LoadFile, msg="Not sure",delta=1)).pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH)
tk.Label(opts_frame, text="NO, but why:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?").pack(padx=5, pady=5,side=tk.RIGHT, fill=tk.BOTH)

OpenFolder()

navigator.files = os.listdir(navigator.directory) 
navigator.cursor = 0

root.mainloop()
