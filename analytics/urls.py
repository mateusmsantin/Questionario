# analytics/urls.py
from django.urls import path
from .views import bi_stats, bi_stats_detalhado, export_csv, stats_por_pergunta, visualizar_dashboard

urlpatterns = [
    
    # Rota para VER O GRÁFICO (HTML)
    path('dashboard/', visualizar_dashboard, name='bi-dashboard'),

    # Agora acessível em /analytics/stats/
    path('stats/', bi_stats, name='bi-stats'),  
    
    # Agora acessível em /analytics/detalhado/
    path('detalhado/', bi_stats_detalhado, name='bi-stats-detalhado'),  
    
    # Agora acessível em /analytics/export/
    path('export/', export_csv, name='export-csv'),  
    
    # Agora acessível em /analytics/stats-por-pergunta/
    path('stats-por-pergunta/', stats_por_pergunta, name='stats_por_pergunta'),
]