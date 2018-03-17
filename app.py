import tornado.ioloop
import tornado.web


class MainController(tornado.web.RequestHandler):
    def get(self):
        return 'main'


class GeoController(tornado.web.RequestHandler):
    def get(self):
        return 'Geo'


class ReverseController(tornado.web.RequestHandler):
    def get(self):
        return 'Reverse'


class DistanceController(tornado.web.RequestHandler):
    def get(self):
        return 'distance'


def main():
    return tornado.web.Application([
        (r'/', MainController),
        (r'/geocode', GeoController),
        (r'/reverse', ReverseController),
        ('/distance', DistanceController)
        ])


if __name__ == '__main__':
    app = main()
