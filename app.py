import os
import sys
from flask import Flask
import pymongo
from json import load

STATIC_FOLDER = sys.path[0] + '/static/'
TEMPLATES_FOLDER = sys.path[0] + '/templates/'

app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)

app.config['MONGO_URI'] = 'mongodb+srv://techtribes:techtribes123@cluster0.cmim8hl.mongodb.net/?retryWrites=true&w=majority'
app.secret_key = "SSKEY"

client = pymongo.MongoClient("mongodb+srv://techtribes:techtribes123@cluster0.cmim8hl.mongodb.net/?retryWrites=true&w=majority")
db = client.trans