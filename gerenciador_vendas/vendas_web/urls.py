from django.urls import path
from . import views
from .funil_insights import dashboard_funil_insights

app_name = 'vendas_web'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    
    # APIs para dados do dashboard
    path('api/dashboard/data/', views.dashboard_data, name='dashboard_data'),
    path('api/dashboard/charts/', views.dashboard_charts_data, name='dashboard_charts'),
    path('api/dashboard/tables/', views.dashboard_tables_data, name='dashboard_tables'),
    path('api/dashboard/leads/', views.dashboard_leads_data, name='dashboard_leads'),
    path('api/dashboard/prospectos/', views.dashboard_prospectos_data, name='dashboard_prospectos'),
    path('api/dashboard/historico/', views.dashboard_historico_data, name='dashboard_historico'),
    path('api/dashboard/contatos/realtime/', views.dashboard_contatos_realtime, name='dashboard_contatos_realtime'),
    path('api/dashboard/contato/<str:telefone>/historico/', views.dashboard_contato_historico, name='dashboard_contato_historico'),
    
    # API para insights do funil de vendas
    path('api/dashboard/funil/insights/', dashboard_funil_insights, name='dashboard_funil_insights'),
]