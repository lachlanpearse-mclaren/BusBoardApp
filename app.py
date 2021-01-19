from flask import Flask
from flask import render_template, request, redirect
from operator import itemgetter
from busboard.BusBoard import departure_list

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/',methods=['POST'])
def show_departures():
    postcode=request.form.get('postcode')
    departures = departure_list(postcode)
    return render_template('index.html', departures=departures)

if __name__ == '__main__':
    app.run()
