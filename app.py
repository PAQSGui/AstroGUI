import tkinter as tk

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
spectrum=tk.Label(spectrum_frame, text="L1J spectrum\nL2XP: best-fit template + Z_BEST (plus lines)\nL2CP: CLASS, PROB, CLASS2, PROB2, ...\nOverplot sky spectrum\nOverplot telluric abs.")
spectrum.pack(padx=5, pady=5,side=tk.TOP)
redshift_slide = tk.Button(spectrum_frame, text="Redshift slide, template drop-down").pack(padx=5, pady=5,side=tk.TOP)

colors_frame = tk.Frame(spectrum_frame, bg="skyblue")
colors_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
red_frame = tk.Frame(colors_frame, bg="red")
red_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(red_frame, text="L1R").place(relx=0.5, rely=0.5, anchor='center')
green_frame = tk.Frame(colors_frame, bg="green")
green_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(green_frame, text="L1G").place(relx=0.5, rely=0.5, anchor='center')
blue_frame = tk.Frame(colors_frame, bg="blue")
blue_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
tk.Label(blue_frame, text="L1B").place(relx=0.5, rely=0.5, anchor='center')

spectrum_buttons = tk.Frame(vis_frame, bg="yellow")
spectrum_buttons.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
show_stack = tk.Button(spectrum_buttons, text="SHOW spectra of STACK").pack(padx=5, pady=5,side=tk.TOP, fill=tk.BOTH, expand=True)
show_sn = tk.Button(spectrum_buttons, text="Show S/N spec").pack(padx=5, pady=5,side=tk.TOP, fill=tk.BOTH, expand=True)
show_skyview = tk.Button(spectrum_buttons, text="Button to grab: Image cutout (DSS) 100\"x100\"").pack(padx=5, pady=5,side=tk.BOTTOM, fill=tk.BOTH, expand=True)


opts_frame = tk.Frame(root, bg="limegreen")
opts_frame.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Go BACK").pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Yes").pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="No").pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(opts_frame, text="Not sure").pack(padx=5, pady=5,side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(opts_frame, text="NO, but why:\nWrong template; wrong redshift (4XP);\nwrong class (4CP);\nBad data (L1); Maybe sat.?").pack(padx=5, pady=5,side=tk.RIGHT, fill=tk.BOTH, expand=True)

#Menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

fileMenu = tk.Menu(menubar)
fileMenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=fileMenu)

root.mainloop()
