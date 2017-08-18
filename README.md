# Advanced Data Science & Architecture
INFO 7390

## Team 3
Hongwei Hu:

* Data Fetching & Upload Automation
* Azure Machine Learning Model Building & Publishing
* Pipelines for Regular Fetching & Retraining
* Deployment: Docker, Flask API

Guangnan Liang:

* Data Wrangling
* Geospatial Analysis
* EDA
* FLASK REST API

## Deployment
1. Data Ingestion & Wrangling
	* Docker Hub: besimilar/advanced-data-analysis:aqi

2. EDA 
	* Docker Hub: besimilar/advanced-data-analysis:aqi

3. Pipelines
	* Docker Hub: besimilar/advanced-data-analysis:pipeline

4. Model
	* Azure Gallery: https://gallery.cortanaintelligence.com/Experiment/Boosted-Decision-Tree

5. FLASK API
	* Pythonanywhere: http://besimilar.pythonanywhere.com/

## Instruction
1. **Import Step Before starting your container**
	* prepare a env.list file for env variables in container
	* refer to "env.list"
		* AWS params: 
			* AWSACCESS: aws access key
			* AWSSECRET: aws private key
			* REGION: aws region
		* EPA API params: 
			* EPAUSERNAME: EPA API username
			* EPAPASSWORD: EPA API password
			* BDATE: the first day of dataset (better within 3 years, try to set around 20140101, its a bug-free choice)
				* You might get error, if you fetch large data from api, because they seem to limit my account, refer to "Notes/1-Bug-EPA"
				* You also might get error, if you fetch small data, because the data might not contain some predictive features, either wrangling or model retraining could produce "no features" errors.
			* EDATE: the last day of dataset: (default: current date)
		* Azure params:
			* ACCOUNTNAME: azure storage account name
			* ACCOUNTKEY: azure storage primary key
			* CONTAINERNAME: azure storage container name
		* Azure ML params:
			* APIKEY: predictive service key
			* APIURL: predictive service url
		* Other default params:
			* change them in "config.json" in container
			* You dont't need to change them to do a demo

2. For individual parts, refer to instruction in their folder to run.
	1. Data-Ingestion: 
		* Start container
			```
			$ docker run --env-file env.list -w /Final/1-Data-Ingestion-Wrangling/data-ingestion -it besimilar/advanced-data-analysis:aqi

			```
		* Run job in container
			```
			# in container
			$ ./run.sh
			```
	2. Pipeline:
		* Start scheduler:
			```
			$ docker run --env-file env.list -w /Final/2-Pipeline/ -it besimilar/advanced-data-analysis:pipeline /bin/bash -c "sudo rabbitmq-server -detached; /bin/sleep 5; celery -A Pipeline worker -B -l info"
			```
		* View Results in Container:
			```
			$ docker start <containerID>
			$ docker exec -it <containerID> /bin/bash
			```

## Proposal
Video: https://www.screencast.com/t/wZBxXC7Y

