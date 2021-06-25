#!/usr/bin/env python3
"""
Notes:      Pull data from DBHydro and export to csv file
Pylint:     
"""

import json
import io
import requests
import pandas as pd
import pickle as pk
import datetime
import numpy as np
import xarray as xr


def get_config():
    """
    Name:       get_config
    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2020-07-07
    Notes:      dbhydro_fetch config file
    """

    print 'get_config()...'
    data_file = './dbhydro.cfg'
    config = open(data_file, 'r').read()
    config = json.loads(config)
    return config


def fetch_station_data(station, config):
    """
    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2020-07-07
    Note: Request data for the given station
    """

    url = config['dbhydro_url']
    station_id = 'station_id=27%(%s)%27' % station
    url = url.replace('station_id=', station_id)
    print 'fetch_data(%s)' % station
    try:
        resp = requests.get(url)
    except requests.ConnectionError, error:
        print 'fetch_station_data() Failed with error %s' % error

  # Consider any status other than 2xx an error

    if not resp.status_code // 100 == 2:
        print 'fetch_data(): Unexpected response {}'.format(resp)
        return False

    data_frame = pd.read_csv(io.StringIO(resp.content.decode('utf-8')))
    return data_frame


def extract_station_data(data_frame, config):
    """
    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2020-07-07
    Note: Iterate over variables in config file and extracts reading from dataframe
    """

    print 'extract_station_data()'
    dbhvars = config['variables']
    new_df = data_frame[dbhvars].copy()
    return new_df


def to_csv(dataframe, config):
    """
    Note: save the dataframe to the given path and with the given name 
    from the config file.
    """

    path = config['data_path']
    file_name = config['out_file']
    dataframe.to_csv(path + '/' + file_name)


def init_app():
    config = get_config()
    for station in config['stations']:
        data_frame = fetch_station_data(station, config)
        extracted = extract_station_data(data_frame, config)
        to_csv(extracted, config)
        print extracted


if __name__ == '__main__':
    print 'dbhydro_fetch_data(): Running as command line app...'
    init_app()
