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

        chi2 = l2_product['zBestChi2'] / l2_product['zBestNfree']
        #title_str += f"\n z = {z:.5f}  Class: {name}  $\\chi^2 = {chi2:.2f}$"
        plt.plot(wave, model, color='r', lw=1.0, alpha=0.7, label = l2_product['zBestSubType'])

        #set combobox text:
        #print(l2_product['zBestSubType']) 
        self.dropdown.setCurrentText(f'template-{l2_product['zBestSubType'].lower()}.fits') 
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
        
    