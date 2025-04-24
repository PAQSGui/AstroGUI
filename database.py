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

    def __init__(self, dataFile, fieldNames, type, path = ''):
        self.dataFile = dataFile
        self.fieldNames = fieldNames
        self.path = path
        index = "OBJ_NAME" if type == "fitter" else "name"

        if not os.path.isfile(dataFile):
            f = open(dataFile, 'a')
            header = ",".join(self.fieldNames)
            f.write(header)
            f.close()
        
        # By using name as the index, we might lose some value by not being fully able to pass around the series
        # But using name also makes it super easy to look up the object in the DataFrame, so I'm not sure what to do
        # since otherwise we would have to go back to linear search
        self.df = pd.read_csv(self.dataFile)
        #self.df = pd.read_csv(self.dataFile, index_col=index) 

        # with open(self.dataFile, 'a', newline='') as file:
        #     writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
        #     writer.writeheader()  

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
            # with open(self.dataFile, 'a', newline='') as dataFile:
            #     writer = csv.DictWriter(dataFile, self.fieldNames, extrasaction = 'ignore')
            #     writer.writerow(dict)
        self.df.to_csv(self.dataFile, index=False)

    def extract(self, fitter):
        directory = QDir(self.path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = []

        for _, row in self.df.iterrows(): # Grab all rows
            name = row['name']
            spectra = tool.SDSS_spectrum(directory.absoluteFilePath(name))
            fitting = fitter.fitFile(directory.absoluteFilePath(name), spectra)
            object = DataObject.fromSeries(row, fitting) # Why is it angery
            object.file = spectra #Why are we even even using file in fromDict if we're changing it here?
            files.append(object)
        return files



        # with open(self.dataFile, 'r', newline='') as file:      
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if row['name'] != self.fieldNames[0]:
        #             spectra = tool.SDSS_spectrum(directory.absoluteFilePath(row['name']))
        #             fitting = fitter.fitFile(directory.absoluteFilePath(row['name']), spectra)
        #             object = DataObject.fromDict(row, fitting)
        #             object.file = spectra
        #             files.append(object)
        # return files

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
        self.df.to_csv(self.dataFile, index = False)
        # with open(self.dataFile, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([name, categorized, category, note, redshift])

    def getEntry(self, name):
        for _, row in self.df.iterrows():
            if row['name'] == name:
                return row.to_dict()
        return None
        
        # Too much? Tried to make it match where it returns None if the row isn't found
        # try:
        #     entry = self.df.loc[name]
        # except KeyError:
        #     return None
        # return entry
        
        # with open(self.dataFile, 'r', newline = '') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if row[self.fieldNames[0]] == name:
        #             return row
        #     return None

    def addFitting(self, l2):
        self.df = pd.concat([self.df, pd.DataFrame([l2])], ignore_index=True)
        self.df.to_csv(self.dataFile, index = False)
        # with open(self.dataFile, 'a', newline='') as file:
        #     writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
        #     writer.writerow(l2)

    def getFitting(self, name):
        for _, row in self.df.iterrows():
            if row['OBJ_NME'] == name:
                return row.to_dict()
        return None
        # try:
        #     entry = self.df.loc[name]
        # except KeyError:
        #     return None
        # return entry
        # with open(self.dataFile, 'r', newline='') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if row[self.fieldNames[0]] == name:
        #             return row
        #     return []
