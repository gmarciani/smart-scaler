# Smart Scaler / Cyclic
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM python:3.6

LABEL Description="Smart Scaler / Cyclic" Vendor="Giacomo Marciani" Version="1.0.0"

# OS UPDATE
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

# SOURCES
COPY smartscalers/cyclic /app/smartscalers/cyclic
COPY smartscalers/common /app/smartscalers/common

# Change working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r smartscalers/cyclic/requirements.txt

# Make port 18002 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "smartscalers/cyclic/main.py"]