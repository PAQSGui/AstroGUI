import csv
import Spec_tools as tool
from DataObject import DataObject
from PySide6.QtCore import (
    QDir,
)
from pathlib import Path

from database_common import CreateReplaceDialog

class Database():
    filepath : Path
    fieldNames = ""
    path : str

    #def __init__(self, filepath, fieldNames, path = ''):
    #    self.filepath = "%s.csv" % filepath
    #    self.fieldNames = fieldNames
    #    self.path = path 

    #    with open(self.filepath, 'a', newline='') as file:
    #        writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
    #        writer.writeheader()  

    def __init__(self, filename, fieldNames, directory=Path('/data/')):
        def writeEmpty(file):
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writeheader() 



        self.directory=directory
        self.filepath = directory / Path(filename).with_suffix('.csv')
        if self.filepath.is_file():
            try:
                with open(self.filepath, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    self.dataFrame = {}
                    for row in reader:
                        if row['name'] != self.fieldNames[0]:
                            self.dataFrame[row[0]]={fieldNames[i]: row[i] for i in range(len(fieldNames))}
            except Exception as e:
                self.dataFrame = CreateReplaceDialog(self.filepath,lambda file: writeEmpty(file),{},e)
        else:
            writeEmpty()
    def populate(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()[0:10]
        for file in files:
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
            fitting = fitter.fitFile(directory.absoluteFilePath(file),spectra)
            object = DataObject(file, spectra, fitting)
            dict = object.toDict()
            with open(self.filepath, 'a', newline='') as filepath:
                writer = csv.DictWriter(filepath, self.fieldNames, extrasaction = 'ignore')
                writer.writerow(dict)

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        with open(self.filepath, 'r', newline='') as file:      
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] != self.fieldNames[0]:
                    spectra = tool.SDSS_spectrum(directory.absoluteFilePath(row['name']))
                    fitting = fitter.fitFile(directory.absoluteFilePath(row['name']), spectra)
                    object = DataObject.fromDict(row, fitting)
                    object.file = spectra
                    files.append(object)     
        return files

    def getFile(self, name):
        pass

    def addEntry(self, name, fields, data):
        if (len(fields)!=len(data)+1):
            raise Exception("Expected fields to be one longer than data because of name field, but it is "+ len(fields))
        entry={}
        for i in range(len(data)):
            entry[fields[i+1]]=data[i]
        self.dataFrame[name]=entry
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(entry.values()))

    def getEntry(self, name):
        with open(self.filepath, 'r', newline = '') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[self.fieldNames[0]] == name:
                    return row
            return None

    def addFitting(self, l2):
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writerow(l2)

    def getFitting(self, name):
        with open(self.filepath, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[self.fieldNames[0]] == name:
                    return row
            return []        

    def getByName(self, name, default=[]):
        return self.dataFrame.get(name,default)

    def addByName(self, name, data):
        self.dataFrame[name]=data
        with open(self.filepath, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writerow(data)

    def getdataFrame(self):
        objs=[]
        for item in list(self.dataFrame.items()):
            spectra = tool.SDSS_spectrum((self.directory / Path(item[0]))) 
            dobject = DataObject(item[0], spectra, item[1])
            objs.append(dobject)
        return objs

def convert_l2(row):
    l2_product = dict()
    l2_product['OBJ_NME']       = row['OBJ_NME']
    l2_product['zBest']         = float(row['zBest'])
    l2_product['zBestProb']     = float(row['zBestProb'])
    l2_product['zBestType']     = row['zBestType']
    l2_product['zBestSubType']  = row['zBestSubType']
    
    def auxInsert(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  x.strip("'")) 
    
    def auxInsertFloat(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  float(x.strip(','))) 

    def aux(key, func):
        temp = row[key].strip('[]').split()
        new = []
        for i in range(len(temp)):
            func(temp,i,new)
        return new

    l2_product['zAltType'] = aux('zAltType',lambda temp,i,new: new.insert(i,  temp[i].strip("'")))

    l2_product['zAltSubType'] = aux('zAltSubType',auxInsert)

    l2_product['zAltProb'] = aux('zAltProb',auxInsertFloat)

    l2_product['zBestPars'] = np.array(aux('zBestPars',lambda temp,i,new: new.insert(i, float(temp[i].strip(',')))))
    return l2_product
    
