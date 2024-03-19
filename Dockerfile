# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /code
COPY /src /code

RUN pip install -r configs/requirements.txt

WORKDIR /web_app

CMD gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:${PORT}