FROM python:3.11-slim

ENV PATH /usr/local/bin:$PATH
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=True \
    APP_HOME=/app \
    PORT=5000

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -yqq wget unzip curl nano
    
RUN apt-get purge -y --auto-remove ca-certificates wget

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       wget \
       libreoffice \
       default-jre \
       libreoffice-java-common \
    && rm -rf /var/lib/apt/lists/*
RUN	apt-get libreoffice --version

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --ignore-pipfile --deploy --dev

# Install unoserver in libreoffice phyton version
RUN mkdir /environments
RUN virtualenv --python=/usr/bin/python3 --system-site-packages /environments/virtenv
RUN /environments/virtenv/bin/pip install unoserver

# Install application into container
COPY . .

# Expose the port the app runs on
EXPOSE $PORT/tcp

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 30 main:app
