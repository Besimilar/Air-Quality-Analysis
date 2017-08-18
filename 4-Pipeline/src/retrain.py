# @author Hongwei
import urllib.request
import json
import time


def printHttpError(httpError):
    print("The request failed with status code: " + str(httpError.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(httpError.info())

    print(json.loads(httpError.read().decode("utf8", 'ignore')))
    return


def saveBlobToFile(output_filename, blobUrl, resultsLabel):
    output_file = output_filename # Replace this with the location you would like to use for your output file, and valid file extension (usually .csv for scoring results, or .ilearner for trained models)
    print("Reading the result from " + blobUrl)
    try:
        response = urllib.request.urlopen(blobUrl)
    except urllib.error.HTTPError as error:
        printHttpError(error)
        return

    with open(output_file, "w+") as f:
        f.write(response.read().decode("utf8", 'ignore'))
    print(resultsLabel + " have been written to the file " + output_file)
    return


def processResults(result, output_filename):
    first = True
    results = result["Results"]
    for outputName in results:
        result_blob_location = results[outputName]
        sas_token = result_blob_location["SasBlobToken"]
        base_url = result_blob_location["BaseLocation"]
        relative_url = result_blob_location["RelativeLocation"]

        print("The results for " + outputName + " are available at the following Azure Storage location:")
        print("BaseLocation: " + base_url)
        print("RelativeLocation: " + relative_url)
        print("SasBlobToken: " + sas_token)

        if (first):
            first = False
            url3 = base_url + relative_url + sas_token
            saveBlobToFile(output_filename, url3, "The results for " + outputName)
    return


def invokeBatchExecutionService(output_filename, account_name, account_key, container_name, api_key, api_url, clean_data):
    storage_account_name = account_name  # Replace this with your Azure Storage Account name
    storage_account_key = account_key  # Replace this with your Azure Storage Key
    storage_container_name = container_name  # Replace this with your Azure Storage Container name
    connection_string = "DefaultEndpointsProtocol=https;AccountName=" + storage_account_name + ";AccountKey=" + storage_account_key

    # api_key = "api_key" # Replace this with the API key for the web service
    url = api_url

    payload = {

            "Outputs": {
                    "output2":
                    {
                        "ConnectionString": connection_string,
                        "RelativeLocation": "/" + storage_container_name + "/" + output_filename  # Replace this with the location you would like to use for your output file, and valid file extension (usually .csv for scoring results, or .ilearner for trained models)
                    },
            },

        "GlobalParameters": {
            "Data source URL": clean_data,
        }
    }

    body = str.encode(json.dumps(payload))
    headers = { "Content-Type":"application/json", "Authorization":("Bearer " + api_key)}
    print("Submitting the job...")

    # submit the job
    req = urllib.request.Request(url + "?api-version=2.0", body, headers)

    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as error:
        printHttpError(error)
        return

    result = response.read()
    job_id = result.decode("utf8", 'ignore')[1:-1]
    print("Job ID: " + job_id)

    # start the job
    print("Starting the job...")
    body = str.encode(json.dumps({}))
    req = urllib.request.Request(url + "/" + job_id + "/start?api-version=2.0", body, headers)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as error:
        printHttpError(error)
        return

    url2 = url + "/" + job_id + "?api-version=2.0"

    consumed_time = 0
    while True:
        print("Checking the job status...")
        req = urllib.request.Request(url2, headers = { "Authorization":("Bearer " + api_key) })

        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as error:
            printHttpError(error)
            return

        result = json.loads(response.read().decode("utf8", 'ignore'))
        status = result["StatusCode"]
        if (status == 0 or status == "NotStarted"):
            print("Job " + job_id + " not yet started...")
        elif (status == 1 or status == "Running"):
            print("Job " + job_id + " running...")
        elif (status == 2 or status == "Failed"):
            print("Job " + job_id + " failed!")
            print("Error details: " + result["Details"])
            break
        elif (status == 3 or status == "Cancelled"):
            print("Job " + job_id + " cancelled!")
            break
        elif (status == 4 or status == "Finished"):
            print("Job " + job_id + " finished!")
            processResults(result, output_filename)
            break
        time.sleep(60)  # wait one second
        consumed_time = consumed_time + 1;
        print("The Job has been running for " + str(consumed_time) + "min... You need to wait for almost 20min")
    return


