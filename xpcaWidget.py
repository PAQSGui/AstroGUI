from numpy import argsort, concatenate,array
from xpca.targets import ProvDict, Target

from xpca.spectrum import Spectrum
from os.path import basename
from astropy.io.fits import getheader
from re import search

from xpca.pipeline import Pipeline

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QLabel,
    QPushButton,
)

from PySide6.QtCore import Signal, Slot
"""
Helper-class for fitter
"""
class xpcaWindow(QWidget):

    def __init__(self, model):
        super().__init__()

        self.setWindowTitle("XPCA Wizard")
        self.model = model

        layout = QVBoxLayout()
        saveAll=QCheckBox("Save all template fits")
        self.startbtn=QPushButton("Start")
        canclbtn=QPushButton("Cancel")

        layout.addWidget(saveAll)
        layout.addWidget(QLabel("Run xpca on all loaded files?"))
        layout.addWidget(self.startbtn)
        layout.addWidget(canclbtn)
        canclbtn.clicked.connect(lambda: self.close())

        self.setLayout(layout)

        self.model.openedSession[list].connect(self.setupSession)

    def start(self):
        #self.model.fileDB.populate()
        self.model.xpcaDone.emit(0)
        self.close()
        
    @Slot()
    def setupSession(self,list):
        self.startbtn.clicked.connect(lambda: self.start())



def get_all_fits(pipeline, filePath, spec, src='sdss'):
        fullList=pipeline.active_templates[:]
        zaltpars={}
        altpipe = Pipeline(debug=False)
        for i in range(0,len(fullList)):
            altpipe.N_targets=1
            altpipe.active_templates=[fullList[i]]

            try:
                l2_product = altpipe.process_target(createTarget(filePath,spec), 0)[0]
                zaltpars[l2_product['zBestSubType']]=l2_product['zBestPars']
            except ValueError as e:
                print(e)
        pipeline.run(filePath, source=src)
        l2_product=pipeline.catalog_items[0]
        l2_product['zAltPars']=zaltpars
        return l2_product


def createTarget(filename,spec, fscale=1.):
    primary_header = getheader(filename, 0)
    result=search(f'.*([0-9]+).*', str(primary_header.get('OBJECT', 1)))
    prov = ProvDict(PROV=basename(filename),
                    OBID=primary_header.get('OBID1', 1),
                    PROG_ID=primary_header.get('PROG_ID', 'None'),
                    MJD_OBS=primary_header.get('MJD-OBS', 0.01),
                    MJD_END=primary_header.get('MJD-END', 0.02),
                    SPECUID=primary_header.get('SPECUID', -1),
                    OBJ_UID=int(result.group(1)),
                    OBJ_NME=str(primary_header.get('OBJECT', 1)),
                    )
    return Target(uid=prov.OBJ_UID,
                    name=prov.OBJ_NME,
                    spectrum=Spectrum(spec.Wavelength,
                                    spec.Flux * fscale,
                                    spec.Noise * fscale,
                                    unit_wl='AA',
                                    unit_flux='erg/(s cm2 AA)',
                                    ),
                    provenance=prov.as_dict(),
                    #meta=row.meta,
                    info=primary_header,
                    )
def findRedshiftForTemplate(templater, l2_product):
    for i in range(len(l2_product['zAlt'])):
            result=search(f'(NEW-)?(.+)', templater.model.getCategory().upper())
            if l2_product['zAltSubType'][i]==result.group(2):
                return l2_product['zAlt'][i]
    return None

def plotTemplate(templater):

    state = templater.model.getState()
    spec = state.file
    l2_product = state.fitting
    if l2_product['zBestSubType'].upper() != templater.model.getCategory().upper():
        l2_product['zBestSubType'] = templater.model.getCategory()
        newRedshift=templater.findRedshiftForTemplate(l2_product)
        if newRedshift is not None:
            templater.model.changeRedShift(newRedshift)
            l2_product['zBest'] = newRedshift
        try:
            l2_product['zBestPars'] = l2_product['zAltPars'][templater.model.getCategory().upper()]
        except Exception: #replace with a contains check
            result=search(f'NEW-(.+)', templater.model.getCategory().upper())
            l2_product['zBestSubType'] = result.group(1)
            l2_product['zBestPars'] = l2_product['zAltPars'][result.group(1)]
    
    l2_product['zBest'] = templater.model.getRedShift()
    target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
    
    try:
        wave, model = template.create_PCA_model(target, l2_product)
    except FileNotFoundError as e: #replace with a file exists check
        name = l2_product['zBestSubType']
        l2_product['zBestSubType'] = f'new-{name}'
        wave, model = template.create_PCA_model(target, l2_product)

    label = l2_product['zBestSubType']
    return plt.plot(wave, model, color=templater.model.getOption('TemplateColor'), lw=templater.model.getOption('LineWidth'), alpha=0.7, label = label)
