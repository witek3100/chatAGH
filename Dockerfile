# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /code
COPY /src /code/src

ENV HOST 0.0.0.0

RUN pip install -r src/configs/requirements.txt

EXPOSE 8080

CMD gunicorn src.web-app.app:app -w 2 --threads 2 -b 0.0.0.0:${PORT}