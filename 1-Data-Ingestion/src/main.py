# @author Hongwei
from fetchdata import fetch_data
from wrangling import pre_process
from awsservice import upload_data
import json
import datetime
import logging
import os


def main():
    # Log
    logger = save_logs()

    # Config.json location
    configFile = 'config.json'
    with open(configFile) as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings from env as prefers
    # Loading Global settings from json as default
    teamNum = str(config['team'])
    assignNum = str(config['assignNum'])
    curr_date = datetime.datetime.now().strftime('%Y%m%d')

    ACCESS_KEY = os.environ.get('AWSACCESS', str(config['AWSAccess']))
    SECRET_KEY = os.environ.get('AWSSECRET', str(config['AWSSecret']))
    region = os.environ.get('REGION', str(config['region']))

    # API request params
    username = os.environ.get('EPAUSERNAME', str(config['username']))
    password = os.environ.get('EPAPASSWORD', str(config['password']))
    data_format = str(config['data_format'])
    pc = str(config['parameter_class'])
    bdate = os.environ.get('BDATE', str(config['begin_date']))
    edate = os.environ.get('EDATE', str(curr_date))
    state = str(config['state'])
    county = str(config['county'])

    # Variables
    bucketName = 'team' + str(teamNum) + 'assignment' + assignNum

    # 1. Fetch data from EPA API
    # And Save to local as "rawdata-bdate-edate.txt"
    raw_file = fetch_data(username, password, data_format, pc, bdate, edate, state, county, logger)
    if raw_file is None:
        logger.error("Download from EPA Failed")
        print("Download from EPA Failed. Find Details in logs.")
        return

    # 2. Load data and clean
    # And Save to local as "clean-bdate-edate.csv"
    clean_file = pre_process(raw_file, bdate, edate, logger)

    # 3. Upload data to S3
    upload_data(ACCESS_KEY, SECRET_KEY, region, bucketName, clean_file, logger)

    # Program END
    logger.info('###### Data Ingestion & Wrangling Finished ######')
    print('###### Find logs in ddmmyyHHMMSS.log ######')


def save_logs():
    # Log File Setting
    time = datetime.datetime.now()
    logFileName = str(time.strftime('%d%m%y%H%M%S')) + '.log'
    logging.basicConfig(filename=logFileName,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger


if __name__ == '__main__':
    main()

