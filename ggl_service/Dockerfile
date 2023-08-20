FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /api
WORKDIR /api

COPY requirements.txt /api/
RUN apt-get update && apt-get install gcc -y && apt-get install curl -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /api/
#CMD ["uwsgi", "--ini", "/api/uwsgi.ini"]
