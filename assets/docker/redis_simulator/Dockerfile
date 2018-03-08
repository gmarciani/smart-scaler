# Smart Scaler / Redis Simulator
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM python:3.6

LABEL Description="Smart Scaler / Redis Simulator" Vendor="Giacomo Marciani" Version="1.0.0"

# ARGUMENTS
ARG rootdir=../..

# OS UPDATE
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# SOURCES
ADD $rootdir/services/redis_simulator /app/services/redis_simulator
ADD $rootdir/services/common /app/services/common

WORKDIR /app

COPY ../../main/services/redis_simulator/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 18003

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]