"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq

api = openaq.OpenAQ()

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    la_list = [(i['date']['utc'], i['value']) for i in body['results']]
    return str(la_list)
