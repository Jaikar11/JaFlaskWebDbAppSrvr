#!flask/bin/python
import json
from flask import Flask, Response
from App.app import flaskrun

application = Flask(__name__)

if __name__ == '__main__':
    flaskrun(application)