FROM python:3.7-alpine

RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev python3-dev libffi-dev openssl-dev make

COPY courses/python/requirements.txt /

RUN python3 -m pip install -r /requirements.txt
