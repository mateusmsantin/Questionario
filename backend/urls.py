from django.contrib import admin
from django.urls import path, include

from analytics.views import bi_dashboard
from analytics.admin import admin_site # <--- Importe o site personalizado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin_site.urls), # <--- USE O SEU SITE AQUI
    path('api/', include('questionario.urls')),  # 🔥 TODAS as rotas da API ficam aqui
    path('analytics/', include('analytics.urls')), # API JSON
    path('bi-dashboard/', bi_dashboard, name='bi-dashboard'), # Dashboard Admin
    ]