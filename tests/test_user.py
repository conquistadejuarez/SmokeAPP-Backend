from asynctest import patch
import tortoise.timezone
from tests.helper import test_base
import users_api as api
import unittest
import users_api.brands
import users_api.user_regiter
from datetime import datetime, timedelta

from users_models import models

id_tenant = '00000000-1111-2222-3333-000000000001'
DEFAULT_PASSWORD = "DefaultComplexPassword1._?"


class test_is_valid_username(unittest.TestCase):

    def test_valid_username(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera'))

    def test_invalid_username(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera+zika'))

    def test_invalid_username_invalid_email(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera@zika'))

    def test_invalid_username_invalid_email2(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera@zika@mika.com'))

    def test_invalid_username_valid_email(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera@zika.com'))

    def test_invalid_username_valid_email_2(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera@zika.co.rs'))


class test_password_strength(unittest.TestCase):
    def test(self):
        # self.assertEqual(5, users_api.user_regiter.password_strength('Pera#.123!_'))
        print(users_api.user_regiter.password_strength(''))


class test_is_valid_password(unittest.TestCase):

    def test_valid_strong_password(self):
        self.assertEqual((True, ''), users_api.user_regiter.is_valid_password('Pera#.123!_'))

    def test_invalid_non_strong_password(self):
        self.assertEqual((False, 'minimum 6 characters is required'), users_api.user_regiter.is_valid_password('pera'))

    def test_invalid_non_strong_password_min_1_uppercase(self):
        self.assertEqual((False, 'minimum 1 uppercase letter is required'),
                         users_api.user_regiter.is_valid_password('peraperic'))

    def test_invalid_non_strong_password_min_1_lowercase(self):
        self.assertEqual((False, 'minimum 1 lowercase letter is required'),
                         users_api.user_regiter.is_valid_password('PERAPERIC'))

    def test_minimum_1_character_is_required(self):
        self.assertEqual((False, 'minimum 1 character is required'), users_api.user_regiter.is_valid_password('123456'))

    def test_minimum_1_number_is_required(self):
        self.assertEqual((False, 'minimum 1 number is required'), users_api.user_regiter.is_valid_password('ABCdefg'))

    def test_password_contains_username(self):
        self.assertEqual((False, 'password should not contains username'),
                         users_api.user_regiter.is_valid_password('Igor123._', 'Igor'))

    def test_minimum_1_spec_char_is_required(self):
        self.assertEqual((False, 'minimum 1 special character !@#$%^&*()_-+=/.,; is required'),
                         users_api.user_regiter.is_valid_password('ABCdefg1'))


class test_model_methods(test_base):

    def setUp(self):
        super().setUp()
        res = self.a(users_api.brands.add('Marlboro', 20, 200, 10))
        self.id_brand = res['id']
        self.username2id = {}

    def create_user_on_day(self, username, date_day):
        with patch('users_api.today', return_value=date_day):
            res = self.a(
                api.register(id_tenant, username, DEFAULT_PASSWORD, id_brand_smoking=self.id_brand, average_per_day=15,
                             quit_date=api.today()))
            self.username2id[username] = res['id_user']

    def test_days_since_user_quits(self):
        # self.flush_db_at_the_end = False

        self.create_user_on_day('milos', datetime(2021, 3, 15).date())
        self.create_user_on_day('igor', datetime(2020, 8, 24).date())

        import tortoise.timezone

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2021, 3, 18).date()):
            self.assertEqual(3, self.a(users_api.days_since_user_quits(self.username2id['milos'])))

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2021, 3, 20).date()):
            self.assertEqual(5, self.a(users_api.days_since_user_quits(self.username2id['milos'])))

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2021, 3, 20).date()):
            self.assertEqual(208, self.a(users_api.days_since_user_quits(self.username2id['igor'])))

        #self.flush_db_at_the_end = False

    def test_calc_money_spend_per_day(self):
        self.create_user_on_day('dragan', datetime(2021, 3, 22).date())
        self.assertEqual(150, self.a(users_api.calc_money_spend_per_day(self.username2id['dragan'])))

    def test_how_much_money_user_saved(self):
        self.create_user_on_day('pedja', datetime(2021, 4, 22))

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2021, 4, 25).date()):
            self.assertEqual(3 * 150, self.a(users_api.calc_money_not_spend(self.username2id['pedja'])))

    def test_how_much_cigarettes_user_did_not_smoke(self):
        self.create_user_on_day('igor', datetime(2021, 4, 22))

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2021, 4, 25).date()):
            self.assertEqual(3*15, self.a(users_api.calc_cigarettes_user_did_not_smoke(self.username2id['igor'])))


class test_register_user(test_base):

    def test_register(self):
        res = self.a(users_api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']

        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertIsNotNone(res)
        self.assertIn('id_user', res)
        self.assertIn('status', res)
        self.assertEqual('ok', res['status'])

        #self.flush_db_at_the_end = False

    def test_try_register_user_with_existing_username_on_same_tenant(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']

        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertIsNotNone(res)
        self.assertIn('status', res)
        self.assertIn('id_user', res)
        self.assertEqual('ok', res['status'])

        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertNotIn('id', res)
        self.assertIn('id_error', res)
        self.assertIn('status', res)
        self.assertEqual('error', res['status'])
        self.assertEqual('REGISTER_ERROR', res['id_error'])

    def test_try_to_register_user_with_invalid_username(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']

        res = self.a(
            api.register(id_tenant, 'pera+zika', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                         quit_date=api.today()))
        self.assertEqual({'status': 'error', 'message': 'invalid username', 'id_error': 'REGISTER_ERROR'}, res)

        res = self.a(api.register(id_tenant, 'p', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertEqual({'status': 'error', 'id_error': 'REGISTER_ERROR', 'message': 'invalid username'}, res)

    def test_try_to_register_user_with_simple_password(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']
        res = self.a(api.register(id_tenant, 'user', 'user123', id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertIn('id_error', res)
        self.assertEqual('PASSWORD_TO_WEAK', res['id_error'])


class test_login_user(test_base):

    def test_login_user_who_dont_exists(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']
        res = self.a(api.login(id_tenant, 'pera', DEFAULT_PASSWORD))
        self.assertEqual('ERROR_LOGGING_USER', res['id_error'])

    def test_login_user(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']
        res = self.a(api.register(id_tenant, 'zika', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                  quit_date=api.today()))
        self.assertEqual('ok', res['status'])

        res = self.a(api.login(id_tenant, 'zika', DEFAULT_PASSWORD))
        self.assertEqual('ok', res['status'])
        self.assertIn('id_user', res)
        self.assertIn('id_session', res)
        self.assertIn('expires_on', res)

        id_session = res['id_session']

        res = self.a(api.check(id_session))
        print(res)

    def test_user_register(self):
        res = self.a(api.brands.add('Marlboro', 20, 200, 10))
        id_brand = res['id']
        user = self.a(api.register(id_tenant, 'Milos', DEFAULT_PASSWORD, id_brand_smoking=id_brand, average_per_day=15,
                                   quit_date=api.today()))
        self.assertIn('id_user', user)
