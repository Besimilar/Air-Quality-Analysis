# Docker Hub
besimilar/advanced-data-analysis:pipeline

# Instuction:
1. Set all parameters in env.list: 
	* This is a list of environment variables in container.
		* AWS params: 
			* AWSACCESS: aws access key
			* AWSSECRET: aws private key
			* REGION: aws region
		* EPA API params: 
			* EPAUSERNAME: EPA API username
			* EPAPASSWORD: EPA API password
			* BDATE: the first day of dataset (default: 20130101)
			* EDATE: the last day of dataset (default: current date)
		* Azure params:
			* ACCOUNTNAME: azure storage account name
			* ACCOUNTKEY: azure storage primary key
			* CONTAINERNAME: azure storage container name
		* Azure ML params:
			* APIKEY: predictive service key
			* APIURL: predictive service url
		* Other default params:
			* change them in "/Final/2-Pipeline/config.json"
			* You dont't need to change them to do a demo

2. Start Pipeline Job:
	```
	$ docker run --env-file env.list -w /Final/2-Pipeline/ -it besimilar/advanced-data-analysis:pipeline /bin/bash -c "sudo rabbitmq-server -detached; /bin/sleep 5; celery -A Pipeline worker -B -l info"
	```
3. View Results in Container:
	```
	$ docker start <containerID>
	$ docker exec -it <containerID> /bin/bash
	```

# Celery Pipelines Notes
1. Installation Celery
	```
	$ pip install -U Celery
	```
2. Install rabbitmq:
	```
	$ brew install rabbitmq
	# To have launchd start rabbitmq now and restart at login:
 	#  		brew services start rabbitmq
	# Or, if you don't want/need a background service you can just run:
 	#  		rabbitmq-server
 	# for ubuntu in docker
 	sudo apt-get install rabbitmq-server
	```

	* start the server:
	```
	$ sudo rabbitmq-server
	```
	* run it in the background:
	```
	$ sudo rabbitmq-server -detached
	```
	* stop the server:
	```
	$ sudo rabbitmq-server stop
	```
3. Start Worker:
	```
	$ celery -A proj worker -l info
	```
4. Start Scheduling:
	```
	# easy way
	$ celery -A proj worker -B -l info
	#
	$ celery -A proj beat -l info
	```

5. Before Start Pipelines: 
	```
	docker run --env-file env.list -w /Final/2-Pipeline/ -it besimilar/advanced-data-analysis:pipeline /bin/bash -c "sudo rabbitmq-server -detached; /bin/sleep 5; celery -A Pipeline worker -B -l info"  
	```

6. View Results in Container:
	```
	docker exec -it <containerID> /bin/bash
	```

7. Timeout: https://social.msdn.microsoft.com/Forums/sqlserver/en-US/cb4ee96d-c2ca-4c65-b02f-0ccb26181f7f/timeout-in-web-service?forum=MachineLearning

8. Set Timezone in Container:
	```
	sudo dpkg-reconfigure tzdata
	```
