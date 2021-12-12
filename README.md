# PBG: Modern Data Engineering

This repository aim to investigate, experiment and understand the modern open source tools and approaches to data engineering with Python.

In this repository we have created a dashboard for Lombardia Italian Healthcare system to understand how the healthcare system is working.

This is just a test and sample experiment

## Tools

- Python
- Poetry
- Airflow
- Streamlit
- Jupyter (for exploration)
- Folium (for map visualization)

## Repository and code

This is a monorepo, so all the code is included here.  
Inside this repository you can find:
1. The airflow etl code with the dags
2. The streamlit application (inside the app folder)
3. The visual studio code dev container
4. Some notebooks and queries for explorative analysis

## Useful Documentation
- [PythonBiellaGroup website for poetry and other configurations](https://pythonbiellagroup.it)
- [Airflow official documentation](https://airflow.apache.org/docs/apache-airflow/stable/concepts/overview.html)
- [Airflow docker getting started](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Airflow production images and docker-compose](https://github.com/apache/airflow/issues/8605)
- [Airflow with Redis and Celery](https://medium.com/codex/how-to-scale-out-apache-airflow-2-0-with-redis-and-celery-3e668e003b5c)


## Useful commands

```bash
# launch the airflow infrastructure
docker-compose -f docker-compose.airflow.yml up --build -d

# launch the etl container that used airflow with the dags

# launch the streamlit application

# visualize the informations of docker container running and not
docker ps -a

# visualize the logs for a docker container
docker logs -t <container name>

# enter inside a docker container (for bin/bash)
docker exec -it <container name> /bin/bash

# inspect a container and get all the informations
docker inspect <container name>

# launch all the project with a make file


```