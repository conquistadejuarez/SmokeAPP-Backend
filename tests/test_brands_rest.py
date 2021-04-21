import unittest
import json
from unittest.mock import patch
from tests.helper import test_base_tornado
from tornado.httpclient import AsyncHTTPClient

from tests.test_rest import ID_TENANT
import uuid


class TestBrandsRest(test_base_tornado):

    def setUp(self):
        super().setUp()
        res = self.add_brand('Marlboro',20,200,10)
        id_brand = res['id']
        self.api(None, 'POST', '/api/users/register',
                 body={
                     'id_tenant': ID_TENANT,
                     'username': 'user',
                     'password': '123ABCa.',
                     'id_brand_smoking': id_brand,
                     'average_per_day': 15
                 })

        self.assertEqual(200, self.last_code)
        print(self.last_code)
        self.id_session = self.last_result['id_session']


    def test_add_brand(self):
        res = self.add_brand('Marlboro', 20, 200, 10)
        self.assertIn('id', res)

    def test_get_all_brands(self):
        self.api(None, 'GET', '/api/brands')
        self.assertEqual([], self.last_result)

        self.add_brand('Marlboro', 20, 200, 10)
        self.api(None, 'GET', '/api/brands')
        self.assertEqual(1, len(self.last_result))

        self.add_brand('Best', 20, 200, 10)
        self.api(None, 'GET', '/api/brands')
        self.assertEqual(2, len(self.last_result))

    def test_get_single_brand(self):
        res = self.add_brand('Best', 20, 200, 10)
        id_brand = res['id']

        self.api(None, 'GET', '/api/brands/' + id_brand)
        print(self.last_code)
        print(self.last_result)

    def add_brand(self, name, pack_quantity, pack_price, model_strength):
        self.api(None, 'POST', '/api/brands',
                 body={
                     'name': name,
                     'pack_quantity': pack_quantity,
                     'pack_price': pack_price,
                     'model_strength': model_strength})
        return self.last_result
        # TODO: assert

    def test_get_one_brand(self):
        r = self.add_brand('Marlboro', 20, 20, 6)
        self.assertIn('id', r)
        #print(self.last_code)
        #print(self.last_result)


if __name__ == '__main__':
    unittest.main()
