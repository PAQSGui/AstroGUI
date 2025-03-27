import matplotlib.pyplot as plt
from Spec_tools import Fies_spectrum
import numpy as np

from astropy.io.fits import getdata
from astropy.io.fits import getheader
from astropy.io import fits
from astropy.units import Unit

from xpca.targets import Target
from xpca.spectrum import Spectrum
from xpca import plotting as template

from PySide6.QtWidgets import (
    QHBoxLayout,
    QComboBox,
    QSlider,
    )
from PySide6.QtGui import (
    Qt,
)
from xpca import config
#https://www.geeksforgeeks.org/list-all-files-of-certain-type-in-a-directory-using-python/
from os import listdir

import re
#from shutil import copyfile

class Templater:

    layout: QHBoxLayout 
    dropdown: QComboBox

    def __init__(self, plotter):
        self.plotter = plotter
        self.layout = QHBoxLayout()
        
        self.layout.addWidget(QSlider(Qt.Orientation.Horizontal))
        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)
        self.layout.addWidget(self.dropdown)

        self.dropdown.textActivated.connect(self.text_changed)

    def plotTemplate(self, spec, l2_product):
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        try:
            wave, model = template.create_PCA_model(target,l2_product)
        except FileNotFoundError:
            print("not found, trying by appending new, this is a bad solution tho")
            name = l2_product['zBestSubType']
            print(name)
            l2_product['zBestSubType']=f'new-{name}'
            wave, model = template.create_PCA_model(target,l2_product)
        #except ValueError:
        #    print(l2_product['zBestPars'])
        #    l2_product['zBestPars']=np.append(l2_product['zBestPars'],[1,1,1,1])
        #    print(l2_product['zBestPars'])
        #    wave, model = template.create_PCA_model(target,l2_product)
        plt.plot(wave, model, color='r', lw=1.0, alpha=0.7, label = l2_product['zBestSubType'])

        #set combobox text:
        #print(l2_product['zBestSubType']) 
        best = l2_product['zBestSubType'].lower()
        self.dropdown.setCurrentText(f'template-%s' % best) 
        self.spec_current=spec
        self.l2_current=l2_product
    

    def text_changed(self, s):

        result = re.search(f'template-(.+).fits', s)
        self.l2_current['zBestSubType']=result.group(1)
        
        try:
            self.plotter.PlotFile(self.l2_current)
        except FileNotFoundError:
            for file in listdir(config.TEMPLATE_PATH):
                if file.lower()==s:
                    result = re.search(f'template-(.+).fits', file)
                    self.l2_current['zBestSubType']=result.group(1)
                    self.plotter.PlotFile(self.l2_current)
                    break
        
    #except FileNotFoundError:
    #        for file in listdir(config.TEMPLATE_PATH):
    #            result = re.search(f'template-(?:new-)?(.+).fits', file)
    #            if result!=None and result.group(1).lower()==l2_product['zBestSubType'].lower:
    #                copyfile(config.TEMPLATE_PATH / file, config.TEMPLATE_PATH / l2_product['zBestSubType'].lower)
    #                wave, model = template.create_PCA_model(target,l2_product)
    #                break