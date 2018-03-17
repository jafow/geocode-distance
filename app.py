from flask import Flask
from flask import render_template, request
import requests as req

f = open('secrets.txt').read().strip('\n')

API_TOKEN = f

GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'

app = Flask(__name__)


@app.route('/')
def index():
    return 'home'


@app.route('/geocode', methods=['GET', 'POST'])
def geocode():
    street = request.args.get('street')
    # street = street.replace(' ', '+')
    city = request.args.get('city')

    print('street: ', street, ' city', city)

    url = '{0}address={1}{2}&key={3}'.format(
            GEOCODE_URL,
            street,
            city,
            API_TOKEN)

    r = req.get(url)

    if r.status_code >= 200 and r.status_code < 400:
        res = r.json()
        return render_template('geo.html', street=street, city=city, rest=res)
    else:
        return render_template(
                'error.html',
                error='There was an error fetching the address')


# geocode api is at:
# https://maps.googleapis.com/maps/api/geocode/json
# geocode lookup is at /?address=<1000+Street+Name+Blvd, +City, CA>&key=<TOKEN>
# reverse lat/long is at /?latlng=40.714224,-73.961452&key=<TOKEN>
