import tkinter as tk
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

#pack functions
pack0=lambda el,s: el.pack(padx=5, pady=5, side=s, fill=tk.BOTH)
pack1=lambda el,s: el.pack(padx=5, pady=5, side=s)
pack2=lambda el,s: el.pack(side = s, fill = tk.BOTH, expand = True)

#temp ui elements
tempLabel= lambda f,t,s: pack1(tk.Label(f, text = t),s)
tempButton= lambda f,t: pack1(tk.Button(f, text = t),tk.TOP)

def UpdateGraph(file):
    PlotFile(file)
    canvas.draw() 
    redCanvas.draw()
    greenCanvas.draw()
    blueCanvas.draw()

def CreateCanvas(fig,rootFrame, place = tk.TOP):
    canv=tkplot.FigureCanvasTkAgg(fig, rootFrame)
    canv.get_tk_widget().config(width = 200, height = 200)
    pack2(canv.get_tk_widget(),place)
    return canv

# The UI elements
root = tk.Tk()
root.minsize(400, 400)
data_frame = tk.Frame(root, bg="red")
pack0(data_frame,tk.TOP)

# FileMenu Dropdown
menubar = tk.Menu(root)
root.config(menu=menubar)

fileMenu = tk.Menu(menubar)
fileMenu.add_command(label="Exit", command=root.quit)
fileMenu.add_command(label="Open Folder", command=lambda: navigator.openFolder(UpdateGraph))
menubar.add_cascade(label="File", menu=fileMenu)

# Header with info about the filetempLabel(f,t,s)
tempLabel(data_frame,"What is the DELTA-MAG of ±2 neighbors on the CCD",tk.LEFT)
tempLabel(data_frame,"Target metadata:\nMAG, MAG_TYPE, target name,\nE(B-V)_gal",tk.RIGHT)

# The graphs
vis_frame = tk.Frame(root, bg="skyblue")
pack2(vis_frame, tk.TOP)
spectrum_frame = tk.Frame(vis_frame, bg = "orange")
pack2(spectrum_frame, tk.LEFT)
canvas = CreateCanvas(bigFig, spectrum_frame)

colors_frame = tk.Frame(spectrum_frame, bg = "skyblue")
pack2(colors_frame, tk.BOTTOM)
redCanvas   = CreateCanvas(redFig,colors_frame, tk.RIGHT)
greenCanvas = CreateCanvas(greenFig,colors_frame, tk.RIGHT)
blueCanvas  = CreateCanvas(blueFig,colors_frame, tk.RIGHT)

tempButton(spectrum_frame,"Redshift slide, template drop-down")

# Sidepanel with buttons
spectrum_buttons = tk.Frame(vis_frame, bg = "yellow")
spectrum_buttons.pack(side = tk.RIGHT, fill = tk.BOTH)
tempButton(spectrum_buttons,"SHOW spectra of STACK")
tempButton(spectrum_buttons,"Show S/N spec")
tempButton(spectrum_buttons,"Button to grab: Image cutout (DSS) 100\"x100\"")

# Navigation buttons in the bottom
opts_frame = tk.Frame(root, bg="limegreen")
pack0(opts_frame,tk.BOTTOM)
navButton = lambda t, d: tk.Button(opts_frame, text=t, command = lambda: NavBtn(navigator, UpdateGraph, msg=t,delta=d))
pack0(navButton("Go Back",-1),tk.LEFT)
pack0(navButton("Yes",1),tk.LEFT)
pack0(navButton("No",1),tk.LEFT)
pack0(navButton("Not sure",1),tk.LEFT)
tempLabel(data_frame,"NO, but why:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?",tk.RIGHT)

navigator.openFolder(UpdateGraph)

root.mainloop()
