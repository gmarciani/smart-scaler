# Smart Scaler / Kubernetes Simulator
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM python:3.6

LABEL Description="Smart Scaler / Kubernetes Simulator" Vendor="Giacomo Marciani" Version="1.0.0"

# ARGUMENTS
ARG rootdir=../..

# OS UPDATE
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# SOURCES
ADD $rootdir/services/kubernetes_simulator /app/services/kubernetes_simulator
ADD $rootdir/services/common /app/services/common

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 18002

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]