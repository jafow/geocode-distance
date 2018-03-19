import os
import unittest
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


class MainController(web.RequestHandler):
    def get(self):
        return self.render('main.html', title="GeoCode App")


class GeoController(web.RequestHandler):
    async def post(self):
        street = self.get_argument('street')
        city = self.get_argument('city')
        if not street or not city:
            # fails fast if missing args
            return self.render(
                    'error.html',
                    msg='Missing required "City" & "Street" values'
                    )

        geocode_params = format_params(dict(street=street, city=city))

        def handle_geo_response(payload):
            ''' callback invoked on the response from geocode API '''
            if payload.error:
                self.render('error.html', msg=payload.error)
            else:
                self.render('geo-results.html', street='', body=payload.body)

        def format_params(params) -> dict:
            ''' escape, format, validate each string in a list of params '''
            res = dict()
            for key, val in params:
                if not val:
                    self.render('error.html', msg='Missing required field:{}'.format(key))
                res[key] = val.replace(' ', '+')

        request = httpclient.AsyncHTTPClient()
        url = 'https:{0}address={1},+{2}+{3}&key={4}'.format(
                GEOCODE_URL,
                _st,
                city,
                state,
                API_TOKEN
                )
        res = await request.fetch(url)
        handle_geo_response(res)


class ReverseController(web.RequestHandler):
    def get(self):
        return self.write('Reverse')


class DistanceController(web.RequestHandler):
    def get(self):
        return self.write('distance')


def make_app():
    return web.Application([
        (r"/", MainController),
        (r"/geocode", GeoController),
        (r"/reverse", ReverseController),
        (r"/distance", DistanceController),
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
