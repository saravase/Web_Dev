# Web_Dev


Module 2:

CD workflow:

1.Test
	Unit and Integration testing
		Source Code
		Test Suite
		Docker wrap Test Runner:
			java 	-	maven,gradle
			python	-	manage.py
		

2.Build
	Build application artifact
		-	python  wheels
		-	java JAR files

	Create deployable artifact

3.Release
	Create deployable release artifact in the form of Docker release image
		-	runtime environment
		-	install application artifact
	Create release environment using docker compose
		-	run acceptance testing 
	Tag and publish the Docker image
		-	only the acceptance is pass
		-	push to Docker Hub

4.Deploy
	Deploy the docker image in atlease one environment
		-	dev, QA or staging envieonment
		-	Ansible used to deplot the AWS
		-	AWS EC2 container mange rolling deployment of docker image



Installation Process:

	-	Install VMWare Fusion
	-	Install brew package manager
		-	installation commend get from brew home page
		-	check brew update command- brew update
	-	Install Docker
		-	brew install docker-compose
		-	brew install docker
		-	brew install docker-machine
	- 	Install Python
		-	brew install python
		-	pip install pip --upgrade
	-	Install ansible
		-	pip install ansible --upgrade 
		-	pip install boto boto3
		-	pip install awscli
	-	Install git
		- 	brew install git
		-	Install sublime text
	-	Create docker virtual machine
		-	docker-machine create --driver virtualbox modifyvm--cpus 4 --memory 20000 --vram 8000 --name dockervm01
		-	docker-machine env dockervm01
		-	eval "$(docker-machine env dockervm01)"
		-	docker pull ubundu
		-	docker images
		-	docker-machine ip dockervm01
		-	docker-machine ssh dockervm01
		-	docker-machine restart dockervm01
		-	docker-machine ls


Module 3:

	-	create simple django application
		-	pip install virtualenv
		-	virtualenv envname
		-	env\scripts\activate
		-	pip install pip --upgrade
		-	pip install django==version
		-	pip install djangorestframework
		-	pip install django-cors-headers
		-	django-admin startproject TodoApp
		-	create src folder in TodoApp. then , move manage.py file to src folder. 
	-	Unit and Integration Testing
		-	create tests file todo app and write testcases
		-	run command : python manage.py test
		-	create settings folder and create base,test file with in the folder
		-	run command : python manage.py test --settings=TodoApp.settings.test
		-	Improving test output 
		- 	install command : pip install django-nose
		-	pip install pinocchio
		-	pip install coverage
		-	run command : python manage.py test --settings=TodoApp.settings.test
	-	Acceptance Test
		-	create TodoApp-Spec folder
		-	install node.js
		-	commnad : npm init
		-	command : npm install bluebird chai chai-as-promised mocha superagent superagent-promise    mocha-jenkins-reporter --save
		- 	save flag add packages with dependencies
		- 	mocha and chai used create and run the test  
		- 	superagent used to communicate with HTTP client
		- 	bluebrid support promises used to control asy process
		- 	jenkins-reporter provide junit.xml report
	- 	Crate TodoClient
		-	clone TodoClient
		-	run commnad : npm install
		-	run commnad : npm install -g grunt-cli
		- 	run commnad : node app.js

