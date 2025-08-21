from django.urls import path
from . import views
from .funil_insights import dashboard_funil_insights

app_name = 'vendas_web'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('dashboard1/', views.dashboard1, name='dashboard1'),  # Nova rota para o template
    
    # APIs para dados do dashboard
    path('api/dashboard/data/', views.dashboard_data, name='dashboard_data'),
    path('api/dashboard/charts/', views.dashboard_charts_data, name='dashboard_charts'),
    path('api/dashboard/tables/', views.dashboard_tables_data, name='dashboard_tables'),
    path('api/dashboard/leads/', views.dashboard_leads_data, name='dashboard_leads'),
    path('api/dashboard/prospectos/', views.dashboard_prospectos_data, name='dashboard_prospectos'),
    path('api/dashboard/historico/', views.dashboard_historico_data, name='dashboard_historico'),
    path('api/dashboard/contatos/realtime/', views.dashboard_contatos_realtime, name='dashboard_contatos_realtime'),
    path('api/dashboard/contato/<str:telefone>/historico/', views.dashboard_contato_historico, name='dashboard_contato_historico'),
    path('api/dashboard/ultimas-conversoes/', views.dashboard_ultimas_conversoes, name='dashboard_ultimas_conversoes'),  # Nova rota
    
    # APIs para validação de vendas
    path('api/vendas/aprovar/', views.aprovar_venda_api, name='aprovar_venda'),
    path('api/vendas/rejeitar/', views.rejeitar_venda_api, name='rejeitar_venda'),
    
    # API para histórico de contatos
    path('api/historico-contatos/', views.historico_contatos_api, name='historico_contatos'),
    
    # API para insights do funil de vendas
    path('api/dashboard/funil/insights/', dashboard_funil_insights, name='dashboard_funil_insights'),
    
    # Rotas adicionais para navegação
    path('leads/', views.leads_view, name='leads'),
    path('vendas/', views.vendas_view, name='vendas'),
    path('relatorio/leads/', views.relatorio_leads_view, name='relatorio_leads'),
    path('analise/atendimentos/', views.analise_atendimentos_view, name='analise_atendimentos'),
    path('relatorio/conversoes/', views.relatorio_conversoes_view, name='relatorio_conversoes'),

    # APIS simples de registro/update
    path('api/leads/registrar/', views.registrar_lead_api, name='registrar_lead'),
    path('api/leads/atualizar/', views.atualizar_lead_api, name='atualizar_lead'),
    path('api/prospectos/registrar/', views.registrar_prospecto_api, name='registrar_prospecto'),
    path('api/prospectos/atualizar/', views.atualizar_prospecto_api, name='atualizar_prospecto'),
    path('api/historicos/registrar/', views.registrar_historico_api, name='registrar_historico'),
    path('api/historicos/atualizar/', views.atualizar_historico_api, name='atualizar_historico'),
    path('api/verificar-relacionamentos/', views.verificar_relacionamentos_api, name='verificar_relacionamentos'),

    # APIs de consulta (GET)
    path('api/consultar/leads/', views.consultar_leads_api, name='consultar_leads_api'),
    path('api/consultar/historicos/', views.consultar_historicos_api, name='consultar_historicos_api'),
    
    # APIs de consulta de Atendimento (GET)
    path('api/consultar/fluxos/', views.consultar_fluxos_api, name='consultar_fluxos_api'),
    path('api/consultar/questoes/', views.consultar_questoes_api, name='consultar_questoes_api'),
    path('api/consultar/atendimentos/', views.consultar_atendimentos_api, name='consultar_atendimentos_api'),
    path('api/consultar/respostas/', views.consultar_respostas_api, name='consultar_respostas_api'),

    # Documentação da API
    path('api/docs/', views.api_swagger_view, name='api_swagger'),
    path('api/docs/markdown/', views.api_documentation_view, name='api_documentation'),
]