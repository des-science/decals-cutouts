#!/usr/bin/env python
"""
Create cutout and url for DES Y6 coadd object using the DECaLS viewer.
"""
import os, os.path
import urllib
import shutil
import tempfile
import subprocess

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image

from astropy.io import fits

DATABSE = "https://github.com/des-science/decals-cutouts/releases/download/v0.1/database_v0.fits"
QUERY = 'select ra, dec from {table}_coadd_object_summary where coadd_object_id = {objid};'
URL_QUERY = "ra={ra}&dec={dec}&zoom={zoom}&layer={release}"
VIEWER_URL = "https://www.legacysurvey.org/viewer?{query}"
CUTOUT_URL = "http://legacysurvey.org/viewer/cutout.jpg?{query}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('objid',type=int,
                        help='DES Y6 COADD_OBJECT_ID')
    parser.add_argument('-d','--database',default='database.fits',
                        help='database file name')
    parser.add_argument('-r','--release',default='ls-dr10',
                        help='DECaLS viewer release layer')
    parser.add_argument('-v','--verbose',action='store_true',
                        help='output verbosity')
    parser.add_argument('-z','--zoom',default=12,type=int,
                        help='zoom level')
    parser.add_argument('-t','--table',help='table for easyaccess')
    args = parser.parse_args()

    if args.database == 'dessci':
        # Query the DESDM database
        import easyaccess as ea
        conn = ea.connect(section='dessci')
        if args.table is None:
            table = 'y6a2'
        else:
            table = args.table
        query = QUERY.format(table=table,objid=args.objid)
        if args.verbose: print(f"Querying DESDM database:\n{query}")
        df = conn.query_to_pandas(query)
        ra,dec = df['RA'].values[0], df['DEC'].values[0]
    elif args.database == 'delve':
        import easyaccess as ea
        conn = ea.connect(section='delve')
        if args.table is None:
            table = 'dr3_1_1'
        else:
            table = args.table
        query = QUERY.format(table=table,objid = args.objid)
        if args.verbose: print(f"Querying DESDM database:\n{query}")
        df = conn.query_to_pandas(query)
        ra,dec = df['RA'].values[0], df['DEC'].values[0]
    else:
        # Query the catalog file
        if not os.path.exists(args.database):
            print("Downloading catalog file...")
            cmd = f"wget {DATABSE} -O {args.database}"
            if args.verbose: print(cmd)
            subprocess.check_call(cmd, shell=True)

        if args.verbose: print(f"Opening catalog: {args.database}")
        with fits.open(args.database) as f:
            catalog = f[1].data

        select = catalog['COADD_OBJECT_ID'] == args.objid
        ra = catalog['RA'][select][0]
        dec =catalog['DEC'][select][0]

    if args.verbose: print(f"RA, Dec = {ra},{dec}")

    url_query = URL_QUERY.format(ra=ra,dec=dec,zoom=args.zoom,release=args.release)
    viewer_url = VIEWER_URL.format(query=url_query)
    print(f"DECaLS Viewer URL:\n {viewer_url}\n")

    cutout_url = CUTOUT_URL.format(query=url_query)
    print(f"DECaLS Cutout URL:\n {cutout_url}\n")
    with tempfile.NamedTemporaryFile(mode="wb",delete=True) as fig_name:
        try:
            req=urllib.request.Request(cutout_url)
            urllib.request.urlretrieve(cutout_url, fig_name.name)
        except HTTPError as e:
            content = e.read()
            print(content)
        image = Image.open(fig_name.name)
        image.show()
