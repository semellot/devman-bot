# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt /opt/devman_bot/requirements.txt
WORKDIR /opt/devman_bot
RUN pip install -r requirements.txt

COPY main.py /opt/devman_bot/

CMD python3 main.py
