FROM python:3.7-alpine
LABEL MAINTAINER Shahroz

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
EXPOSE 3000

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
