from django.urls import path
from . import views
from . import views_api_atendimento
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
    
    # Rotas para cadastro de clientes
    path('cadastro/', views.cadastro_cliente_view, name='cadastro_cliente'),
    path('api/cadastro/cliente/', views.api_cadastro_cliente, name='api_cadastro_cliente'),
    path('api/planos/internet/', views.api_planos_internet, name='api_planos_internet'),
    path('api/vencimentos/', views.api_vencimentos, name='api_vencimentos'),

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
    
    # ========================================================================
    # APIS COMPLETAS DE ATENDIMENTO - CRUD
    # ========================================================================
    
    # APIs de Fluxos de Atendimento
    path('api/fluxos/', views_api_atendimento.consultar_fluxos_api, name='api_fluxos_consultar'),
    path('api/fluxos/criar/', views_api_atendimento.criar_fluxo_api, name='api_fluxos_criar'),
    path('api/fluxos/<int:fluxo_id>/atualizar/', views_api_atendimento.atualizar_fluxo_api, name='api_fluxos_atualizar'),
    path('api/fluxos/<int:fluxo_id>/deletar/', views_api_atendimento.deletar_fluxo_api, name='api_fluxos_deletar'),
    
    # APIs de Questões de Fluxo
    path('api/questoes/', views_api_atendimento.consultar_questoes_api, name='api_questoes_consultar'),
    path('api/questoes/criar/', views_api_atendimento.criar_questao_api, name='api_questoes_criar'),
    path('api/questoes/<int:questao_id>/atualizar/', views_api_atendimento.atualizar_questao_api, name='api_questoes_atualizar'),
    path('api/questoes/<int:questao_id>/deletar/', views_api_atendimento.deletar_questao_api, name='api_questoes_deletar'),
    
    # APIs de Atendimentos de Fluxo
    path('api/atendimentos/', views_api_atendimento.consultar_atendimentos_api, name='api_atendimentos_consultar'),
    path('api/atendimentos/criar/', views_api_atendimento.criar_atendimento_api, name='api_atendimentos_criar'),
    path('api/atendimentos/<int:atendimento_id>/atualizar/', views_api_atendimento.atualizar_atendimento_api, name='api_atendimentos_atualizar'),
    path('api/atendimentos/<int:atendimento_id>/responder/', views_api_atendimento.responder_questao_api, name='api_atendimentos_responder'),
    path('api/atendimentos/<int:atendimento_id>/finalizar/', views_api_atendimento.finalizar_atendimento_api, name='api_atendimentos_finalizar'),
    
    # APIs de Respostas de Questões
    path('api/respostas/', views_api_atendimento.consultar_respostas_api, name='api_respostas_consultar'),
    
    # APIs de Estatísticas
    path('api/atendimento/estatisticas/', views_api_atendimento.estatisticas_atendimento_api, name='api_atendimento_estatisticas'),
    
    # ========================================================================
    # APIS ESPECÍFICAS PARA INTEGRAÇÃO COM N8N
    # ========================================================================
    
    # APIs para gerenciamento de atendimento pelo N8N
    path('api/n8n/atendimento/iniciar/', views_api_atendimento.iniciar_atendimento_n8n, name='api_n8n_iniciar_atendimento'),
    path('api/n8n/atendimento/<int:atendimento_id>/consultar/', views_api_atendimento.consultar_atendimento_n8n, name='api_n8n_consultar_atendimento'),
    path('api/n8n/atendimento/<int:atendimento_id>/responder/', views_api_atendimento.responder_questao_n8n, name='api_n8n_responder_questao'),
    path('api/n8n/atendimento/<int:atendimento_id>/avancar/', views_api_atendimento.avancar_questao_n8n, name='api_n8n_avancar_questao'),
    path('api/n8n/atendimento/<int:atendimento_id>/finalizar/', views_api_atendimento.finalizar_atendimento_n8n, name='api_n8n_finalizar_atendimento'),
    
    # APIs para busca e consulta pelo N8N
    path('api/n8n/lead/buscar/', views_api_atendimento.buscar_lead_por_telefone_n8n, name='api_n8n_buscar_lead'),
    path('api/n8n/lead/criar/', views_api_atendimento.criar_lead_n8n, name='api_n8n_criar_lead'),
    path('api/n8n/fluxos/', views_api_atendimento.listar_fluxos_ativos_n8n, name='api_n8n_listar_fluxos'),
    path('api/n8n/fluxo/<int:fluxo_id>/questao/<int:indice_questao>/', views_api_atendimento.obter_questao_n8n, name='api_n8n_obter_questao'),
    
    # APIs para controle de atendimento pelo N8N
    path('api/n8n/atendimento/<int:atendimento_id>/pausar/', views_api_atendimento.pausar_atendimento_n8n, name='api_n8n_pausar_atendimento'),
    path('api/n8n/atendimento/<int:atendimento_id>/retomar/', views_api_atendimento.retomar_atendimento_n8n, name='api_n8n_retomar_atendimento'),
    
    # Rotas compatíveis antigas (mantidas para compatibilidade)
    path('api/consultar/fluxos/', views_api_atendimento.consultar_fluxos_api, name='consultar_fluxos_api'),
    path('api/consultar/questoes/', views_api_atendimento.consultar_questoes_api, name='consultar_questoes_api'),
    path('api/consultar/atendimentos/', views_api_atendimento.consultar_atendimentos_api, name='consultar_atendimentos_api'),
    path('api/consultar/respostas/', views_api_atendimento.consultar_respostas_api, name='consultar_respostas_api'),

    # APIs de análise de atendimentos
    path('api/analise/atendimentos/data/', views.api_analise_atendimentos_data, name='api_analise_atendimentos_data'),
    path('api/analise/atendimentos/fluxos/', views.api_analise_atendimentos_fluxos, name='api_analise_atendimentos_fluxos'),
    path('api/analise/atendimentos/detalhada/', views.api_analise_detalhada_atendimentos, name='api_analise_detalhada_atendimentos'),
    path('api/jornada/cliente/', views.api_jornada_cliente_completa, name='api_jornada_cliente_completa'),
    path('api/atendimento/tempo-real/', views.api_atendimento_em_tempo_real, name='api_atendimento_em_tempo_real'),

    # Documentação da API
    path('api/docs/', views.api_swagger_view, name='api_swagger'),
    path('api/docs/markdown/', views.api_documentation_view, name='api_documentation'),
    path('api/docs/n8n/', views.n8n_guide_view, name='n8n_guide'),
]