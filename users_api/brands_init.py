from users_models.models import CigarettesBrand


async def brands_init(name: str, pack_quantity: int, pack_price: int, model_strength: int):
    brand = CigarettesBrand(name=name, pack_quantity=pack_quantity, pack_price=pack_price,
                            model_strength=model_strength)
    await brand.save()

    return {'id' : str(brand.id)}