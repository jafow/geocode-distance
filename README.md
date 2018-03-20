# geocode web app
A python app using the Google geocode API

## Overview
This is a web app built with a python application layer that fetches user
geocode data using Google's Geocode API.
This project is comprised of a server & route handlers found in `app.py`, server
rendered view templates in the `/views` directory and static files with the
client code in the `/static` directory.

## Requirements

This project assumes python versions 3.5+. It is suggested to install & run the
app within a `virtualenv`.

This project requires an api token to use the Google Geocode API. Once it's
obtained, paste it into a file called `secrets.txt` in the project root
directory. Info on gettng a key can be
found on [google's geocoding docs]
(https://developers.google.com/maps/documentation/geocoding/get-api-key).


## Install

1.  Create a virtual environment:

```bash
$ python3 -m venv env
```

2. From the project root directory, install the dependencies

```bash
$ pip install -r requirments.txt
```

4. To start the server run:

```bash
$ python3 app.py
```

This will start a webserver on running on `http://localhost:4000`.

## Tests
Unit tests and route handling tests are found in the `test.py` file.
Run with:
```bash
$ python3 test.py
```

Once the server is running, you can inspect sample payloads from the API you can run these commands in a separate
terminal using `curl`. For example:

```bash
$ curl -s -d 'street=1600+Amphitheatre+Parkway&city=Mountain+View' http://localhost:4000/geocode | python3 -m json.tool
# returns geocode payload

$ curl -s -d 'lat=37.4238253802915&long=-122.0829009197085' http://localhost:4000/address | python3 -m json.tool
# returns reverse payload

$ curl -s -d 'lat1=37.4238253802915&long1=-122.0829009197085&lat2=41.41224&long2=132.0324356' http://localhost:4000/distance | python3 -m json.tool
# returns distance payload
```


