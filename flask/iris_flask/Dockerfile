FROM python:3.7-buster

RUN apt-get update -y

WORKDIR /usr/src/app

ENV LANG C.UTF-8

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .