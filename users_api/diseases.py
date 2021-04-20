from users_models import models


async def add(name: str, description: str, disease_difficulty: int, time_to_recover: int):
    try:
        disease = models.Diseases(name=name, description=description, disease_difficulty=disease_difficulty,
                                  time_to_recover=time_to_recover)

        await disease.save()
    except Exception as e:
        return {'status': 'error',
                'id_error': 'DATABASE_ERROR',
                'message': str(e)}

    return {
        'status': 'ok',
        'id': str(disease.id),
        'name': disease.name,
        'description': disease.description
    }


async def get(id_disease):
    c = await models.Diseases.filter(id=id_disease).get_or_none()

    if not c:
        return False

    return {
        'id': str(c.id),
        'name': c.name
    }


async def get_all():
    return [{'id': str(c.id)} for c in await models.Diseases.all().order_by('name')]
