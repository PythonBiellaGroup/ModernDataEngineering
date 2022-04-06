# PBG: Modern Data Engineering

This repository aim to investigate, experiment and understand the modern open source tools and approaches to data engineering with Python.

In this repository we have created a dashboard for Lombardia Italian Healthcare system to understand how the healthcare system is working.

This is just a test and sample experiment

## What we talk

1. how to define the cluster
2. how to create a simple dag
3. tasks and operators
4. dummy operators and file sensors
5. scheduling
6. xcom transfer
7. plugins

## Status
- Create DAGS for data import on different sources
- Create DAGS for data manipulation
- Ingest new data into db
- Create visualization and analysis on streamlit dashboard

Completed
- streamlit template
- airflow cluster
- project setup

## Tools

- Python
- Poetry
- Airflow
- Streamlit
- Jupyter (for exploration)
- Folium (for map visualization)
- Pydantic
- Sqlalchemy (pyodbc)

## Repository and code

This is a monorepo, so all the code is included here.  
Inside this repository you can find:
1. The airflow etl code with the dags
2. The streamlit application (inside the app folder)
3. The visual studio code dev container
4. Some notebooks and queries for explorative analysis


## Useful commands

```bash
# launch the airflow infrastructure
docker-compose -f docker-compose.airflow.yml up --build -d

# launch the etl container that used airflow with the dags

# launch the streamlit application

# stop or remove all the docker containers for a specific dockerfile configuration
docker-compose -f docker-compose.airflow.yml stop  #if you want to stop them
docker-compose -f docker-compose.airflow.yml rm #if you want to remove them

# visualize the informations of docker container running and not
docker ps -a

# visualize the logs for a docker container
docker logs -t <container name>

# enter inside a docker container (for bin/bash)
docker exec -it <container name> /bin/bash

# inspect a container and get all the informations
docker inspect <container name>

# stop containers and delete volumes
docker-compose -f docker-compose.airflow.yml down --volumes --rmi all

# launch all the project with a make file

```

If you want to forward the port from the server to your machine (because everything here is not exposed on internet on PBG server) you can do:
```bash
ssh -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER

#example (pbg server is defined into ssh config file)
ssh -LN 8042:localhost:8080 pbg

```
You can add your machine configuration inside the ssh config file for your user: `~/.ssh/config`


## Considerations,  errors and problems

Collection of comments, info and problems that we found during the development and how to fix them

**pyodbc**

To use **pyodbc** on linux you have to install the following dependencies:
`sudo apt install unixodbc-dev`

We suggest also on linux and docker to install those packages:
```
sudo apt install vim libpq-dev gcc curl openssh-client git unixodbc-dev libxml2-dev libxslt1-dev zlib1g-dev g++
```

**psycopg library**

To use the system with psycopg2 for the postgres database connection it's important to install in your system (linux-based) the requirements: `sudo apt-get install libpq-dev`

To launch the project from terminal if you are on the project root you have to do: `PYTHONPATH="./" python ./test/<name of the script>.py`

Be carefull not to install virtualenv via `apt` on linux, but use virtualenv by `pip`.

## Useful Documentation
- [PythonBiellaGroup website for poetry and other configurations](https://pythonbiellagroup.it)
- [Airflow official documentation](https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html)
- [Airflow docker getting started](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow official docker-compose version](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml)
- [Airflow production images and docker-compose](https://github.com/apache/airflow/issues/8605)
- [Airflow custom docker image](https://airflow.apache.org/docs/docker-stack/build.html)
- [Running airflow in docker](https://airflow.apache.org/docs/apache-airflow/2.1.3/start/docker.html)
- [Airflow Production Deployment](https://airflow.apache.org/docs/apache-airflow/1.10.14/production-deployment.html)
- [Airflow with Redis and Celery](https://medium.com/codex/how-to-scale-out-apache-airflow-2-0-with-redis-and-celery-3e668e003b5c)
- [Pydantic settings management](https://pydantic-docs.helpmanual.io/usage/settings/)

If you want to **monitor and control** the ETL you have to connect to the web interface.
- If you run this on a server don't forget to forward the port via ssh (see Useful commands section behind)
- Monitor executions of DAGs, available at: http://**ip**:8080/
- Monitor celery execution: http://**ip**:5555

Default credentials for Airflow web interface:
- user: Airflow
- password: airflow

