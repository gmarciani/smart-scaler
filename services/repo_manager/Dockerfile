# Smart Scaler / Repo Manager
#
# VENDOR                Giacomo Marciani
# VERSION               1.0.0

FROM ubuntu:latest

# Update OS
RUN apt-get update -y
RUN apt-get upgrade -y

# Install Python
RUN apt-get install -y build-essential python3 python3-dev python3-pip
RUN pip3 install --upgrade pip

# Copy files
ADD . /app

# Change working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Make port 18003 available to the world outside this container
EXPOSE 18003

# Run app.py when the container launches
CMD ["python3", "app.py"]
