from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from .services.kpis import score_geral
from .services.segmentacoes import media_por_genero, media_por_idade
from .services.distribuicoes import media_por_aba, distribuicao_respostas

from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
import csv  # Para exportar CSV
from questionario.models import Resposta  # Para acessar os dados das respostas
from django.db.models import Count
from questionario.models import Pergunta, Resposta


# CRIE ESTA VIEW
def visualizar_dashboard(request):
    """Renderiza a página HTML com os gráficos"""
    return render(request, 'admin/bi_dashboard.html')

@staff_member_required
def bi_dashboard(request):
    return TemplateResponse(request, "admin/bi_dashboard.html")

def bi_stats(request):
    return JsonResponse({
        "score_geral": score_geral(),
        "media_genero": list(media_por_genero()),
        "media_idade": list(media_por_idade()),
        "media_por_aba": list(media_por_aba()),
        "distribuicao": list(distribuicao_respostas())
    })


@staff_member_required
def export_csv(request):
    """Exporta todos os dados do questionário em CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questionario_dados.csv"'

    writer = csv.writer(response)
    
    # --- VERIFIQUE O CABEÇALHO ---
    writer.writerow([
        'User Email', 'Nome Completo', 'Faixa Etária', 'Gênero', 'Raça',
        'Aba', 'Pergunta', 'Peso' # <--- O 'Peso' deve estar aqui
    ])

    # Busca as respostas com os dados relacionados para performance
    respostas = Resposta.objects.select_related('user', 'pergunta', 'pergunta__aba', 'user__profile').all()

    for r in respostas:
        # --- VERIFIQUE A LINHA DE DADOS ---
        writer.writerow([
            r.user.email,
            r.user.profile.nome_completo,
            r.user.profile.faixa_etaria,
            r.user.profile.genero,
            r.user.profile.raca,
            r.pergunta.aba.nome,
            r.pergunta.texto,
            r.peso # <--- O r.peso deve estar aqui
        ])

    return response


from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from questionario.models import Pergunta, Resposta
from django.db.models import Count

@staff_member_required
def bi_stats_detalhado(request):
    resultado = []
    perguntas = Pergunta.objects.select_related('aba').all()
    
    for p in perguntas:
        distribuicao = (
            Resposta.objects.filter(pergunta=p)
            .values('peso')
            .annotate(total=Count('peso'))
            .order_by('peso')
        )
        distrib = [{'peso': i, 'total': next((d['total'] for d in distribuicao if d['peso']==i),0)} for i in range(1,6)]
        resultado.append({"pergunta": p.texto, "aba": p.aba.nome, "distribuicao": distrib})
    
    return JsonResponse(resultado, safe=False)


from django.db.models import Avg


# views.py
def stats_por_pergunta(request):
    dados = (
        Resposta.objects.values('pergunta__texto') # Verifique se o campo é 'texto' mesmo
        .annotate(media_peso=Avg('peso'))
        .order_by('media_peso')
    )
    # Converta para lista para garantir a serialização
    lista_dados = list(dados)
    #print(lista_dados) # Isso vai aparecer no seu terminal do VS Code para você conferir
    return JsonResponse(lista_dados, safe=False)