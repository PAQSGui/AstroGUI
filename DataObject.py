import Spec_tools as tool

class DataObject:

    name: str
    file: tool.SDSS_spectrum
    fitting: dict
    redshift: float

    def __init__(self, filename, file, fitting, redshift):
        self.name = filename
        self.file = file
        self.fitting = fitting
        self.redshift = redshift

    def toDict(self):
        selfDict = {
        'name': self.name,
        'file' : self.file,
        'fitting' : self.fitting,
        'redshift' : self.redshift }

        return selfDict
    
    def fromDict(dict):
        name = dict['name']
        file = dict['file']
        fitting = dict['fitting']
        redshift = dict['redshift']

        return DataObject(name, file, fitting, redshift)