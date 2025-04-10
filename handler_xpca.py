from numpy import argsort, concatenate,array
from xpca.targets import ProvDict, Target

from xpca.spectrum import Spectrum
from os.path import basename
from astropy.io.fits import getheader
from re import search
def get_all_fits(pipeline, filePath, spec, src='sdss'):
        #debug mode possible allows us to get the full output, i.e. all zaltpars
        #It's pretty hard to understand
        #make a copy of the list of processed templates
        fullList=pipeline.active_templates[:]
        #run the pipeline to get most of the info
        pipeline.run(filePath, source=src)
        #iterate over each template, fitting to it and adding the result into an array
        zaltpars=[]
        for i in range(0,len(fullList)):
            pipeline.active_templates=fullList[i:i+1]

            l2_product = pipeline.process_target(createTarget(filePath,spec), 0)
            zaltpars.append(l2_product['zBestSubType'],l2_product['zBestPars'])
        #sort by highest probability (https://www.skytowner.com/explore/sorting_value_of_one_array_according_to_another_in_python)
        #then set the list to full again.
        pipeline.active_templates=fullList
        print(zaltpars)
        pipeline.catalog_items[0]['zAltPars']=zaltpars


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
                    OBJ_NME=primary_header.get('OBJECT', 1),
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