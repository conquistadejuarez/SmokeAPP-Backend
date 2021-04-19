from tests.helper import test_base
import users_api.diseases as diseases_api


class test_diseases_crud(test_base):

    def test_add_disease(self):
        self.assertIn('id', self.a(diseases_api.add('Bolest1', 'Lorem ipsum dolor sit amet.', 8)))
        self.assertIn('name', self.a(diseases_api.add('Bolest10','Lorem ipsum',5)))
        self.assertIn('description', self.a(diseases_api.add('Bolest12','Lorem ipsum dolor sit ares mar.', 10)))

    def test_get_by_id(self):
        res = self.a(diseases_api.add('Bolest2', 'Lorem ipsum dolor sit amet.', 6))
        self.assertIn('id', res)
        id_disease = res['id']
        r = self.a(diseases_api.get(id_disease))
        # print(r)

    def test_get_all(self):
        self.assertEqual(0, len(self.a(diseases_api.get_all())))
        res = self.a(diseases_api.add('Bolest3', 'Lorem ipsum dolor sit amet.', 9))
        # print(res)
        self.assertEqual(1, len(self.a(diseases_api.get_all())))
        self.a(diseases_api.add('Bolest4', 'Lorem ispum dolor sit amet.', 4))
        self.assertEqual(2, len(self.a(diseases_api.get_all())))