MODULE 4:
	-  	Continuous Delivery Workflow
		-	Test Workflow using docker
			-	Create Test Environement
				-	Base Image
				-	Development Image
				-	Docker Compose
			-	Run unit Test
				-	Single Container
			-	Run Itegration Test
				-	Single/ Multi container Complex workflow
		-	Basic of Base Image
			-	minimum runtime environment
			-	application defendencies
			-	system configuration
			-	default setting
		-	Basic of Release Image
			-	install application
			-	application configuration
			-	application entrypoint
		-	Basic of development Image
			-	install Dev defendencies
			-	install buid / test tool
	-	Create base image
		-	folder structure - TodoApp-Base

		-	Docker Operation ------- Base docker image ----- Docker Repository
		                      commit                    push           
            																    = CI + CD
		-	Developer  --------  sourcecode -------    git repository  
		                commit               push                     

		-   create folder TodoApp-Base. 
		-	create Docker file using command - touch Dockerfile 
		-	create entrypoint

		Base Image:

			
			# parent image ubundu,release code name trusty 
			FROM ubundu:trusty
			MAINTAINER Saravanakumar Selvam  <saravanakumar323py@gmail.com>

			# prevent package error
			ENV TERM=xterm-256color
			
			# Set mirrors to NZ
			# sed is a editor, s/Regexp/Replacement store location
			RUN sed -i "s/http:\/\/archive./http:\/\/nz.archive./g" /etc/apt/sources.list

			# Install python runtime
			# Update the linux package database
			RUN apt-get update &&\
				apt-get install -y\
				-o APT::Install-Recommend=false -o APT::Install-Suggests=false \
				pyhon python-virtualenv

			# Create virtual environment
			# Upgrade PIP in virtual environment to latest version
			RUN virtualenv /appenv && \
				./appenv/bin/activate && \
				pip install pip --upgrade

		- Create entrypoint.sh
			# activate the virtual environment
			. /appenv/bin/activate
			exec $@
		- Run build command - docker build -t saravase/TodoApp-Base .
		- Display list of images - docker images
		- Run entrypoint - docker run -rm saravase/TodoApp ps
			# -rm - cleanup container
			# ps show current container

	- 	Create development image
		-	Folder structure
			TodoApp - docker - dev - create Docker file
		-	Development Image
			FROM saravase/TodoApp-Base:latest
			MAINTAINER Saravanakumar Selvam <saravanakumar323py@gmail.com>

			# Install dev/build dependancies
			RUN apt-get update && \
				apt-get install -qy python-dev libmysqlclient-dev

			#Activate VE and install wheel
			RUN ./appenv/bin/activate && \
				pip install wheel --upgrade

			# PIP environment variavbles
			ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache

			# OUTPUT: Build artifacts(wheel) are output here
			VOLUME /wheelhouse

			# OUTPUT: Test reports
			VOLUME /reports

			#Add test entrypoint script
			COPY scripts/test.sh /usr/local/bin/test.sh
			RUN chmod +x /usr/local/bin/test.sh

			# Set defaults for entrypoint and command string
			ENTRYPOINT ["test.sh"]
			CMD ["python", "manage.py", "test", "--noinput"]

			# Add applicaton source
			COPY src / application
			WORKDIR /application

		- 	Create folder TodoApp - scripts - test.sh
		-	test.sh
			# Activate VE
			. /appenv/bin/activate

			# Install application test requirements
			pip install -r requirements_test.txt

			# Run test.sh arguements
			exec $@
	- 	Create application requirements
		-	Create folder structure - TodoApp - src - requirements.txt
		-	requirements.txt
			Django==2.2
			django-cors-headers==2.5.2
			djnagorestframework==3.9.2
			mysqlclient==1.4.2.post1

		-	requirements_test.txt
			-r requirements.txt
			colorama==0.4.1
			coverage==4.5.3
			django-nose==1.4.6
			nose==1.3.7
			pinocchio==0.4.2
		- 	activate the virtual environment
		- 	move to src folder. run command - pip freeze > requirements.txt
		- 	run command - docker build -t TodoApp-Dev -f docker/dev/Dockerfile .
		-	run command - touch .dockerignore
		- 	run command - docker run --rm TodoApp-Dev
		- 	run command - time docker run --rm TodoApp-Dev
		-	reducing testing time
		-	run command - docker run -v /tmp/cache:/cache --entrypoint true --name 	cache TodoApp-Dev 
		-	run command - docker ps -a
		-	run command - time docker run --rm --volumes-from cache TodoApp-Dev
		-	Run settings.test
		-	run command - docker run --rm -e 			                             DJANGO_SETTINGS_MODULE=TodoApp.settings.test --volume-from cache TodoApp-Dev
	- Create multiple container environment using Docker Compose
		-	create docker-compose.yml
		-	Folder strcuture - TodoApp - docker - dev - docker-compose.yml
		-	docker-compose.yml
			# Test Service
			test:
				build:../../
				dockerfile: docker/dev/Dockerfile
				volumes_from:
					- cache

				# Link DB service with Test service
				links:
					- db
				environment:
					DJANGO_SETTINGS_MODULE: TodoApp.settings.test
					MYSQL_HOST: db
					MYSQL_USER: root
					MYSQL_PASSWORD: 
					TEST_OUTPUT_DIR: /reports

			# DB Service
			db:
				image: mysql:5.6
				hostname: db
				expose:
					- "3306"
				environment:
				MYSQL_ROOT_PASSWORD: 

			# Cache Service
			cache:
				build: ../../
				dockerfile: docker/dev/Dockerfile
				volumes:
					- /tmp/cache:
				entrypoint: "true"
		-	move to docker/dev path
		-	run command: docker compose up test
		-	run command: docker-compose ps
		-	run command: docker-compose logs db
		-	run command: docker compose up test
	- 	Multi container Race Conditions
		- if test initialization over than db initialization time - test not run
		- 	run command: docker-compose kill
		-	run command: docker-compose rm -f
	- 	Handling Race Conditions
		-	folder structure - TodoApp-Ansible
		-	create Docker file
			FROM ubundu:trusty
			MAINTAINER Saravanakumar Selvam <saravanakumar323py@gmail.com>

			# Prevent package error
			ENV TERM=xterm-256-color

			# SEt mirrors to NZ
			RUN sed -i "s/http:\/\/archive./http:\/\/nz.archive./g" /etc/apt/sources.list

			# Install Ansible
			RUN apt-get update -qy && \
				apt-get install -qy software-properties-common && \
				apt-get-repository -y ppa:ansible/ansible && \
				apt-get update -qy && \
				apt-get install -qy ansible

			# Add volume for Ansible laybook
			VOLUME /ansible
			WORKDIR /ansible

			# Entrypoint
			ENTRYPOINT["ansibleplaybook"]
			CMD["site.yml"]
		- 	run command: docker build -t saravase/ansible .
		-	create Ansible  playbook
			- folder structure - TodoApp/ansible/ probe.yml
		- 	probe.yml
			---
			- name: Probe Host
			  hosts: localhost
			  connection: local
			  gather_facts: no
			  tasks:
			  - name: Set facts
			    set_fact:
			      probe_host: "{{ lookup('env','PROBE_HOST') }}"
			      probe_port: "{{ lookup('env','PROBE_PORT') }}"
			      probe_delay: "{{ lookup('env', 'PROBE_DELAY') | default(0, true) }}"
			      probe_timeout: "{{ lookup('env', 'PROBE_TIMEOUT') | default(180, true) }}"
			  - name: Message
			    debug:
			      msg: >
                    Probing {{ probe_host }}:{{ probe_port }} with delay={{ probedelay}}s and timeout={{ probe_timeout }}s
              - name: Waiting for host to respond...
                local_action: >
                  wait_for host={{ probe_host }} 
                  port= {{ probe_post }}
                  delay= {{ probe_delay }}
                  timeout= {{ probe_timeout }}
        - 	Rewrite docker-compose.yml
        -	docker-compose.yml

        	after test service

        	# Agent Service
        	agent:
        		images: saravase/ansible
        		volumes:
        			- ../../ansible/probe.yml:/ansible/site.yml
        		links:
        			- db
        		environment:
        			PROBE_HOST: "db"
        			PROBE_PORT: "3306"
        - 	run command: docker-compose kill
        -	run command: docker-compose rm -f
        - 	run command: docker-compose up agent
        -	run command: docker-compose up test
        
