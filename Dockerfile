FROM python:3.11.6-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY weather_reminder/requirements/prod.txt ./requirements/prod.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r requirements/prod.txt


WORKDIR /weather_reminder

COPY weather_reminder .
