FROM ubuntu:latest

MAINTAINER Giacomo Marciani "gmarciani@acm.org"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]