import os
import json
import utils.distance as d
from urllib.parse import quote
from tornado import ioloop, web, httpclient

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "templates": os.path.join(os.path.dirname(__file__), "views"),
    "debug": False,
    "autoreload": False,
    "template_path":  os.path.join(os.path.dirname(__file__), "views"),
    "compiled_template_cache": False
}


API_TOKEN = open('secrets.txt').read().strip('\n')
GEOCODE_URL = '//maps.googleapis.com/maps/api/geocode/json'
ADDRESS_URL = '//maps.googleapis.com/maps/api/address/json'


class BaseHandler(web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code >= 400:
            self.write(dict(SUCCESS=False, payload=[]))

    def format_params(self, params) -> str:
        ''' concat the list of form args into a urlencoded string '''
        return ','.join(map(quote, params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render('main.html', title="GeoCode App")


class GeoHandler(BaseHandler):
    async def post(self):
        street = self.get_argument('street')
        city = self.get_argument('city')
        if not street or not city:
            # fails fast if missing args
            return self.render(
                    'error.html',
                    msg='Missing required "City" & "Street" values'
                    )

        geocode_req_qs = self.format_params([street, city])

        def handle_geo_response(payload):
            ''' callback invoked on the response from geocode API '''
            if payload.error:
                self.render('error.html', msg=payload.error)

            res_raw = dict(json.loads(bytes.decode(payload.body)))

            if res_raw['status'] == 'ZERO_RESULTS':
                self.write(json.dumps(res))

            else:
                [res_geo] = res_raw['results']
                geo_data = dict(
                        SUCCESS=True,
                        full_address=res_geo['formatted_address'],
                        **res_geo['geometry'],
                        place_id=res_geo['place_id'])

                self.write(json.dumps(geo_data))

        request = httpclient.AsyncHTTPClient()
        url = 'https:{0}?address={1}&key={2}'.format(
                GEOCODE_URL,
                geocode_req_qs,
                API_TOKEN
                )
        res = await request.fetch(url)
        handle_geo_response(res)


class ReverseHandler(BaseHandler):
    def get(self):
        return self.render('address.html', title="Reverse Lookup")

    async def post(self):
        lat = self.get_argument('lat')
        lon = self.get_argument('long')
        if not lat or not lon:
            # fails fast if missing args
            return self.render(
                    'error.html',
                    msg='Missing required "Latitude" & "Longitude" values'
                    )

        reverse_qs = self.format_params([lat, lon])

        def handle_reverse_response(payload):
            ''' callback invoked on the response from reverse geocode API '''
            if payload.error:
                self.render('error.html', msg=payload.error)

            res_raw = dict(json.loads(bytes.decode(payload.body)))

            if res_raw['status'] != 'OK':
                self.write(json.dumps(res))
            else:
                res_reverse = res_raw['results'][0]
                geo_data = dict(
                        SUCCESS=True,
                        full_address=res_reverse['formatted_address'],
                        place_id=res_reverse['place_id'])

                self.write(json.dumps(geo_data))

        request = httpclient.AsyncHTTPClient()
        url = 'https:{0}?latlng={1}&key={2}'.format(
                GEOCODE_URL,
                reverse_qs,
                API_TOKEN
                )
        res = await request.fetch(url)
        handle_reverse_response(res)


class DistanceHandler(BaseHandler):
    def get(self):
        return self.render('distance.html', title="Distance")

    async def post(self):
        sorted_keys = sorted(self.request.arguments.keys())
        args_list = []
        for x in sorted_keys:
            pt = self.get_argument(x)
            if not pt:
                return self.render(
                    'error.html',
                    msg='Missing required "Latitude" & "Longitude" values')
            else:
                args_list.append(float(pt))

        [lat1, lat2, lon1, lon2] = args_list

        distance = d.get_distance(lat1, lat2, lon1, lon2)
        res = dict(
                SUCCESS=True,
                distance=distance)

        self.write(json.dumps(res))


def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r"/geocode", GeoHandler),
        (r"/address", ReverseHandler),
        (r"/distance", DistanceHandler),
        (r"/static/(.*)", web.StaticFileHandler,
            dict(path=settings['static_path'])),
        ], **settings)


def main():
    app = make_app()
    app.listen(4000)
    print('listening on 4000')
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
