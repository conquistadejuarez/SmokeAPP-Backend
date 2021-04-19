from users_models.models import Diseases


async def diseases_init(name=str, description=str, disease_difficulty=int):
    disease = Diseases(name=name,description=description,disease_difficulty=disease_difficulty)

    await disease.save()

    return {'id': str(disease.id)}