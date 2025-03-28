#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download_ERA_daily.py
@Time    :   2025/03/20 13:51:27
@Author  :   Jiashun Wang 
@Version :   1.0
@Contact :   wjs@ieee.org
'''


import cdsapi

dataset = "derived-era5-single-levels-daily-statistics"
request = {
    "product_type": "reanalysis",
    "variable": ["surface_net_solar_radiation"],
    "year": "1993",
    "month": ["01"],
    "day": ["01"],
    "daily_statistic": "daily_mean",
    "time_zone": "utc+00:00",
    "frequency": "1_hourly"
}

save_path = 'data/output_file.nc' 

client = cdsapi.Client()
client.retrieve(dataset, request,save_path)
