# Docker Hub
besimilar/advanced-data-analysis:aqi

# Steps in Data Ingestion
1. Fetch rawdata from EPA API ("src/fetchdata.py"):
	* set begin-date and end-date in env.list before starting your container

2. Clean rawdata and save both rawdata and cleandata to local ("src/wrangling.py")
	* for details, refer to "notebook/preprocess*.ipynb"

3. Upload cleandata to AWS S3 ("src/awsservice.py"):
	* set AWS params in env.list before starting your container

# Instruction
1. Set all parameters in env.list: 
	* This is a list of environment variables in container.
		* AWS params: 
			* AWSACCESS: aws access key
			* AWSSECRET: aws private key
			* REGION: aws region
		* EPA API params: 
			* EPAUSERNAME: EPA API username
			* EPAPASSWORD: EPA API password
			* BDATE: the first day of dataset (better within 3 years, try to set around 20140101, its a bug-free choice)
			* EDATE: the last day of dataset (default: current date)
		* Other default params:
			* change them in "/Final/1-Data-Ingestion-Wrangling/data-ingestion/config.json"
			* You dont't need to change them to do a demo

2. Start Container and set env:
	```
	$ docker run --env-file env.list -w /Final/1-Data-Ingestion-Wrangling/data-ingestion -it besimilar/advanced-data-analysis:aqi
	``` 
	
3. Run job:
	```
	$ ./run.sh
	```

# Data Ingestion & Wrangling Notes
1. Using environment: 
	* https://stackoverflow.com/questions/4906977/access-environment-variables-from-python
	```
	# check whether in env
	"HOME" in os.environ
	# provide default 
	os.environ.get('HOME','/home/username/')
	```

2. current date:
	```
	import datetime
	curr_date = datetime.datetime.now().strftime('%Y%m%d')

	```

3. env settings in :
	```
	export AWSACCESS=
	export AWSSECRET=
	export REGION=us-west-2
	export USERNAME=
	export PASSWORD=
	export BDATE=20130101
	export EDATE=20170816
	```

4. Error Handle:
	* Download from EPA:
		```
		try:
        	r = requests.get(url, params=req, stream=True)
		except requests.exceptions.HTTPError as err:
        	logger.error(err)
        	sys.exit(1)
		```
	* AWS:
		```
		try:
			# Any AWS connection
		except exceptions.EndpointConnectionError or exceptions.ClientError as e:
	        print("Warning: " + str(e))
	        logger.error(e)
	        return None
	    except Exception as e:
	        print("Warning: " + str(e))
	        logger.error(e)
	        return None
		```

5. Start Container and set env
	```
	docker run --env-file env.list -it besimilar/advanced-data-analysis:aqi
	```

6. Set working directory in Container
	```
	$ docker  run -w /path/to/dir/ -i -t <dockerimages> pwd
	```





