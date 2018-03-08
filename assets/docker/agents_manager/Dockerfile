# Smart Scaler / Agents Manager
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM python:3.6

LABEL Description="Smart Scaler / Agents Manager" Vendor="Giacomo Marciani" Version="1.0.0"

# ARGUMENTS
ARG rootdir=../..

# OS UPDATE
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# SOURCES
ADD $rootdir/services/agents_manager /app/services/agents_manager
ADD $rootdir/services/common /app/services/common

# Change working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Make port 18002 available to the world outside this container
EXPOSE 18002

# Run app.py when the container launches
CMD ["python3", "app.py"]
