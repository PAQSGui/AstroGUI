import csv
import Spec_tools as tool
from DataObject import DataObject
from PySide6.QtCore import (
    QDir,
)
import pandas as pd
import os.path

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

    def write(self):
        self.df = self.df.drop_duplicates(subset=[self.fieldNames[0]], keep='last')
        self.df.to_csv(self.dataFile, index=False)

    def populate(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()[0:5]
        for file in files:
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
            fitting = fitter.fitFile(directory.absoluteFilePath(file),spectra)
            object = DataObject(file, spectra, fitting)
            dict = object.toDict()
            self.df = pd.concat([self.df, pd.DataFrame([dict])], ignore_index=True)
        self.write()

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        for _, row in self.df.iterrows():
            name = row['name']
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(name))
            fitting = fitter.fitFile(directory.absoluteFilePath(name), spectra)
            object = DataObject.fromSeries(row, fitting) # Why is it angery
            object.file = spectra #Why are we even even using file in fromDict if we're changing it here?
            files.append(object)
        return files

    def addEntry(self, name, categorized, category, redshift, note):
        if note == '':
            note = 'no-note'
        new_row = {
            "name": name,
            "categorized": categorized,
            "category": category,
            "redshift": redshift,
            "note": note
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.write()

    def getEntry(self, name):
        for _, row in self.df.iterrows():
            if row['name'] == name:
                return row.to_dict()
        return None

    def addFitting(self, l2):
        self.df = pd.concat([self.df, pd.DataFrame([l2])], ignore_index=True)
        self.write()

    def getFitting(self, name):
        for _, row in self.df.iterrows():
            if row['OBJ_NME'] == name:
                return row.to_dict()
        return None
