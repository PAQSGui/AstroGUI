import csv
import Spec_tools as tool
from DataObject import DataObject
from PySide6.QtCore import (
    QDir,
)
import pandas as pd
import os.path
import numpy as np

class Database():
    dataFile = ""
    fieldNames = ""
    path : str

    def __init__(self, dataFile, fieldNames, path = ''):
        self.dataFile = dataFile
        self.fieldNames = fieldNames
        self.path = path

        if not os.path.isfile(dataFile):
            f = open(dataFile, 'a')
            header = ",".join(self.fieldNames)
            f.write(header)
            f.close()
        
        self.df = pd.read_csv(self.dataFile) 

    def load(self,dataFile):
        #load a file and return it as a dict
        df = pd.read_csv(dataFile)

    def write(self):
        self.df = self.df.drop_duplicates(subset=[self.fieldNames[0]], keep='last')
        self.df.to_csv(self.dataFile, index=False)

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        for _, row in self.df.iterrows():
            name = row['path']
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(name))
            obj = fitter.fitFile(directory.absoluteFilePath(name), spectra)
            obj.file = spectra #Why are we even even using file in fromDict if we're changing it here?
            files.append(obj)
        return files

    def addEntry(self, name, note, fieldnames, fields):
        if note == '':
            note = 'no-note'
        new_row = {
            "name": name,
            "note": note
        }
        new_row.update({fieldnames[i]: fields[i] for i in range(len(fieldnames))})
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.write()

    def getEntry(self, name, default):
        for _, row in self.df.iterrows():
            if row['name'] == name:
                return row.to_dict()
        return default

    def addFitting(self, l2):
        self.df = pd.concat([self.df, pd.DataFrame([l2])], ignore_index=True)
        self.write()

    def getFitting(self, name):
        for _, row in self.df.iterrows():
            if row['OBJ_NME'] == name:
                l2 = row.to_dict()
                return convert_l2(l2)
        return None

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