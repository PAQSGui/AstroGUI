#https://www.pythonguis.com/tutorials/pyside6-dialogs/ 
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel
    )

def CreateReplaceDialog(filepath,func,default,exc):
    replaceDialog=QDialog()
    replaceDialog.setWindowTitle(str(type(exc)))

    QBtn = (
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    )

    buttonBox = QDialogButtonBox(QBtn)
    buttonBox.accepted.connect(replaceDialog.accept)
    buttonBox.rejected.connect(replaceDialog.reject)

    layout = QVBoxLayout()
    layout.addWidget(QLabel("An exception occurred. It is possible a previous session was found in the folder, but cannot be opened. Would you like to overwrite it?"))
    layout.addWidget(buttonBox)
    replaceDialog.setLayout(layout)
        
    if replaceDialog.exec():
        with open(filepath, 'w') as file:
            #dictionary
            func(file)
            return default
    else:
        raise exc

def getdataModelFromDatabase(filepath, database):
    with open(filepath, 'r') as file:
                    data = database.load(file)
                    return data
