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
            f = open(dataFile, "a")
            f.write("name,categorized,category,redshift,note")
        
        self.df = pd.read_csv(self.dataFile, index_col="name")

        # with open(self.dataFile, 'a', newline='') as file:
        #     writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
        #     writer.writeheader()  

    # Ignore for now
    def populate(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()[0:10]
        for file in files:
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
            fitting = fitter.fitFile(directory.absoluteFilePath(file),spectra)
            object = DataObject(file, spectra, fitting)
            dict = object.toDict()
            with open(self.dataFile, 'a', newline='') as dataFile:
                writer = csv.DictWriter(dataFile, self.fieldNames, extrasaction = 'ignore')
                writer.writerow(dict)

    # needed?
    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        for row in self.df[:]: # Grab all rows
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath())



        with open(self.dataFile, 'r', newline='') as file:      
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

    def addEntry(self, name, categorized, category, note, redshift):
        entry = pd.DataFrame([name, categorized, category, note, redshift])
        self.df = pd.concat([self.df, entry], ignore_index=True)
        # with open(self.dataFile, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([name, categorized, category, note, redshift])

    def getEntry(self, name):
        try:
            entry = self.df.loc[name]
        except KeyError:
            return None
        return entry
        
        # with open(self.dataFile, 'r', newline = '') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if row[self.fieldNames[0]] == name:
        #             return row
        #     return None

    def addFitting(self, l2):
        with open(self.dataFile, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writerow(l2)

    def getFitting(self, name):
        with open(self.dataFile, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[self.fieldNames[0]] == name:
                    return row
            return []        
