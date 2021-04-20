import uuid
import tortoise
from tortoise import Tortoise, fields
from tortoise.models import Model
import json
import datetime


class User(Model):
    class Meta:
        table = 'users'
        unique_together = (('id_tenant', 'username'),)

    id = fields.UUIDField(pk=True)
    id_tenant = fields.UUIDField(index=True)
    username = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    active = fields.BooleanField(null=False, default=True)
    average_per_day = fields.IntField(null=False, default=15)
    #brand_smoking = fields.ForeignKeyField("models.CigarettesBrand", null=False, index=True, related_name='smokers')



class CigarettesBrand(Model):
    class Meta:
        table = 'cigarettes_brands'

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128, unique=True)
    pack_quantity = fields.IntField()
    pack_price = fields.IntField()
    model_strength = fields.IntField()

    #smokers: fields.ReverseRelation["User"] = fields.ReverseRelation


class Diseases(Model):
    class Meta:
        table = 'diseases'

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128, unique=True)
    description = fields.TextField()
    disease_difficulty = fields.IntField()
    time_to_recover = fields.IntField()


class Session(Model):
    class Meta:
        table = 'sessions'

    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', index=True)

    expires_datetime = fields.DatetimeField(null=True)

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.expires_datetime = datetime.datetime.now() + datetime.timedelta(days=2)
