# syntax=docker/dockerfile:1
FROM python:3.10

COPY requirements.txt /opt/devman_bot/requirements.txt
WORKDIR /opt/devman_bot
RUN pip install -r requirements.txt

COPY main.py /opt/devman_bot/

CMD python main.py
