"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
from tabulate import tabulate

api = openaq.OpenAQ()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    return str(records)
    # for i in body['results']:
    #     la_list.append((i['date']['utc'], i['value']))
    #tabulate(la_list, headers=['datetime', 'value'], tablefmt="github")

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<{}: {}>'.format(self.datetime, self.value)
        #tabulate([[self.datetime],[self.value]], tablefmt='grid')
        #tabulate(["id", self.id], tablefmt="github")


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # Get data from OpenAQ, make Record objects with it, and add to db
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    la_list = [(i['date']['utc'], i['value']) for i in body['results']]
    print(la_list)
    try:
        for i in la_list:
            object = Record(datetime=i[0], value=i[1])
            DB.session.add(object)
    except Exception as e:
        print('Error processing {}: {}'.format(i, e))
        raise e
    DB.session.commit()
    return 'Data refreshed!'
