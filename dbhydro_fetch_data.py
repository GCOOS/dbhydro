#!/usr/bin/env python3
"""Name:       dbhydro_fetch_data.

Author:     robertdcurrier@gmail.com
Created:    2020-07-07
Modified:   2021-06-25
Notes:      Example of pulling data from dbhydro RESTful API
Pylint:     10.0
"""
import json
import sys
import io
import requests
import logging
import pandas as pd
from datetime import date


def config_logging():
    """ Define console and file  logging. """
    logger = logging.getLogger('DB_Hydro')
    logger.setLevel(logging.INFO)

    logger_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-2s %(message)s',
                                          datefmt='%Y-%m-%d %I:%M:%S %p %Z')
    dts = date.today().strftime('%Y-%m-%d')
    logfile = './logs/%s.log' % dts
    flogger = logging.FileHandler(logfile)
    flogger.setFormatter(logger_formatter)

    conlogger = logging.StreamHandler()
    conlogger.setFormatter(logger_formatter)

    logger.addHandler(flogger)
    logger.addHandler(conlogger)
    return logger


def get_config():
    """Name:       get_config.

    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2021-06-25
    Notes:      dbhydro_fetch config file
    """
    data_file = "./dbhydro.cfg"
    logger.info("get_config(%s)" % data_file)
    config = open(data_file, 'r').read()
    config = json.loads(config)
    return config


def fetch_wq_data(station, config, logger):
    """Name:       fetch_wq_data.

    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2021-06-25
    Notes:      Gets base URL from configuration file and uses requests to
    get station data from the DBHYDRO RESTful API
    """
    url = config['dbhydro_wq_url']
    station_id = "station_id='%s'" % station
    url = url.replace('station_id=', station_id)

    logger.info('fetch_wq_data(): Fetching %s' % station)
    try:
        resp = requests.get(url)
    except requests.ConnectionError as error:
        logger.info("fetch_wq_data() Failed with error %s" % error)
    # Consider any status other than 2xx an error
    if not resp.status_code // 100 == 2:
        logger.info('fetch_wq_data(): Unexpected response {}'.format(resp))
        return False
    data_frame = pd.read_csv(io.StringIO(resp.content.decode('utf-8')))
    return data_frame


def extract_wq_station_data(station, data_frame, config, logger):
    """Name:       extract_wq_station_data.

    Author:     robertdcurrier@gmail.com
    Created:    2020-07-08
    Modified:   2021-06-25
    Notes:      Iterates over variables in config file and extracts readings
    from data frame. Added station so we can debug logger.info station name.
    """
    logger.info("extract_wq_station_data(%s)" % station)
    dbhvars = config['variables']
    new_df = data_frame[dbhvars].copy().dropna()
    return new_df


def extract_flow_station_data(station, data_frame, config, logger):
    """Name:       extract_flow_station_data.

    Author:     robertdcurrier@gmail.com
    Created:    2021-06-25
    Modified:   2021-06-25
    Notes:      Iterates over variables in config file and extracts readings
    from data frame. Added station so we can debug logger.info station name.
    """
    logger.info("extract_flow_station_data(%s)" % station)
    dbhvars = config['variables']
    new_df = data_frame[dbhvars].copy().dropna()
    return new_df


def process_wq_stations(logger):
    """Name:    process_wq_stations

    Author:     robertdcurrier@gmail.com
    Created:    2020-07-07
    Modified:   2021-06-25
    Notes:      Modified for use by Ashley Brereton
    """
    config = get_config()
    logger.info('processing water quality stations...')
    for site in config['wq_stations']:
        station = site['station']
        data_frame = fetch_wq_data(station, config, logger)
        extracted_df = extract_wq_station_data(station, data_frame, config, logger)
        if len(extracted_df) > 0:
            filename = "reports/%s.csv" % station
            logger.info('process_wq_stations(): Writing %s' % filename)
            csv = extracted_df.to_csv(filename, index=False)
        else:
            logger.warning('process_wq_stations(): %s returned no data.' % station)


def process_flow_stations(logger):
        """Name:    process_flow_stations

        Author:     robertdcurrier@gmail.com
        Created:    2021-06-25
        Modified:   2021-06-25
        Notes:      Split process stations into wq and flow
        """
        pass


if __name__ == '__main__':
    logger = config_logging()
    process_wq_stations(logger)
    process_flow_stations(logger)
