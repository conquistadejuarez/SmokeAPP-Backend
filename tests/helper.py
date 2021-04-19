import unittest
from tortoise.contrib.test import initializer, finalizer
import asyncio
import json
import os
from tornado.testing import AsyncHTTPTestCase

from users_models import models

current_file_folder = os.path.dirname(os.path.realpath(__file__))

class test_base(unittest.TestCase):
    def setUp(self):

        super().setUp()

        with open(f'{current_file_folder}/../users_config/config.json', 'rt') as f:
            c = json.load(f)

        self.loop = asyncio.new_event_loop()
        self.a = self.loop.run_until_complete

        c['dbname'] = 'test_'+c['dbname']

        initializer(
            modules={"users_models.models": models},
            db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
            loop=self.loop,
        )

    def tearDown(self):
        _flush_db = not hasattr(self, 'flush_db_at_the_end') or self.flush_db_at_the_end
        if _flush_db:
            finalizer()
        self.loop.close()


import service


class test_base_tornado(AsyncHTTPTestCase):

    def get_app(self):
        return service.make_app()

    def api(self, token, method, url, body={}):
        body = json.dumps(body)
        if method in ('GET', 'DELETE'):
            body = None

        self.last_code = 0
        self.last_result = {}

        headers = {}
        if token:
            headers['Authorization'] = token

        res = self.fetch(url, method=method, body=body, headers=headers)

        self.last_code = res.code
        try:
            self.last_result = json.loads(res.body.decode())
        except Exception as e:
            raise

        return res.code


    def setUp(self):

        super().setUp()

        with open(f'{current_file_folder}/../users_config/config.json', 'rt') as f:
            c = json.load(f)

        c['dbname'] = 'test_'+c['dbname']

        from tornado.ioloop import IOLoop

        self.loop = IOLoop.current()

        initializer(
            modules={"users_models.models": models},
            db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
            loop=self.loop.asyncio_loop,
        )

    def tearDown(self):
        _flush_db = not hasattr(self, 'flush_db_at_the_end') or self.flush_db_at_the_end
        if _flush_db:
            finalizer()
