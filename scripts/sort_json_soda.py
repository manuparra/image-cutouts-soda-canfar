import json
import click
import pandas
from astropy.io import fits
from astropy import wcs
from astropy.nddata.utils import Cutout2D,NoOverlapError
from astropy import units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import requests
import numpy as np
import os, sys

soda_url = "http://spsrc33.iaa.csic.es:18022/soda"

@click.group()
def cli():
    pass

@click.command()
#@click.option('--survey-dir',default='images',help='Directory for downloaded images')
@click.option('--output-dir',default='output',help='Directory for cutouts')
@click.argument('source_list', type=click.Path(exists=True), )
@click.argument('input_json', type=click.Path(exists=True), )
def make_fits(source_list, input_json, output_dir):
    """Make directory of fits cutout images"""
 
    # Read JSON file
    urls = _process_JSON(input_json)

    # Read in source list
    srcs = pandas.read_csv(source_list)
    cols = srcs.columns

    name_col = cols[0]
    ra_col = cols[1]
    dec_col = cols[2]
    siz_col = cols[3]

    names = srcs[name_col].values
    ra = srcs[ra_col].values
    dec = srcs[dec_col].values
    siz = srcs[siz_col].values/50.0

    nsrc = len(names)

    # Made cutouts for each source
    for i in range(nsrc):
        did_url = urls[names[i]]
        pos = f"{ra[i]} {dec[i]} {siz[i]}"
        params = {"ID":did_url, "CIRCLE":pos}  
        outfile = f"{output_dir}/{names[i]}_soda.fits"

        response = requests.get(soda_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the data to a file
            with open(outfile, "wb") as f:
                f.write(response.content)
        else:
                print("Error:", response.status_code)

     
def _process_JSON(input_json):

      # Open the JSON file
    with open(input_json, 'r') as infile:
        data = json.load(infile)

    # Make dictionary to look up image url from source name
    urls = {}
    for item in data:
        urls[item[0]] = item[1]
      
    return urls
  


cli.add_command(make_fits)

if __name__ == '__main__':
    cli()
