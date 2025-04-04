import csv
import Spec_tools as tool
from DataObject import DataObject
from PySide6.QtCore import (
    QDir,
)

class Database():
    dataFile = ""
    fieldNames = ""
    path : str

    def __init__(self, dataFile, fieldNames, path = ''):
        self.dataFile = dataFile
        self.fieldNames = fieldNames
        self.path = path 

        with open(self.dataFile, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
            writer.writeheader()  


    def populate(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()
        for file in files:
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
            fitting = fitter.fitFile(directory.absoluteFilePath(file))
            object = DataObject(file, spectra, fitting)
            dict = object.toDict()
            with open(self.dataFile, 'a', newline='') as dataFile:
                writer = csv.DictWriter(dataFile, self.fieldNames, extrasaction = 'ignore')
                writer.writerow(dict)

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        with open(self.dataFile, 'r', newline='') as file:      
            reader = csv.DictReader(file)
            for row in reader:
                object = DataObject.fromDict(row)
                object.file = tool.SDSS_spectrum(directory.absoluteFilePath(object.name))
                object.fitting = fitter.fitFile(directory.absoluteFilePath(object.name))
                files.append(object)     

        return files

    def getFile(self, name):
        pass

    def addEntry(self, name, categorized, category, note, redshift):
        with open(self.dataFile, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, categorized, category, note, redshift])

    def getEntry(self, name):
        with open(self.dataFile, 'r', newline = '') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[self.fieldNames[0]] == name:
                    return row
                return []


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
