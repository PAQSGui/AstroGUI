import Spec_tools as tool
from DataObject import DataObject
import csv

from PySide6.QtCore import (
    QDir,
)

class Model:
    cursor = 0
    objects = []
    options: dict
    fieldNames = ['name', 'file', 'fitting', 'redshift']

    def __init__(self, path, fromCSV = False):
        # most of this below should be handled by a  seperate class filehandler:
        # it should also be paralelized and the amount of objects simultaniously in memory should be limited
        if fromCSV:
            with open('data.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
                    object = DataObject.fromDict(row)
                    self.objects.append(object)
        else:
            directory = QDir(path)
            directory.setNameFilters(["([^.]*)","*.fits"])
            files = directory.entryList()
            with open('data.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, self.fieldNames, extrasaction = 'ignore')
                writer.writeheader()
                for file in files:
                    spectra = tool.SDSS_spectrum(directory.absoluteFilePath(file)) 
                    object = DataObject(file, spectra, [], 0)
                    dict = object.toDict()
                    self.objects.append(dict)
                    writer.writerow(dict)

        # initilaize options

    def getFile(self, delta = 0):
        cursor = self.cursor + delta
        self.cursor = cursor
        return DataObject.fromDict(self.objects[cursor])

    def setOptions(self, opt, val):
        self.options[opt] = val
    
    def changeRedShift(self, val):
        self.redshifts[self.cursor] = val
