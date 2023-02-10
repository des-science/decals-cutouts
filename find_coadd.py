#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import pandas as pd
import urllib
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import astropy.io.fits as pyfits
from os.path import exists
import fitsio as ft
import shutil
import tempfile
y6_gold = ft.read("database.fits")

coadd = int(input("Enter Coadd ID:"))

select_coadd = np.isin(y6_gold['COADD_OBJECT_ID'],coadd)
ra = y6_gold['RA'][select_coadd]
dec = y6_gold['DEC'][select_coadd]
url_name = "http://legacysurvey.org/viewer/cutout.jpg?ra={0}&dec={1}&zoom={2}&layer=ls-dr10".format(ra[0],
                                                                                                    dec[0],
                                                                                                    "12")
print('DECaLS URL: ', 'http://legacysurvey.org/viewer?ra={0}&dec={1}&layer=ls-dr10&zoom={2}'.format(ra[0],
                                                                                                   dec[0],
                                                                                                   "12"))

with tempfile.NamedTemporaryFile(mode="wb",delete=True) as fig_name:
    try:
        req=urllib.request.Request(url_name)
        urllib.request.urlretrieve(url_name, fig_name.name)
    except HTTPError as e:
        content = e.read()
    image = Image.open(fig_name.name)
    image.show()



