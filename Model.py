import Spec_tools as tool
from DataObject import DataObject
import csv
from fitter import Fitter

from PySide6.QtCore import (
    QDir,
)

class Model:
    cursor = 0
    objects = []
    options: dict
    fieldNames = ['name', 'file', 'fitting', 'redshift']
    fitter: Fitter

    def __init__(self, path, fromCSV = False):
        # most of this below should be handled by a  seperate class filehandler:
        # it should also be paralelized and 
        # the amount of objects simultaniously in memory should be limited
        self.fitter = Fitter()

        directory = QDir(path)
        directory.setNameFilters(["([^.]*)","*.fits"])
        files = directory.entryList()

        if fromCSV:
            with open('data.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    object = DataObject.fromDict(row)
                    object.file = tool.SDSS_spectrum(directory.absoluteFilePath(object.name))
                    object.fitting = self.fitter.fitFile(directory.absoluteFilePath(object.name))
                    self.objects.append(object)
        else:
            with open('data.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
                writer.writeheader()
                for file in files:
                    spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
                    fitting = self.fitter.fitFile(directory.absoluteFilePath(file))
                    object = DataObject(file, spectra, fitting, 0)
                    dict = object.toDict()
                    self.objects.append(dict)
                    writer.writerow(dict)

        # initilaize options

    def getFile(self):
        return self.objects[self.cursor].file
    
    def getState(self):
        return self.objects[self.cursor]
    
    def updateCursor(self, delta):
        self.cursor = self.cursor + delta 

    def setOptions(self, opt, val):
        self.options[opt] = val
    
    def changeRedShift(self, val):
        self.redshifts[self.cursor] = val

