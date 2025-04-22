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
        self.model.populate()
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
                #pipeline.process_target is much faster, but it spams logs, so lets just use run for now
                l2_product = altpipe.process_target(createTarget(filePath,spec), 0)[0]
                print(l2_product)
                #altpipe.run(filePath, source=src)
                #l2_product=altpipe.catalog_items[0]
                zaltpars[l2_product['zBestSubType']]=l2_product['zBestPars']#,l2_product['zBest']
                #pipeline.reset()
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