FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1

RUN mkdir /api
WORKDIR /api

RUN apt-get update && apt-get install gcc -y && pip install --upgrade pip
#RUN apt-get install curl -y

COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY requirements.txt /api/
RUN pip install -r requirements.txt

RUN python manage.py makemigrations && manage.py migrate

COPY . /api/

FROM base as api
CMD ["uwsgi", "--ini", "/api/uwsgi.ini"]

FROM base as consumer
CMD ["python3", "manage.py", "consumer", "--command", "run"]

FROM base as producer
CMD ["python3", "manage.py", "producer", "--command", "run"]

