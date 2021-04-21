import unittest
import json
from unittest.mock import patch
from tests.helper import test_base_tornado, TestingHelper
from tornado.httpclient import AsyncHTTPClient
from datetime import datetime, timedelta
from tests.test_rest import ID_TENANT
import uuid


class TestBrandsRest(TestingHelper):

    def setUp(self):
        super().setUp()
        res = self.add_brand('Marlboro',20,200,10)
        self.id_brand = res['id']
        self.api(None, 'POST', '/api/users/register',
                 body={
                     'id_tenant': ID_TENANT,
                     'username': 'user',
                     'password': '123ABCa.',
                     'brand_smoking': self.id_brand,
                     'average_per_day': 15,
                     'quit_date': str(datetime.today() - timedelta(5))
                 })

        print(self.last_code)
        print(self.last_result)

        self.assertEqual(200, self.last_code)
        print(self.last_code)
        self.id_session = self.last_result['id_session']


    def test_try_to_add_brand_that_already_exists(self):
        res = self.add_brand('Marlboro', 20, 200, 10)
        self.assertIn('status', res)
        self.assertEqual('error', res['status'])

    def test_add_brand(self):
        res = self.add_brand('Dunhill', 20, 200, 10)
        self.assertIn('status', res)
        self.assertEqual('ok', res['status'])

    def test_get_all_brands(self):
        self.api(None, 'GET', '/api/brands')
        self.assertEqual(1, len(self.last_result))

        self.add_brand('Dunhill', 20, 200, 10)
        self.api(None, 'GET', '/api/brands')
        self.assertEqual(2, len(self.last_result))

        self.add_brand('Best', 20, 200, 10)
        self.api(None, 'GET', '/api/brands')
        self.assertEqual(3, len(self.last_result))

    def test_get_single_brand(self):
        res = self.add_brand('Best', 20, 200, 10)
        id_brand = res['id']

        self.api(None, 'GET', '/api/brands/' + id_brand)
        print(self.last_code)
        print(self.last_result)


    def test_get_one_brand(self):
        r = self.add_brand('Marlboro2', 20, 20, 6)
        self.assertIn('id', r)
        #print(self.last_code)
        #print(self.last_result)


if __name__ == '__main__':
    unittest.main()
