import json
from astropy.utils.misc import JsonCustomEncoder #https://docs.astropy.org/en/stable/api/astropy.utils.misc.JsonCustomEncoder.html
from os import makedirs
from pathlib import Path
from PySide6.QtWidgets import (
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel
    )

import Spec_tools as tool
from DataObject import DataObject
from numpy import array
class Database():
    filepath : Path
    directory : Path

    def __init__(self, filename, fieldNames, directory=Path('/data/')):
        self.directory=directory
        self.filepath = directory / Path(filename).with_suffix('.json')
        #must turn values into numpy for it to work right
        if self.filepath.is_file():
            try:
                with open(self.filepath, 'r') as file:
                    self.model = json.load(file)
                    for file in list(self.model.keys()):
                        values = self.model[file]
                        for key in list(values.keys()):
                            if type(values[key]) is list:
                                try:
                                    values[key]=array(values[key])
                                except ValueError:
                                    continue
            except Exception as e: #this is a bit dangerous, maybe it should be a limited set of exceptions if that works
                #makedirs(directory, exist_ok=True) Admin privileges are required to run this regardless
                print(type(e))
                replaceDialog=QDialog()
                replaceDialog.setWindowTitle("Can't open database!")

                QBtn = (
                    QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                )

                buttonBox = QDialogButtonBox(QBtn)
                buttonBox.accepted.connect(replaceDialog.accept)
                buttonBox.rejected.connect(replaceDialog.reject)

                layout = QVBoxLayout()
                layout.addWidget(QLabel("A previous session was found in the folder, but cannot be opened. Would you like to overwrite it?"))
                layout.addWidget(buttonBox)
                replaceDialog.setLayout(layout)
                    
                if replaceDialog.exec():
                    with open(self.filepath, 'w') as file:
                        self.model = {} #dictionary
                        json.dump(self.model, file, cls=JsonCustomEncoder)
                else:
                    raise e
        else:
            with open(self.filepath, 'w') as file:
                self.model = {} #dictionary
                json.dump(self.model, file, cls=JsonCustomEncoder)


    def getByName(self, name, default=[]):
        return self.model.get(name,default)

    def addByName(self, name, data):
        self.model[name]=data
        #print(name)
        #print(data)
        with open(self.filepath, 'w') as file:
            json.dump(self.model, file, cls=JsonCustomEncoder)

    def getModel(self):
        objs=[]
        for item in list(self.model.items()):
            print(self.filepath)
            spectra = tool.SDSS_spectrum((self.directory / Path(item[0]))) 
            dobject = DataObject(item[0], spectra, item[1])
            objs.append(dobject)
        return objs


    def addEntry(self, name, fields, data):
        if (len(fields)!=len(data)+1):
            raise Exception("Expected fields to be one longer than data because of name field, but it is "+ len(fields))
        entry={}
        for i in range(len(data)):
            entry[fields[i+1]]=data[i]
        self.model[name]=entry
        #print(name)
        #print(data)
        with open(self.filepath, 'w') as file:
            json.dump(self.model, file, cls=JsonCustomEncoder)