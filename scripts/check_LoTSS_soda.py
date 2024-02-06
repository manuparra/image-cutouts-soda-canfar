import sys
import pyvo as vo
from astropy import units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astroquery.vo_conesearch import conesearch
from astropy.io.votable import parse_single_table
import requests
import six

import numpy as np
import pandas
import json
import click

service_url = 'https://ivoa.dachs.srcdev.skao.int:443/rucio/rucio/cone/scs.xml?'

#@click.group()
#def cli():
#    pass
    
@click.command()
@click.argument("obj_list_file", type=click.File("rb"))
def cli(obj_list_file):
    # Read in sources to plot from CSV
    print(f"Reading source list file {obj_list_file}")
    srcs = pandas.read_csv(obj_list_file)
    nsrc = len(srcs)
    print(f"{nsrc} sources read hic")

    # Store column names as used in file
    cols = srcs.columns
    name_col = cols[0]
    ra_col = cols[1]
    dec_col = cols[2]
    siz_col = cols[3]

    rmin = 1.5

    # Read sources from dataframe into arrays
    name = srcs[name_col].values
    ra = srcs[ra_col].values
    dec = srcs[dec_col].values
    siz = srcs[siz_col].values
    src_pos = SkyCoord(ra*u.deg, dec*u.deg)

    res = [] # list to store results
    # Now go through sources checking if in known image field
    image_pos = [] # Get running store of image centre positions
    image_tab = [] # and it's corresponding VO table
    for i in range(len(src_pos)):

        print(i)
        pos = src_pos[i]

        # First check if source is already within known field
        if len(image_pos)!=0:
    
            sep =[]
            for ip in image_pos:    
                sep.append(ip.separation(pos).deg)
            sep = np.array(sep)    
            min_pos = np.argmin(sep)
        
            if sep[min_pos]<rmin: 

                r = image_tab[min_pos]
            
                res.append((name[i],r))         
                continue

        
        tables = conesearch.conesearch(pos, 2.0*u.degree, catalog_db=service_url)
        sep = [] # Go through images checking for centre position
        for tab in tables:
    
            ra = tab['s_ra']*u.deg
            dec = tab['s_dec']*u.deg
            image_cen = SkyCoord(ra,dec)
            sep.append(tab['distCol'])

    
        min_pos = int(np.argmin(sep))
        access_url = tables[min_pos]['access_url']

        # Follow access url
        response = requests.get(access_url)
        if response.status_code == 200:
            data = response.text  # or response.content for binary data
            # Process the data
            votable = parse_single_table(six.BytesIO(data.encode('utf-8'))).to_table()
            image_url = votable[0]['ID']

        else:
            print(f"Failed to retrieve data: Status code {response.status_code}")
            continue

        res.append((name[i],image_url))
        image_pos.append(image_cen)
        image_tab.append(image_url) 

    # Write to JSON file
    with open('data_soda.json', 'w') as outfile:
        json.dump(res, outfile)


