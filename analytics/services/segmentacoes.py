from django.db.models import Avg
from questionario.models import Resposta

def media_por_genero():
    return (
        Resposta.objects
        .values('user__profile__genero')
        .annotate(media=Avg('peso'))
    )

def media_por_idade():
    return (
        Resposta.objects
        .values('user__profile__faixa_etaria')
        .annotate(media=Avg('peso'))
    )