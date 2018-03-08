# Smart Scaler / Api Gateway
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM python:3.6

LABEL Description="Smart Scaler / Api Gateway" Vendor="Giacomo Marciani" Version="1.0.0"

# ARGUMENTS
ARG rootdir=../..

# OS UPDATE
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# SOURCES
ADD $rootdir/services/api_gateway /app/services/api_gateway
ADD $rootdir/services/common /app/services/common

# Change working directory
WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

# Make port 18001 available to the world outside this container
EXPOSE 18001

# Run app.py when the container launches
CMD ["python3", "app.py"]
