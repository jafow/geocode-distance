import os
import json
from urllib.parse import quote
from tornado import ioloop, web, httpclient

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "xsrf_cookies": True,
    "templates": os.path.join(os.path.dirname(__file__), "views"),
    "debug": True,
    "autoreload": True,
    "template_path":  os.path.join(os.path.dirname(__file__), "views"),
    "compiled_template_cache": False
}

API_TOKEN = open('secrets.txt').read().strip('\n')
GEOCODE_URL = '//maps.googleapis.com/maps/api/geocode/json?'
ADDRESS_URL = '//maps.googleapis.com/maps/api/address/json?'


class BaseHandler(web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code >= 400:
            self.write(dict(SUCCESS=False, payload=[]))


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
        return self.write('Reverse')


class DistanceHandler(BaseHandler):
    def get(self):
        return self.write('distance')


def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r"/geocode", GeoHandler),
        (r"/reverse", ReverseHandler),
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
