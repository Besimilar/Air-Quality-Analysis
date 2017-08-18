# @author Hongwei
import pandas as pd
from pandas import read_csv
import numpy as np


def pre_process(raw_file, begin, end, logger):
    logger.info('Starting Cleansing Raw DataSet')
    print('###### Starting Cleansing Raw DataSet ######')
    clean_filename = "cleandata-" + begin + "-" + end + ".csv"

    # Clean Raw Data and Save to local
    clean_data = clean(raw_file)
    clean_data.to_csv(clean_filename, index=False)

    logger.info('DataSet Cleansing Completed')
    print('###### DataSet Cleansing Completed ######')
    return clean_filename


def clean(filename):
    data = read_csv(filename)
    data.columns = ["Latitude", "Longitude", "Datum", "Horizontal Accuracy", "State Code", "County Code", "Site Num",
                    "Parameter Code", "POC", "AQS Parameter Desc", "Date Local", "24 Hour Local", "Date GMT",
                    "24 Hour GMT", "Year GMT", "Day In Year GMT", "Sample Measurement", "Units of Measure",
                    "Sample Duration", "Sample Frequency", "Detection Limit", "Measurement Uncertainty",
                    "Qualifier Description", "Method Type", "Method Description"]

    # drop last row for END OF FILE
    data = data.drop(data.index[len(data)-1])

    # Drop unused columns
    data = data.drop("Parameter Code", axis=1)
    data = data.drop("POC", axis=1)
    data = data.drop("Detection Limit", axis=1)
    data = data.drop("Measurement Uncertainty", axis=1)
    data = data.drop("Horizontal Accuracy", axis=1)
    data = data.drop("Units of Measure", axis=1)
    data = data.drop("Sample Frequency", axis=1)
    data = data.drop("Qualifier Description", axis=1)
    data = data.drop("Method Type", axis=1)
    data = data.drop("Method Description", axis=1)

    dp = pd.pivot_table(data, index=data.index.values, columns=["AQS Parameter Desc"], values="Sample Measurement")

    dp.columns = list(dp.columns)
    frames = [data, dp]

    result = pd.concat(frames, axis=1)
    result["Date Local"] = pd.to_datetime(result["Date Local"])

    tmp = result.sort_values(by=["Latitude", "Date Local", "24 Hour Local"]).reset_index(drop=True)
    final = tmp.groupby(["Latitude", "Longitude", "Date Local", "24 Hour Local", "Sample Duration"], as_index=False).mean()

    pollutant = list(dp.columns)

    pd.options.mode.chained_assignment = None
    for i in pollutant:
        mask = np.isnan(final[i])
        final[i][mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), final[i][~mask])

    final = final.drop("Sample Measurement", axis=1)
    final = final.drop("PM2.5 - Local Conditions", axis=1)

    return final
