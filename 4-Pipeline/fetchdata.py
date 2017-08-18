# @author Hongwei
import requests


def fetch_data(username, password, data_format, pc, bdate, edate,
               state, county, logger):
    api_url = "https://aqs.epa.gov/api/rawData"
    req = {
        'user': username,
        'pw': password,
        'format': data_format,
        'pc': pc,
        'bdate': bdate,
        'edate': edate,
        'state': state,
        'county': county,
    }

    file = download_file(api_url, bdate, edate, req, logger)
    return file


def download_file(url, begin, end, req, logger):
    local_filename = "rawdata-" + begin + "-" + end + ".txt"

    logger.info('Fetch Data From EPA...')
    print('###### Fetch Data From EPA ######')
    # NOTE the stream=True parameter
    try:
        r = requests.get(url, params=req, stream=True)
        r.raise_for_status()

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        f.close()
        logger.info('Data From EPA Download Completed.')
        print('###### Data From EPA Download as ' + local_filename + ' ######')
        return local_filename
    except requests.exceptions.HTTPError as err:
        logger.error(r.headers['status'])
        print(err)
        logger.error(err)
        return None
