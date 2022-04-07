FROM apache/airflow:2.2.4-python3.8

# Metadata
LABEL name="Streamlit dashboard"
LABEL maintainer="PBG"
LABEL version="0.1"

USER root

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONPATH="/opt/" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install poetry dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y --no-install-recommends \
    vim libpq-dev gcc curl openssh-client git unixodbc-dev libxml2-dev libxslt1-dev zlib1g-dev g++\
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Install sql server odbc drivers
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && sudo apt-get update \
    && sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && echo 'export PATH="$PATH:/opt/mssql-tools17/bin"' >> ~/.bashrc \
    && sudo apt-get install -y unixodbc-dev libgssapi-krb5-2


# Install project libraries
#ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
#RUN pip install "poetry==$POETRY_VERSION"

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false



# Project Python definition
# WORKDIR /admin_app

#Copy all the project files
COPY pyproject.toml .
COPY poetry.lock .

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-root --no-dev --no-interaction --no-ansi

# COPY launch.sh .
# COPY launch_init.sh .

USER airflow

#Launch the main (if required)
# RUN chmod +x launch.sh
# CMD ["bash", "launch.sh"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${APP_ENDPOINT_PORT:-8045}", "app.main:app"]