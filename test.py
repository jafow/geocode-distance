import unittest
import json
import app
from tornado import testing


class TestBaseHandler(unittest.TestCase):
    ''' unit test for app BaseHandler '''
    def test_format_params(self):
        params0 = ['123 Test Ave']
        params1 = ['123 Test Ave', 'Test City']
        self.assertEqual(
                app.BaseHandler.format_params(self, params0),
                '123%20Test%20Ave',
                'should format form args')

        self.assertEqual(
                app.BaseHandler.format_params(self, params1),
                '123%20Test%20Ave,Test%20City',
                'should format all keys form args')


class TestGeocodeRoute(testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_valid_args(self):
        body_success = 'street=1600+Amphitheatre+Pkwy&city=+Mountain+View'
        success_address = (
                'Google Building 41, '
                '1600 Amphitheatre Pkwy, '
                'Mountain View, CA 94043, USA')

        res_raw = self.fetch('/geocode', method='POST', body=body_success)
        try:
            res_dict = json.loads(bytes.decode(res_raw.body))
        except json.decoder.JSONDecodeError:
            res_dict = dict()

        self.assertEqual(res_dict['SUCCESS'], True)
        self.assertEqual(
                res_dict['full_address'],
                success_address)
        self.stop()

    def test_invalid_args(self):
        body_fail_missing_arg = 'street=1600+Amphitheatre+Pkwy&city='

        res_raw = self.fetch(
                '/geocode',
                method='POST',
                body=body_fail_missing_arg)
        err_template = bytes.decode(res_raw.body)

        self.assertEqual(err_template != '', True)
        self.assertEqual('Missing required' in err_template, True)
        self.stop()


class TestReverseRoute(testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_valid_args(self):
        body_success = 'lat=40.714224&long=-73.961452'
        success_address = '277 Bedford Ave, Brooklyn, NY 11211, USA'

        res_raw = self.fetch('/address', method='POST', body=body_success)
        try:
            res_dict = json.loads(bytes.decode(res_raw.body))
        except json.decoder.JSONDecodeError:
            res_dict = dict()

        self.assertEqual(res_dict['SUCCESS'], True)
        self.assertEqual(
                res_dict['full_address'],
                success_address)
        self.stop()

    def test_invalid_args(self):
        body_fail_missing_arg = 'lat=40.714224&long='

        res_raw = self.fetch(
                '/address',
                method='POST',
                body=body_fail_missing_arg)
        err_template = bytes.decode(res_raw.body)

        self.assertEqual(err_template != '', True)
        self.assertEqual('Missing required' in err_template, True)
        self.stop()


class TestDistanceRoute(testing.AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_valid_args(self):
        body_success = (
                'lat1=40.714224&long1=124.33241&'
                'lat2=41.23535&long2=134.33422')
        success_distance = 888.7342392295541

        res_raw = self.fetch('/distance', method='POST', body=body_success)
        try:
            res_dict = json.loads(bytes.decode(res_raw.body))
        except json.decoder.JSONDecodeError:
            res_dict = dict()

        self.assertEqual(res_dict['SUCCESS'], True)
        self.assertEqual(
                res_dict['distance'],
                success_distance)
        self.stop()

    def test_invalid_args(self):
        body_fail_missing_arg = 'lat=40.714224&long='

        res_raw = self.fetch(
                '/address',
                method='POST',
                body=body_fail_missing_arg)
        err_template = bytes.decode(res_raw.body)

        self.assertEqual(err_template != '', True)
        self.assertEqual('Missing required' in err_template, True)
        self.stop()


if __name__ == '__main__':
    unittest.main()
