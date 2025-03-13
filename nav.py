from tkinter import filedialog as browse
import os
import Spec_tools as tool
from pathlib import Path

class Navigator:

    cursor: int
    files: list[str]
    directory: str
    current: tool.SDSS_spectrum

    def __init__(self, dir, files, cursor):
        self.directory = dir
        self.files = files
        self.cursor = cursor
    
    def getCurrentFile(self):
        return self.files[self.cursor]
        
    def updateCursor(self, delta):
        self.cursor = self.cursor + delta
    
    def deleteFile(self, delta):
        del self.files[self.cursor]
        if delta < 0:
            self.updateCursor(-1)
        print("skipping bad file\n")

    def openFolder(self, loadfunc):
        #Tests: What if you cancel selecting a folder? What if the folder does not exist? What if it is the first time you select a folder?

        self.directory = browse.askdirectory()
        self.files = os.listdir(self.directory) 
        self.cursor = 0
        self.loadFile(loadfunc)

    
    def loadFile(self, updatefunc, delta=1):
        print("Current File: " + self.getCurrentFile())

        while True:
            try:
                self.current = tool.SDSS_spectrum(Path(self.directory) / Path(self.getCurrentFile()))
                print("Current File: " + self.getCurrentFile())
                break
            except OSError:
                self.deleteFile(delta)
                continue
        updatefunc(self.current)



def NavBtn (navigator, loadfunc, msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' waith the target name once we can extract that information
        f.write(f"{navigator.getCurrentFile()}, {msg}\n")
    navigator.updateCursor(delta)
    navigator.loadFile(loadfunc,delta)