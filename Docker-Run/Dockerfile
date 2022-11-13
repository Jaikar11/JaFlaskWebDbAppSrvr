# start by pulling the python image
FROM python:3.8-alpine

# Create app directory
WORKDIR /Flask-App

#Copy All files from App-Dir to Flask-App Direto
COPY ./App-Dir /Flask-App

# copy the requirements file into the image
CMD [./App-Dir/scripts/temp_run.sh]