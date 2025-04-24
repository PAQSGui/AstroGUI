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
                    self.datamodel = json.load(file)
                    for file in list(self.datamodel.keys()):
                        values = self.datamodel[file]
                        convertNPRecursive(values)
                                
            except Exception as e:
                self.datamodel = CreateReplaceDialog(self.filepath,lambda file: json.dump({}, file, cls=JsonCustomEncoder),{},e)
        else:
            self.datamodel = {} #dictionary
            with open(self.filepath, 'w') as file:
                json.dump(self.datamodel, file, cls=JsonCustomEncoder)


    def getByName(self, name, default=None):
        return self.datamodel.get(name,default)

    def addByName(self, name, data):
        self.datamodel[name]=data
        with open(self.filepath, 'w') as file:
            json.dump(self.datamodel, file, cls=JsonCustomEncoder)

    def getFilenames(self):
        list(self.datamodel.keys())

    def addEntry(self, dataObj, fields, data):
        if (len(fields)!=len(data)+1):
            raise Exception("Expected fields to be one longer than data because of name field, but it is "+ len(fields))
        entry={}
        for i in range(len(data)):
            entry[fields[i+1]]=data[i]
        self.datamodel[dataObj.name]=entry
        with open(self.filepath, 'w') as file:
            json.dump(self.datamodel, file, cls=JsonCustomEncoder)

    def savedataModelToFile(self,file):
        json.dump(self.datamodel, file, cls=JsonCustomEncoder)

def getdataModelFromDatabase(filepath):
    with open(filepath, 'r') as file:
                    data = json.load(file)
                    for file in list(data.keys()):
                        data[file] = convertNPRecursive(data[file])
                    return data

def convertNPRecursive(values):
    for key in list(values.keys()):
        if type(values[key]) is list:
            try:
                values[key]=array(values[key])
            except ValueError:
                continue
        elif type(values[key]) is dict:
            convertNPRecursive(values[key])
    return values