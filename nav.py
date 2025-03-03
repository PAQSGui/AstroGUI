class Navigator:

    cursor: int
    files: list[str]
    directory: str

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


def NavBtn (navigator, loadfunc, msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' waith the target name once we can extract that information
        f.write(f"{navigator.getCurrentFile()}, {msg}\n")
    navigator.updateCursor(delta)
    loadfunc(delta)