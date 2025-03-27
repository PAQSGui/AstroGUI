import matplotlib.pyplot as plt
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
        
        self.zSlider = QSlider(Qt.Orientation.Horizontal)
        self.zSlider.setSingleStep(1)
        self.zSlider.sliderMoved.connect(self.slider_changed)
        self.zSlider.sliderReleased.connect(self.sliderrelease)
        self.layout.addWidget(self.zSlider)
        self.dropdown = QComboBox()
        for file in listdir(config.TEMPLATE_PATH):
            if file.endswith(".fits"):
                self.dropdown.addItem(file)
        self.layout.addWidget(self.dropdown)

        self.dropdown.textActivated.connect(self.text_changed)

    def plotTemplate(self, spec, l2_product, firstLoad = False):
        target=Target(uid=0,name="temp",spectrum=Spectrum(spec.Wavelength*Unit("AA"),spec.Flux*Unit("erg/(s cm2 AA)"),spec.Noise*Unit("erg/(s cm2 AA)")))
        try:
            wave, model = template.create_PCA_model(target,l2_product)
        except FileNotFoundError:
            print("not found, trying by appending new, this is a bad solution tho")
            name = l2_product['zBestSubType']
            print(name)
            l2_product['zBestSubType']=f'new-{name}'
            wave, model = template.create_PCA_model(target,l2_product)
        plt.plot(wave, model, color='r', lw=1.0, alpha=0.7, label = l2_product['zBestSubType'])

        #set combobox text:
        best = l2_product['zBestSubType'].lower()
        print(f'template-%s' % best)
        self.dropdown.setCurrentText(f'template-%s.fits' % best)
        self.spec_current=spec
        self.l2_current=l2_product
        if firstLoad:
            self.setMiddle(l2_product)
            

    def sliderrelease(self):
        self.l2_current['zBest']=float(self.zSlider.value())/100
        self.setMiddle(self.l2_current)
        self.plotter.PlotFile(self.l2_current)
        
    def setMiddle(self,l2_product):
        newMiddle = l2_product['zBest']*100
        self.zSlider.setMinimum(newMiddle-100)
        self.zSlider.setMaximum(newMiddle+100)
        self.zSlider.setValue(newMiddle)
    
    def slider_changed(self,s):
        self.l2_current['zBest']=float(self.zSlider.value())/100

        self.plotter.PlotFile(self.l2_current, first = False)

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