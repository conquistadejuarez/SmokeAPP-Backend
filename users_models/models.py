import uuid
import tortoise
from tortoise import Tortoise, fields, timezone
from tortoise.models import Model
import json
import datetime


def tz_now():
    return tortoise.timezone.now()


class User(Model):
    class Meta:
        table = 'users'
        unique_together = (('id_tenant', 'username'),)

    id = fields.UUIDField(pk=True)
    id_tenant = fields.UUIDField(index=True)
    username = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    active = fields.BooleanField(null=False, default=True)
    average_per_day = fields.IntField(null=False)
    brand_smoking = fields.ForeignKeyField("models.CigarettesBrand", null=False, index=True, related_name='smokers')
    quit_date = fields.DateField(null=True)

    def __str__(self):
        return 'Welcome back, ' + self.username

    @property
    def days_since_user_quits(self):
        diff = tz_now() - self.quit_date
        return diff.days

    async def calc_money_spend_per_day(self):
        await self.fetch_related('brand_smoking')

        one_cigarette = self.brand_smoking.pack_price / self.brand_smoking.pack_quantity
        spending_per_day = self.average_per_day * one_cigarette
        return spending_per_day

    async def calc_money_not_spend(self):
        money = self.days_since_user_quits * await self.calc_money_spend_per_day()
        return money

    def calc_cigarettes_user_did_not_smoke(self):
        cigarettes = self.days_since_user_quits * self.average_per_day
        return cigarettes


class CigarettesBrand(Model):
    class Meta:
        table = 'cigarettes_brands'

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128, unique=True)
    pack_quantity = fields.IntField()
    pack_price = fields.IntField()
    model_strength = fields.IntField()

    # smokers: fields.ReverseRelation["User"] = fields.ReverseRelation


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
