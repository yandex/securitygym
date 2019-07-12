FROM python:3.6-alpine

RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update --no-cache g++ gcc libxslt-dev py-lxml

COPY courses/python/requirements.txt /

RUN python3 -m pip install -r /requirements.txt