MODULE : 5
	- 	Building Docker artifacts
		-	Build Workflow using docker
			-	Create Build environment
				-	Reuse Test envionment
				-	Create Builder Service
			-	Build Artifacts
				-	Compile Source
				-	Build Python wheel
			-	Publish Artifacts
				-	publish locally
				-	release stage inputs
	-	Application Artifact Types
		-	Source Distribution
			-	build process
				-	source   - package
			-	deploy process
				-	package to source - compile and build  [ add external dependancies] - app binary
		-	Build Distribution
			-	build process
				-	source - compile and build  [ add external dependancies] - app binary - package
			- 	deploy process
				-	package to app binary
		-	Compare to both artifacts type Build distribution contains less risk
	-	Demo Build application artifacts
		-	add packgae metadata
			-	create folder structure TodoApp/src/ setup.py
			-	setup.py

				from setuptools import setup, find_packages
				setup(
					name 				= "TodoApp",
					version 			= "0.1.0",
					description 		= "TodoApp Django REST services"
					include_package_data= True,
					scripts				= ["manage.py"]
					install_requires	= [
						"Django>=2.2, <2.3",
						"django-cors-headers>=2.5.2",
						"djnagorestframework>=3.9.2"
						"mysqlclient>=1.4.2.post1"
					]
					# In requiremnts.txt , remove all the dependencies name, only put [.] . it means pip install
					extras_require 			= {
						"test" : [
							"colorama>=0.4.1",
							"coverage>=4.5.3",
							"django-nose>=1.4.6",
							"nose>=1.3.7",
							"pinocchio>=0.4.2"
						]
					}

					# In requirements_test.txt file, remove all the dependancies,put -e .[test] , it means pip to additionally install "test" array dependacies in the extra require setting of setup.py
				)
		-	Build Cache
			-	why do we go build case?
				-	some situation, test stage - app dependancy 3.3.1. Run test
				-	build stage - app dependancy 3.3.2 
				-	this situation, dependancy inconsistency occur.
		-	Adding builder service
			-	Create build cache
				-	test.sh
					# Download requirements to build cache
					pip download -d/build -r requirements_test.txt --no-input

					# Install application test requireemnts
					pip install --no-index -f/build -r requirements_test.txt
				-	docker/dev/Dockerfile
					# OUPUT: build cache
					VOLUME /build
				-	docker-compose.yml
					...
					# Builder service
					builder:
						build: ../../
						dockerfile: docker/dev/Dockerfile
						volumes:
							- ../../target:/wheelhouse
						volumes_from:
							- cache
					cache:
						volumes:
							...
							-	/build
						entrypoint: "entrypoint.sh"
						command: ["pip", "wheel", "--no-index", "-f/build", "."]
		-	Building and publishing python wheels
			-	run command:	cd docker/dev
			-	run commnad:	docker-compose kill
			-	run commnad:	docker-compose rm -f
			-	run command:	docker-compose up agent
			-	run command:	docker-compose up test
			-	development image not rebuild. we rectify this issue
			-	run commnad:	docker-compose kill
			-	run commnad:	docker-compose rm -f
			-	run command:	docker-compose build
			-	run command:	docker-compose up agent
			-	run command:	docker-compose up test
			- 	build our application artifacts
			-	run command:	docker-compose up builder
			-	see in the root folder target folder is created. this is contain dependencies wheel file
			-	builder service process:
					-	copy the source code from src folder to application folder
					-	entrypoint.sh , execute pip wheel dot command
					-	then, it will take dependencies from build bolder, compile and build the pyhton wheel
					-	finally create dependecies whl file, this will stored in a wheelhouse , then mapped to target
