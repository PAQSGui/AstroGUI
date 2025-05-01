import Spec_tools as tool
from PySide6.QtCore import (
    QDir,
)
import pandas as pd
import os.path
from os import makedirs
from numpy import array

"""
CSVDatabase handles reading from and writing to csv-files. 
They are used to store classifications made by the user as well as fittings made by xpca
"""
class Database():
    dataFile: str
    fieldNames: str
    path : str
    dataFrame: pd.DataFrame

    def __init__(self, dataFile, fieldNames, path = ''):
        self.dataFile = os.path.join('csv', dataFile+'.csv')
        self.fieldNames = fieldNames
        self.path = path

        if not os.path.isfile(self.dataFile):
            if not os.path.exists('csv'):
                makedirs('csv')
            file = open(self.dataFile, 'a')
            header = ','.join(self.fieldNames)
            file.write(header)
            file.close()
        
        self.dataFrame = pd.read_csv(self.dataFile) 

    def write(self):
        self.dataFrame = self.dataFrame.drop_duplicates(subset=[self.fieldNames[0]], keep='last')
        self.dataFrame.to_csv(self.dataFile, index=False)

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(['([^.]*)','*.fits'])
        files = []

        for _, row in self.dataFrame.iterrows():
            path = row['path']
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(path))
            obj = fitter.fitFile(directory.absoluteFilePath(path), spectra)
            obj.file = spectra
            files.append(obj)
        return files

    def addEntry(self, fieldnames, fields):
        new_row ={fieldnames[i]: fields[i] for i in range(len(fieldnames))}
        self.data = pd.concat([self.dataFrame, pd.DataFrame([new_row])], ignore_index=True)
        self.write()

    def getEntry(self, name, default):
        for _, row in self.dataFrame.iterrows():
            if row['name'] == name:
                return row.to_dict()
        return default

    def addFitting(self, name, l2):
        l2['name'] = name
        self.dataFrame= pd.concat([self.dataFrame, pd.DataFrame([l2])], ignore_index=True)
        self.write()

    def getFitting(self, name):
        for _, row in self.dataFrame.iterrows():
            if row['name'] == name:
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
    
    def auxInsertString(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  x.strip('\'')) 
    
    def auxInsertFloat(temp,i,new):
        x = temp[i]
        if x != '--':
            new.insert(i,  float(x.strip(','))) 

    def auxParseList(key, func):
        temp = row[key].strip('[]').split()
        new = []
        for i in range(len(temp)):
            func(temp,i,new)
        return new

    l2_product['zAltType'] = auxParseList('zAltType',lambda temp,i,new: new.insert(i,  temp[i].strip('\'')))

    l2_product['zAltSubType'] = auxParseList('zAltSubType',auxInsertString)

    l2_product['zAltProb'] = auxParseList('zAltProb',auxInsertFloat)

    l2_product['zBestPars'] = array(auxParseList('zBestPars', lambda temp, i, new: new.insert(i, float(temp[i].strip(',')))))
    return l2_product
