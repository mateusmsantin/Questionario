from django.db.models import Avg
from questionario.models import Resposta

def score_geral():
    return Resposta.objects.aggregate(media=Avg('peso'))