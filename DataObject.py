import Spec_tools as tool

class DataObject:

    filename: str
    file: tool.SDSS_spectrum
    fitting: dict
    redshift: float

    def __init__(self, filename, file, fitting, redshift):
        self.filename = filename
        self.file = file
        self.fitting = fitting
        self.redshift = redshift

    def toDict(self):
        selfDict = {
        'name': self.filename,
        'file' : self.file,
        'fitting' : self.fitting,
        'redshift' : self.redshift }

        return selfDict
    
    def fromDict(dict):
        filename = dict['name']
        file = dict['file']
        fitting = dict['fitting']
        redshift = dict['redshift']

        return DataObject(filename, file, fitting, redshift)