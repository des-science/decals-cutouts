# DECaLS Cutout Viewer
Create cutout and url for DES Y6 coadd object using the DECaLS viewer.

## Install
```
git clone https://github.com/des-science/decals-cutouts.git
cd decals-cutouts
```

## Usage

The script can be run for a specific DES Y6 COADD_OBJECT_ID (in this case `919605106`). From the directory hosting the script:

```
> ./decals-cutout.py 919605106
```

The first time the tool is run it will download a catalog database file to the current directory on your machine (database.fits). Subsequent runs will use this database file.

Full usage options can be found from the help string.
```
> ./decals-cutout.py -h
usage: decals-cutout.py [-t TABLE] [-h] [-d DATABASE] [-r RELEASE] [-v] [-z ZOOM] objid

Create cutout and url for DES Y6 coadd object using the DECaLS viewer.

positional arguments:
  objid                 DES Y6 COADD_OBJECT_ID

options:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        database file name
  -r RELEASE, --release RELEASE
                        DECaLS viewer release layer
  -v, --verbose         output verbosity
  -z ZOOM, --zoom ZOOM  zoom level
  -t, --table TABLE     specify which table to use in easyaccess
```