MODULE:6
	-	Creating releases using docker
		- Release workflow using docker
			-	Create Release environment
				-	Create release settings
				-	Create Release image
			-	Bootstrap Release Environment
				-	Prepare environment
				-	Start application
			-	Acceptance Testing
				-	Run acceptance testing
				-	Publish release image
		-	ngnix	-	front end webserver
			-	contain authentication middleware
			-	manage static content
		-	uwsgi	-	server container
		-	wsgi	-	wsgi application interface
			-	ngnix and uwsgi communicatw with uwsgi protocol
			-	communication between socket either file or netwok base
			-	convert incoming request received from web server  and call our  application using web server gateway interface
			-	django contain wsgi application interface	
		-	Workflow
			-	ngnix forward all non static request
			-	uwsgi application container convert http request into binary converted uwsgi protocol request
			-	receive request and call uwsgi entrypoint for the application
			-	application contain two arguments:
			-	environment argument - http request dictionary
			-	start response callback	- set the http status code
			-	response contain [status, headers], response body
			-	uwsgi application container return response binary uwsgi protocol format to ngnix . ngnix translate http response
	-	Create release environment
		-	create release settings
			-	create folder structure src/TodoApp/settings/release.py
			-	release.py
			-	edit setup.py
				install_requires =[
					...
					"uwsgi>=2.0"
		-	run commnad:	docker-compose kill
			-	run commnad:	docker-compose rm -f
			-	run command:	docker-compose build
			-	run command:	docker-compose up agent
			-	run command:	docker-compose up test
			- 	build our application artifacts
			-	run command:	docker-compose up builder
	-	Creating the release image
		-	Create folder structure TodoApp/docker/release/Dockerfile
		-	Dockerfile
			FROM saravse/TodoApp-Base:latest

			MAINTAINER Saravanakumar Selvam<saravanakumar323py@gmail.com>

			# Copy application artifacts
			COPY target /wheelhouse

			# Install application
			RUN ./appenv/bin/activate &&\
				pip install -no-index -f /wheelhouse TodoApp &&\
				rm -rf /wheelhouse
	-	Discribing Release environment
		-	Release environment design
			-	ngnix service  - webroot - appservice - db service - agent service
			- finally run test service
			-	create folder structure TodoApp/docker/release/docker-compose.yml
			-	docker-compose.yml

				# Application Service
				app:
					build: ../..
					dockerfile: docker/release/Dockerfile
					links:
						-	db
					volumes_from:
						-	webroot
					environment:
						DJANGO_SETTINGS_MODULE : TodoApp.settings.release
						MYSQL_HOST: db
						MYSQL_USER: root
						MYSQL_PASSWORD: 
					command:
						- 	uwsgi
						- 	"--socket /var/www/TodoApp/todoApp.sock"
						# it is used to read and write
						- 	"--chmod-socket=666"
						-	"--module todoApp.wsgi"
						-	"--master"
						-	"--die-on-term"
				# Ngnix Service
					image: ngnix
					volumes:
						-	./todoApp.conf:etc/ngnix/conf .d/tooApp.conf
					ports:
						-	"8000:8000"

				# Webroot Service
				webroot:
					build: ../../
					dockerfile: docker/release/Dockerfile
					volumes:
						-	/var/www/TodoApp
					entrypoint: "true"

				# Database Service
				db:
					image: mysql:5.6
					expose:
						-	"3306"
					environment:
						MYSQL_DATABASE: todoapp
						MYSQL_USER: root
						MYSQL_PASSWORD:
						MYSQL_ROOT_PASSWORD:

				# Agent Service
				agent: 
					image: saravase/ansible
					volumes:
						-	../../ansible/probe.yml:/ansible/site.yml
					links:
						-	db
					environment:
						PROBE_HOST: "db"
						PROBE_PORT: "3306"
			- 	create folder structure docker/release/todoApp.conf
            -	todoApp.conf
            	# the upstream uWSGI application server
            	upstream appserver{
            		server unix:///var/www/TodoApp/todoApp.sock;
            	}

            	# Configuration of the server
            	server{
            		listen 8000;

            		location /static{
            			alias /var/www/TodoApp/static;
            		}

            		location /media{
            			alias /var/www/TodoApp/media;
            		}

            		# Send all other requests to the uWSGI application server using uwsgi wire protocol
            		location /{
            			uwsgi_pass appserver;
            			include /etc/ngnix/uwsgi_params;
            		}
            	}
        -	Testing release  image
        	-	Release environment issues
        		-	runtime environment
        			-	missing requiremnts from base image
        			-	encoutered upon intial setup
        			-	application container fail to start
        			-	release environment misconfiguration
        		-	Bootstrap tasks
        			-	establish initial state
        			-	required for each release stage iteration
        			-	typically present as errors to user
        				-	setup database schema and data
        -	move to docker/release path
        -	run command: docker-compose build
        -	run command: docker-compose up agent
        -	run command: docker-compose up app
        -	it will through on error. 
        -	modify baseimage
        	...
        	python python-virtualenv python2.7
        -	move to base imgae path
        -	run command: docker build -t saravase/TodoApp-Base
        -	move to docker/release path
        -	run command: docker-compose kill
        -	run command: docker-compose rm -f 
        -	run command: docker-compose build
        -	run command: docker-compose agent
        -	run command: docker-compose app
        -	it will through on error. 
        -	modify baseimage
        	...
        	python python-virtualenv libpython2.7 python-mysqldb
        -	move to base imgae path
        -	run command: docker build -t saravase/TodoApp-Base
        -	move to docker/release path
        -	run command: docker-compose kill
        -	run command: docker-compose rm -f 
        -	run command: docker-compose build
        -	run command: docker-compose agent
        -	run command: docker-compose app

    -	Bootstraping the application
    	-	initilization task
    		-	modify - docker/release/docker-compose.yml
    			modify ngnix service
    			...
    			links:
    				-	app
    		-	run command: docker-compose up ngnix
    		-	it will through sttaic error
    		-	modify base.py file
    			-	STATIC_URL = '/static/'

    		-	run command: docker-compose run -rm app manage.py collecstatic --noinput
    		-	run commnad: docker-compose run -rm app manage.py migrate
    		- 	run command: docker-compose up ngnix
    	- 	Create Acceptnce test service
    		-	create folder structure TodoApp-Specs/Dockerfile
    		-	Dockerfile
    			FROM ubuntu:trusty
    			MAINTAINER Saravanakumar Selvam <saravanakumar323py@gmail.com>

    			# Prevent package errors
    			ENV_TERM=xterm-256color

    			#Set mirrors to NZ
    			RUN sed -i "s/http:\/\/archieve./http:\/\/nz.archive./g" /etc/apt/sources.list

    			#Install node.js
    			RUN apt-get update &&\
    				apt-get install curl-y &&\
    				curl -sL https://deb.nodsource.com/setup_4.x | sudo -E bash -&&\
    				apt-get install -y nodejs

    			COPY ./app
    			WORKDIR /app

    			# Install application dependancies
    			RUN npm install -g mocha &&\
    				npm install

    			ENTRYPOINT['mocha']

    		-	run command: docker build -t saravase/TodoApp-Specs.
    		- 	move to docker/release/docker-compose.yml
    			-	modify compose.yml
    				# Test Service
    				test:
    					image: saravase/TodoApp-Specs
    					links:
    						-	ngnix
    					environment:
    						URL: http://ngnix:8000/todos
    						JUNIT_REPORT_PATH: /reports/acceptance.xml
    						JUNIT_REPORT_STACK: 1
    					command: --reporter mocha-jenkins-reporter
    		-	move to docker/release path
        	-	run command: docker-compose kill
        	-	run command: docker-compose rm -f 
        	-	run command: docker-compose build
        	-	run command: docker-compose up agent
        	-	run command: docker-compose run --rm app manage.py collectstatic --noinput
        	-	run command: docker-compose run --rm app manage.py migrate --noinput
        	-	run command: docker-compose up test
        	-	run commnad: docker tag release_app saravase/TodoApp:0.01
MODULE : 7
    -	CD workflow
    	-	GNU Make
    		-	three reason
    			-	make designed for the shell
    			-	syntex is simple and more powerful
    			-	maitainability and usability (popular)
    	-	Creating make file
    		-	folder sructure TodoApp/Makefile
    		-	Makefile
    			# Project variables
    			PROJECT_NAME ?= TodoApp
    			ORG_NAME ?= saravase
    			REPO_NAME ?= TodoApp

    			#Filename
    			DEV_COMPOSE_FILE := docker/dev/docker-compose.yml
    			REL_COMPOSE_FILE := docker/release/docker-compose.yml

    			#Docker compose project name
    			REL_PROJECT := $(PROJECT_NAME)$(BUILD_ID)
    			DEV_PROJECT := $(REL_PROJECT)dev

    			.PHONY : test build release clean

    			test:
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) build
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up agent
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up test

    			build:
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) up builder

    			release:
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) build
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up agent
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py collectstatic --noinput
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) run --rm app manage.py migrate --noinput
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) up test

    			clean:
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) kill
    				docker-compose -p $(DEV_PROJECT) -f $(DEV_COMPOSE_FILE) rm -f
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) kill
    				docker-compose -p $(REL_PROJECT) -f $(REL_COMPOSE_FILE) rm -f
    		-	run command : make test	
    		-	run command : make build
    		-	run command : make release
    		-	run command : make clean
    	-	Creating GitHub repositories
    		-	create repository TodoApp
    			-	run command: git status
    			-	run command: git log
    			-	run command: git remote add origin url:saravase/TodoApp.git
    			-	run command: git push -u origin master
    	-	Creating DockerHub repositories
    		-	login docker hub
    		-	click create
    		-	create repository
    		-	enter repository name, short description, full description, visibility
    		-	click create
    		-	move to TodoApp-Client path
    		-	run command: docker build -t saravase/TodoApp-Client.
    		-	run command: docker push saravase/TodoApp-Client
    		-	run command: docker login
    			-	Enter Username
    			-	Enter Password
    			-	Enter Email
    		-	run command: docker push saravase/TodoApp-Client
    	- Create automated build repositories
    		-	normal repositories
    			-	TodoApp-Client
    			-	TodoApp
    		-	automated build repositories
    			-	TodoApp-Base
    			-	TodoApp-Specs
    			-	TodoApp-Ansible
    			






























































































