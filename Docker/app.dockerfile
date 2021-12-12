FROM python:3.8

# Metadata
LABEL name="Streamlit dashboard"
LABEL maintainer="PBG"
LABEL version="0.1"

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc curl

# System deps:
# RUN pip install "poetry==$POETRY_VERSION"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /streamlit
COPY dashboard ./dashboard
COPY poetry.lock .
COPY pyproject.toml .
COPY launch.sh .
COPY launch_dev.sh .

#update pip to avoid problems 
# RUN python3 -m pip instal --upgrade pip

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

#Streamlit configuration
ENV PYTHONPATH /streamlit
RUN mkdir -p /root/.streamlit

# Copy streamlit production configuration
COPY ./.streamlit/config.toml /root/.streamlit/config.toml

RUN chmod +x launch.sh
RUN chmod +x launch_dev.sh

# Launch etl and streamlit
ENTRYPOINT ["/bin/bash", "./launch.sh"]
