import unittest
from app import BaseHandler


class TestBaseHandler(unittest.TestCase):
    def test_format_params(self):
        params0 = ['123 Test Ave']
        params1 = ['123 Test Ave', 'Test City']

        self.assertEqual(
                BaseHandler.format_params(params0),
                '123%20Test%20Ave',
                'should format form args')

        self.assertEqual(
                BaseHandler.format_params(params1),
                '123%20Test%20Ave,Test%20City',
                'should format all keys form args')


if __name__ == '__main__':
    unittest.main()
