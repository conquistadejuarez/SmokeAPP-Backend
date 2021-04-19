from tests.helper import test_base
import users_api as api
import unittest

import users_api.user_regiter

id_tenant = '00000000-1111-2222-3333-000000000001'

import users_api.brands as brands_api

class test_brands_crud(test_base):

    def test_add(self):
        self.assertIn('id', self.a(brands_api.add('Marlboro', 20, 200, 10)))

    def test_get_by_id(self):
        res = self.a(brands_api.add('Marlboro', 20, 200, 10))
        self.assertIn('id', res)
        id_brand = res['id']
        r = self.a(brands_api.get(id_brand))

    def test_get_all(self):

        self.assertEqual(0,len(self.a(brands_api.get_all())))
        self.assertIn('id', self.a(brands_api.add('Marlboro', 20, 200, 10)))
        self.assertEqual(1,len(self.a(brands_api.get_all())))
