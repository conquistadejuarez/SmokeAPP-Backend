#!.venv/bin/python


import tornado.ioloop
import tornado.web
import json

import users_api as api
import os

from users_models import models
import users_api.brands as brands_api
import users_api.diseases as disease_api


class RegisterHandler(tornado.web.RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode())

        id_tenant = body['id_tenant']
        username = body['username']
        password = body['password']
        average_per_day = body['average_per_day'] if 'average_per_day' in body else None
        id_brand_smoking = body['brand_smoking'] if 'brand_smoking' in body else None
        quit_date = body['quit_date'] if 'quit_date' in body else None

        res = await api.register(id_tenant, username, password, id_brand_smoking, average_per_day, quit_date)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


class LoginHandler(tornado.web.RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode())

        id_tenant = body['id_tenant']
        username = body['username']
        password = body['password']

        res = await api.login(id_tenant, username, password)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


async def authorized(handler):
    if 'Authorization' not in handler.request.headers:
        handler.set_status(401)
        handler.write(json.dumps({'message': 'not authorized'}))
        return False

    id_session = handler.request.headers['Authorization']

    res = await api.check(id_session)
    if 'error' in res['status']:
        handler.set_status(401)
        handler.write(json.dumps({'message': 'not authorized'}))
        return False

    return res


class ProtectedMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        if not await authorized(self):
            return

        self.write(json.dumps({'message': 'This is message only for logged users'}))
        return None


class singleBrandMethodHandler(tornado.web.RequestHandler):

    async def get(self, id_brand):
        self.write(json.dumps(await brands_api.get(id_brand)))


class brandsMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        self.write(json.dumps(await brands_api.get_all()))

    async def post(self):
        body = json.loads(self.request.body.decode())

        name = body['name']
        pack_quantity = body['pack_quantity']
        pack_price = body['pack_price']
        model_strength = body['model_strength']

        res = await brands_api.add(name, pack_quantity, pack_price, model_strength)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


class FHandler(tornado.web.RequestHandler):

    async def get(self, command: str):
        self.write(json.dumps(await brands_api.get_all()))

        if command=='..':
            pass
        if command=='..':
            pass
        if command=='..':
            pass

        self.set_status(404)
        self.write(json.dumps({'message': f'command {command} not exists'}, indent=4))
        return


class diseasesMethodHandler(tornado.web.RequestHandler):

    async def get(self):
        self.write(json.dumps(await disease_api.get_all()))

    async def post(self):
        body = json.loads(self.request.body.decode())

        name = body['name']
        description = body['description']
        disease_difficulty = body['disease_difficulty']
        time_to_recover = body['time_to_recover']

        res = await api.diseases_init(name, description, disease_difficulty, time_to_recover)

        if 'id_error' in res:
            self.set_status(400)
            self.write(json.dumps(res, indent=4))
            return

        self.set_status(200)
        self.write(json.dumps(res, indent=4))
        return


def make_app():
    return tornado.web.Application([
        (r"/api/users/register", RegisterHandler),
        (r"/api/users/login", LoginHandler),
        (r"/api/protected", ProtectedMethodHandler),
        (r"/api/brands", brandsMethodHandler),
        (r"/api/brands/(.*)", singleBrandMethodHandler),
        (r"/api/diseases", diseasesMethodHandler),
        (r"/api/f/(.*)", FHandler),
    ])


import tortoise


async def init_db():
    current_file_folder = os.path.dirname(os.path.realpath(__file__))
    with open(f'{current_file_folder}/users_config/config.json', 'rt') as f:
        c = json.load(f)

    await tortoise.Tortoise.init(
        db_url=f"postgres://{c['user']}:{c['password']}@{c['host']}/{c['dbname']}",
        modules={"models": [models]},
    )

    await tortoise.Tortoise.generate_schemas()


if __name__ == "__main__":
    app = make_app()

    from tornado.ioloop import IOLoop

    loop = IOLoop.current()

    app.listen(8888)

    loop.run_sync(init_db)

    tornado.ioloop.IOLoop.current().start()
