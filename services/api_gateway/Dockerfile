# Smart Scaler / Api Gateway
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM ubuntu:latest

LABEL Description="Smart Scaler / Api Gateway" Vendor="Giacomo Marciani" Version="1.0.0"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev

ADD . /app

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 18002

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]