'''
Created on Aug 3, 2017

@author: guangnanliang
'''
from flask import Flask, request, render_template
#from StdSuites.AppleScript_Suite import result
import urllib
import json 
app = Flask(__name__)

@app.route("/")
@app.route("/prediction")
def classification():
    #return "Hello"
    return render_template("api.html")

@app.route("/respond", methods=["POST"])
def decisionforest1():
    Barometric_pressure = request.form["Barometric_pressure"]
    Black_carbon_PM25_STP = request.form["Black_carbon_PM25_STP"]
    Carbon_monoxide = request.form["Carbon_monoxide"]
    Nitric_oxide = request.form["Nitric_oxide"]
    Nitrogen_dioxide = request.form["Nitrogen_dioxide"]

    Outdoor_Temperature = request.form["Outdoor_Temperature"]
    Oxides_of_nitrogen = request.form["Oxides_of_nitrogen"]
    Ozone = request.form["Ozone"]
    PM10_LC = request.form["PM10_LC"]
    PM10_Total_STP = request.form["PM10_Total_STP"]

    PM1025_Local_Conditions = request.form["PM1025_Local_Conditions"]
    Reactive_oxides_of_nitrogen = request.form["Reactive_oxides_of_nitrogen"]
    Relative_Humidity = request.form["Relative_Humidity"]
    Solar_radiation = request.form["Solar_radiation"]
    Sulfate_STP = request.form["Sulfate_STP"]

    Sulfur_dioxide = request.form["Sulfur_dioxide"]
    Total_NMOC = request.form["Total_NMOC"]
    Wind_Direction_Resultant = request.form["Wind_Direction_Resultant"]
    Wind_Direction_Scalar = request.form["Wind_Direction_Scalar"]
    Wind_Speed_Resultant = request.form["Wind_Speed_Resultant"]
    Wind_Speed_Scalar = request.form["Wind_Speed_Scalar"]
    
    data =  {
                
                    "Inputs": {
                        "input1": {
                            "ColumnNames": ["Barometric pressure",
                            "Black carbon PM2.5 STP",
                            "Carbon monoxide",
                            "Nitric oxide (NO)",
                            "Nitrogen dioxide (NO2)",
                            "Outdoor Temperature",
                            "Oxides of nitrogen (NOx)",
                            "Ozone",
                            "PM10 - LC",
                            "PM10 Total 0-10um STP",
                            "PM10-2.5 - Local Conditions",
                            "Reactive oxides of nitrogen (NOy)",
                            "Relative Humidity",
                            "Solar radiation",
                            "Sulfate (TSP) STP",
                            "Sulfur dioxide",
                            "Total NMOC (non-methane organic compound)",
                            "Wind Direction - Resultant",
                            "Wind Direction - Scalar",
                            "Wind Speed - Resultant",
                            "Wind Speed - Scalar"],
                            "Values": [
                                [
                                  Barometric_pressure,
                                  Black_carbon_PM25_STP,
                                  Carbon_monoxide,
                                  Nitric_oxide,
                                  Nitrogen_dioxide,
                                  Outdoor_Temperature,
                                  Oxides_of_nitrogen,
                                  Ozone,
                                  PM10_LC,
                                  PM10_Total_STP,
                                  PM1025_Local_Conditions,
                                  Reactive_oxides_of_nitrogen,
                                  Relative_Humidity,
                                  Solar_radiation,
                                  Sulfate_STP,
                                  Sulfur_dioxide,
                                  Total_NMOC,
                                  Wind_Direction_Resultant,
                                  Wind_Direction_Scalar,
                                  Wind_Speed_Resultant,
                                  Wind_Speed_Scalar
                                ], 
                            ]
                        }, 
                    },
              "GlobalParameters": {}
            
    }
#     data =  {

#         "Inputs": {

#                 "input1":
#                 {
#                     "ColumnNames": ["Barometric pressure", "Black carbon PM2.5 STP", "Carbon monoxide", "Nitric oxide (NO)", "Nitrogen dioxide (NO2)", "Outdoor Temperature", "Oxides of nitrogen (NOx)", "Ozone", "PM10 - LC", "PM10 Total 0-10um STP", "PM10-2.5 - Local Conditions", "Reactive oxides of nitrogen (NOy)", "Relative Humidity", "Solar radiation", "Sulfate (TSP) STP", "Sulfur dioxide", "Total NMOC (non-methane organic compound)", "Wind Direction - Resultant", "Wind Direction - Scalar", "Wind Speed - Resultant", "Wind Speed - Scalar"],
#                     "Values": [ [ "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0" ], [ "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0" ], ]
#                 },        },
#             "GlobalParameters": {
# }
#     }


    
    body = str.encode(json.dumps(data))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/f4a5c63f0e6a40e2a8b4244226a5c91f/services/f71a5431f2d442ab993c9386b92907c4/execute?api-version=2.0&details=true'
    api_key = 'Lzwwc1u7brG9tJZlTNeCvphAa2Z10c7xpZKbo80nJ2uEpqPytFzdhzr2b5Bg6BXtVeaRkLmekCMj+JxyjdYhCA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    #return body
    req = urllib.request.Request(url, body, headers) 
    
    response = urllib.request.urlopen(req)
    result = response.read()
    encoding = response.info().get_content_charset('utf-8')
    JSON_object = json.loads(result.decode(encoding))
	
    return render_template('respond.html', Scored_Labels=JSON_object["Results"]["output1"]["value"]["Values"][0][21])

if __name__ == '__main__':
   app.run()