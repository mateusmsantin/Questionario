from django.db.models import Avg, Count
from questionario.models import Resposta

def media_por_aba():
    return (
        Resposta.objects
        .values('pergunta__aba__nome')
        .annotate(media=Avg('peso'))
    )

def distribuicao_respostas():
    return (
        Resposta.objects
        .values('peso')
        .annotate(total=Count('id'))
        .order_by('peso')
    )