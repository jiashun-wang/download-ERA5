# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:54:38 2021

@author: Dong
"""

import cdsapi
import requests

# CDS API script to use CDS service to retrieve daily ERA5* variables and iterate over
# all months in the specified years.

# Requires:
# 1) the CDS API to be installed and working on your system
# 2) You have agreed to the ERA5 Licence (via the CDS web page)
# 3) Selection of required variable, daily statistic, etc

# Output:
# 1) separate netCDF file for chosen daily statistic/variable for each month

c = cdsapi.Client(timeout=300)

# Uncomment years as required

years =  [
            '1979'
            ,'1980', '1981',
            '1982', '1983', '1984',
            '1985', '1986', '1987',
            '1988', '1989', '1990',
            '1991', '1992', '1993',
            '1994', '1995', '1996',
            '1997', '1998', '1999',
            '2000', '2001', '2002',
            '2003', '2004', '2005',
            '2006', '2007', '2008',
            '2009', '2010', '2011',
            '2012', '2013', '2014',
            '2015', '2016', '2017',
            '2018', '2019', '2020',
            '2021', '2022'
]


# Retrieve all months for a given year.

months = ['01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12']

# For valid keywords, see Table 2 of:
# https://datastore.copernicus-climate.eu/documents/app-c3s-daily-era5-statistics/C3S_Application-Documentation_ERA5-daily-statistics-v2.pdf

# select your variable; name must be a valid ERA5 CDS API name.
var = "surface_latent_heat_flux"

# Select the required statistic, valid names given in link above
stat = "daily_mean"

# Loop over years and months

for yr in years:
    for mn in months:
        result = c.service(
        "tool.toolbox.orchestrator.workflow",
        params={
             "realm": "user-apps",# "realm": "user-apps" or "c3s",
             "project": "app-c3s-daily-era5-statistics",
             "version": "master",
             "kwargs": {
                 "dataset": "reanalysis-era5-single-levels",
                 "product_type": "reanalysis",
                 "variable": var,
                 "statistic": stat,
                 "year": yr,
                 "month": mn,
                 "time_zone": "UTC+00:0",
                 "frequency": "1-hourly",
#
# Users can change the output grid resolution and selected area
#
                "grid": "0.25/0.25",
                "area":{"lat": [-15, 15], "lon": [90, 144]}

                 },
        "workflow_name": "application"
        })

# set name of output file for each month (statistic, variable, year, month

        file_name = "ERA5_" + stat + "_" + var + "_" + yr + "_" + mn + ".nc"

        location=result[0]['location']
        res = requests.get(location, stream = True)
        print("Writing data to " + file_name)
        with open(file_name,'wb') as fh:
            for r in res.iter_content(chunk_size = 1024):
                fh.write(r)
        fh.close()
