FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_PROD=true

RUN mkdir /api
WORKDIR /api

COPY requirements.txt /api/
RUN apt-get update && apt-get install gcc -y && apt-get install curl -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /api/
CMD ["python3", "manage.py", "bot", "start"]
