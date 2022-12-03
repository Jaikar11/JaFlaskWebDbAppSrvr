This is a Flask WebApplication connecting to an existing Mysql DB
ipaddress.txt and rds_endpoint.txt are updated by parameters by local_run_script.sh
sqldbparms.txt has to be updated manually. 

Docker Commands: 

To build image: docker build -t flask-app .

Run Docker : docker run -d flask-app