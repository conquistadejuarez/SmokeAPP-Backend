# from users_models.models import CigarettesBrand

from users_models import models

async def add(name: str, pack_quantity: int, pack_price: int, model_strength: int):

    try:
        brand = models.CigarettesBrand(name=name, pack_quantity=pack_quantity, pack_price=pack_price,
                                model_strength=model_strength)
        await brand.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(brand.id)}

async def get(id_brand):

    b = await models.CigarettesBrand.filter(id=id_brand).get_or_none()

    if not b:
        return False

    return {
        'id': str(b.id),
        'name': b.name
    }

async def get_all():

    return [{'id': str(b.id), 'name': b.name} for b in await models.CigarettesBrand.all().order_by('name')]
