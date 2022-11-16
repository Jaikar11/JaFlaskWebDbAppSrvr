# start by pulling the python image
#Download base image ubuntu 20.04
FROM ubuntu:20.04
#FROM python:3.9

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && pip3 install virtualenv \  
  && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /Flask-App

#Copy All files from App-Dir to Flask-App Direto
COPY ./App-Dir /Flask-App


# copy the requirements file into the image
RUN pip3 install -r requirements.txt

#Execute flask from bash script 
CMD ["/bin/bash", "scripts/local_run_script.sh"]
