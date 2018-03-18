import os
from tornado import ioloop, web, httpclient, gen

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
        state = self.get_argument('state')
        _st = street.replace(' ', '+')

        def handle_geo_response(payload):
            ''' callback invoked on the response from geocode API '''
            if payload.error:
                self.render('error.html', msg=payload.error)
            else:
                self.render('geo-results.html', street='', body=payload.body)

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
