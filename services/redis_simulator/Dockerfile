# Smart Scaler / Repo Manager
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

#FROM ubuntu:latest
FROM python:3.6

LABEL Description="Smart Scaler / Repo Manager" Vendor="Giacomo Marciani" Version="1.0.0"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev

ADD . /app

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 18003

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]