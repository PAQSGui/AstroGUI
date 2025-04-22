import json
from astropy.utils.misc import JsonCustomEncoder #https://docs.astropy.org/en/stable/api/astropy.utils.misc.JsonCustomEncoder.html
from os import makedirs
from pathlib import Path

from DataObject import DataObject
from numpy import array

from database_common import CreateReplaceDialog

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
                        convertNPRecursive(values)
                                
            except Exception as e:
                self.model = CreateReplaceDialog(self.filepath,lambda file: json.dump({}, file, cls=JsonCustomEncoder),{},e)
        else:
            with open(self.filepath, 'w') as file:
                self.model = {} #dictionary
                json.dump(self.model, file, cls=JsonCustomEncoder)


    def getByName(self, name, default=[]):
        return self.model.get(name,default)

    def addByName(self, name, data):
        self.model[name]=data
        with open(self.filepath, 'w') as file:
            json.dump(self.model, file, cls=JsonCustomEncoder)

    def getFilenames(self):
        list(self.model.keys())

    def addEntry(self, name, fields, data):
        if (len(fields)!=len(data)+1):
            raise Exception("Expected fields to be one longer than data because of name field, but it is "+ len(fields))
        entry={}
        for i in range(len(data)):
            entry[fields[i+1]]=data[i]
        self.model[name]=entry
        with open(self.filepath, 'w') as file:
            json.dump(self.model, file, cls=JsonCustomEncoder)

def convertNPRecursive(values):
    for key in list(values.keys()):
        if type(values[key]) is list:
            try:
                values[key]=array(values[key])
            except ValueError:
                continue
        elif type(values[key]) is dict:
            convertNPRecursive(values[key])