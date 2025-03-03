class Navigator:

    cursor: int
    files: list[str]
    directory: str

    def __init__(self, dir, files, cursor):
        self.directory = dir
        self.files = files
        self.cursor = cursor


def NavBtn (navigator, loadfunc, msg, delta):
    #Tests: Can you go out of bounds? Is the selected file a FITS? Is it the correct format of FITS?
    print("Button clicked: " + msg)
    with open("data.csv", "a") as f:
        # Replace 'files[cursor]' waith the target name once we can extract that information
        f.write(f"{navigator.files[navigator.cursor]}, {msg}\n")
    navigator.cursor = navigator.cursor + delta
    loadfunc(delta)