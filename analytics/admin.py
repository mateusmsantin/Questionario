# analytics/admin.py
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
# --- ADICIONE ESTES IMPORTS NO TOPO ---
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# --------------------------------------
from questionario.models import Resposta # Importe seus modelos se precisar


# 1. Defina a classe personalizada do AdminSite
class AnalyticsAdminSite(admin.AdminSite):
    site_header = 'Administração do Questionário'
    site_title = 'Admin BI'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # A URL que acessará seu dashboard (/admin/dashboard-bi/)
            path('dashboard-bi/', self.admin_view(self.bi_dashboard_view), name='dashboard_bi'),
        ]
        return custom_urls + urls

    def bi_dashboard_view(self, request):
        # Esta view renderiza o template que você já tem
        context = dict(
            self.each_context(request),
            title='Dashboard BI - Lagoa Mirim',
        )
        return TemplateResponse(request, "admin/bi_dashboard.html", context)

    def get_app_list(self, request):
        """
        Adiciona o link especial ao menu lateral.
        """
        app_list = super().get_app_list(request)
        
        # Adiciona o item ao menu lateral
        app_list.append({
            'name': 'Relatórios e BI',
            'app_label': 'analytics',
            'models': [{
                'name': 'Dashboard Lagoa Mirim',
                'admin_url': '/admin/dashboard-bi/', # URL definida em get_urls
                'view_only': True,
            }],
        })
        return app_list

# 2. Instancie o site personalizado
admin_site = AnalyticsAdminSite(name='analytics_admin')

# --- REGISTROS ---
# Traz de volta os usuários e grupos
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Registre seus modelos do app questionario se necessário
# admin_site.register(Resposta)