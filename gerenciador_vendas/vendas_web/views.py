from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
import json
from .models import LeadProspecto, Prospecto, HistoricoContato, ConfiguracaoSistema, LogSistema


# Utilitários simples para as APIs de registro/atualização
def _parse_json_request(request):
    try:
        body = request.body.decode('utf-8') if isinstance(request.body, (bytes, bytearray)) else request.body
        return json.loads(body or '{}')
    except Exception:
        return None


def _model_field_names(model_cls):
    # Campos concretos (exclui M2M e reversos)
    field_names = []
    for f in model_cls._meta.get_fields():
        if getattr(f, 'many_to_many', False) or getattr(f, 'one_to_many', False):
            continue
        if hasattr(f, 'attname'):
            field_names.append(f.name)
    return set(field_names)


def _serialize_instance(instance):
    from django.forms.models import model_to_dict
    from decimal import Decimal
    data = model_to_dict(instance)
    for key, value in list(data.items()):
        if isinstance(value, Decimal):
            data[key] = float(value)
        elif isinstance(value, datetime):
            data[key] = value.isoformat()
    # Campos DateTime auto que podem não estar em model_to_dict
    for auto_dt in ['data_cadastro', 'data_atualizacao', 'data_criacao', 'data_processamento', 'data_inicio_processamento', 'data_fim_processamento', 'data_hora_contato', 'data_conversao_lead', 'data_conversao_venda']:
        if hasattr(instance, auto_dt):
            val = getattr(instance, auto_dt)
            if isinstance(val, datetime):
                data[auto_dt] = val.isoformat()
    # Campos de choices: adiciona display quando existir
    for display_field, getter in [
        ('status_api_display', 'get_status_api_display'),
        ('origem_display', 'get_origem_display'),
        ('status_display', 'get_status_display'),
        ('origem_contato_display', 'get_origem_contato_display')
    ]:
        if hasattr(instance, getter):
            try:
                data[display_field] = getattr(instance, getter)()
            except Exception:
                pass
    return data


def _resolve_fk(model_cls, field_name, value):
    # Resolve ids para FKs simples quando o payload vem com inteiro
    if value is None:
        return None
    if model_cls is Prospecto and field_name in ['lead', 'lead_id']:
        return LeadProspecto.objects.get(id=value) if value else None
    if model_cls is HistoricoContato and field_name in ['lead', 'lead_id']:
        return LeadProspecto.objects.get(id=value) if value else None
    return value


def _apply_updates(instance, updates):
    fields = _model_field_names(type(instance))
    for key, value in updates.items():
        if key in ['id', 'pk']:
            continue
        if key not in fields and not key.endswith('_id'):
            continue
        try:
            resolved_value = _resolve_fk(type(instance), key, value)
            setattr(instance, key, resolved_value)
        except LeadProspecto.DoesNotExist:
            raise ValueError('Lead relacionado não encontrado')
    instance.save()
    return instance


@csrf_exempt
def registrar_lead_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    required = ['nome_razaosocial', 'telefone']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'error': f'Campos obrigatórios ausentes: {", ".join(missing)}'}, status=400)
    try:
        allowed = _model_field_names(LeadProspecto)
        payload = {k: v for k, v in data.items() if k in allowed}
        lead = LeadProspecto.objects.create(**payload)
        return JsonResponse({'success': True, 'id': lead.id, 'lead': _serialize_instance(lead)}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def atualizar_lead_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    termo = data.get('termo_busca')
    busca = data.get('busca')
    if not termo or busca is None:
        return JsonResponse({'error': 'Parâmetros obrigatórios: termo_busca e busca'}, status=400)
    try:
        qs = LeadProspecto.objects.filter(**{termo: busca})
    except Exception:
        return JsonResponse({'error': 'termo_busca inválido para LeadProspecto'}, status=400)
    count = qs.count()
    if count == 0:
        return JsonResponse({'error': 'Registro não encontrado'}, status=404)
    if count > 1:
        return JsonResponse({'error': f'Múltiplos registros encontrados ({count}). Refine a busca.'}, status=400)
    lead = qs.first()
    updates = {k: v for k, v in data.items() if k not in ['termo_busca', 'busca']}
    if not updates:
        return JsonResponse({'error': 'Nenhum campo para atualizar informado'}, status=400)
    try:
        _apply_updates(lead, updates)
        return JsonResponse({'success': True, 'id': lead.id, 'lead': _serialize_instance(lead)})
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def registrar_prospecto_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    required = ['nome_prospecto']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'error': f'Campos obrigatórios ausentes: {", ".join(missing)}'}, status=400)
    try:
        allowed = _model_field_names(Prospecto)
        payload = {k: v for k, v in data.items() if k in allowed}
        # Resolver lead se vier como id simples
        if 'lead' in data and isinstance(data['lead'], int):
            payload['lead'] = LeadProspecto.objects.get(id=data['lead'])
        if 'lead_id' in data and isinstance(data['lead_id'], int):
            payload['lead_id'] = data['lead_id']
        prospecto = Prospecto.objects.create(**payload)
        return JsonResponse({'success': True, 'id': prospecto.id, 'prospecto': _serialize_instance(prospecto)}, status=201)
    except LeadProspecto.DoesNotExist:
        return JsonResponse({'error': 'Lead informado não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def atualizar_prospecto_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    termo = data.get('termo_busca')
    busca = data.get('busca')
    if not termo or busca is None:
        return JsonResponse({'error': 'Parâmetros obrigatórios: termo_busca e busca'}, status=400)
    try:
        qs = Prospecto.objects.filter(**{termo: busca})
    except Exception:
        return JsonResponse({'error': 'termo_busca inválido para Prospecto'}, status=400)
    count = qs.count()
    if count == 0:
        return JsonResponse({'error': 'Registro não encontrado'}, status=404)
    if count > 1:
        return JsonResponse({'error': f'Múltiplos registros encontrados ({count}). Refine a busca.'}, status=400)
    prospecto = qs.first()
    updates = {k: v for k, v in data.items() if k not in ['termo_busca', 'busca']}
    if not updates:
        return JsonResponse({'error': 'Nenhum campo para atualizar informado'}, status=400)
    try:
        _apply_updates(prospecto, updates)
        return JsonResponse({'success': True, 'id': prospecto.id, 'prospecto': _serialize_instance(prospecto)})
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def registrar_historico_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    required = ['telefone', 'status']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'error': f'Campos obrigatórios ausentes: {", ".join(missing)}'}, status=400)
    try:
        allowed = _model_field_names(HistoricoContato)
        payload = {k: v for k, v in data.items() if k in allowed}
        if 'lead' in data and isinstance(data['lead'], int):
            payload['lead'] = LeadProspecto.objects.get(id=data['lead'])
        if 'lead_id' in data and isinstance(data['lead_id'], int):
            payload['lead_id'] = data['lead_id']
        contato = HistoricoContato.objects.create(**payload)
        return JsonResponse({'success': True, 'id': contato.id, 'historico': _serialize_instance(contato)}, status=201)
    except LeadProspecto.DoesNotExist:
        return JsonResponse({'error': 'Lead informado não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def atualizar_historico_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    data = _parse_json_request(request)
    if data is None:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    termo = data.get('termo_busca')
    busca = data.get('busca')
    if not termo or busca is None:
        return JsonResponse({'error': 'Parâmetros obrigatórios: termo_busca e busca'}, status=400)
    try:
        qs = HistoricoContato.objects.filter(**{termo: busca})
    except Exception:
        return JsonResponse({'error': 'termo_busca inválido para Histórico de Contato'}, status=400)
    count = qs.count()
    if count == 0:
        return JsonResponse({'error': 'Registro não encontrado'}, status=404)
    if count > 1:
        return JsonResponse({'error': f'Múltiplos registros encontrados ({count}). Refine a busca.'}, status=400)
    contato = qs.first()
    updates = {k: v for k, v in data.items() if k not in ['termo_busca', 'busca']}
    if not updates:
        return JsonResponse({'error': 'Nenhum campo para atualizar informado'}, status=400)
    try:
        _apply_updates(contato, updates)
        return JsonResponse({'success': True, 'id': contato.id, 'historico': _serialize_instance(contato)})
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def dashboard_view(request):
    """View principal do dashboard"""
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'vendas_web/new_dash.html', context)

def dashboard1(request):
    """View alternativa do dashboard - alias para dashboard_view"""
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'vendas_web/new_dash.html', context)

def leads_view(request):
    """View para a página de gerenciamento de leads"""
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'vendas_web/leads.html', context)

def relatorio_leads_view(request):
    """View para a página de relatórios de leads"""
    # Por enquanto redireciona para a página de leads
    # Você pode criar um template específico para relatórios depois
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'vendas_web/leads.html', context)

def vendas_view(request):
    """View para a página de gerenciamento de vendas (prospectos)"""
    context = {
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'vendas_web/vendas.html', context)


def dashboard_data(request):
    """API para dados principais do dashboard"""
    try:
        # Cálculo das métricas conforme especificação:
        # 1. ATENDIMENTOS = Histórico de contatos finalizados
        atendimentos = HistoricoContato.objects.filter(
            status__in=['fluxo_finalizado', 'transferido_humano', 'convertido_lead', 'venda_confirmada']
        ).count()
        
        # 2. LEADS = Quantidade de LeadProspecto ativos
        leads = LeadProspecto.objects.filter(ativo=True).count()
        
        # 3. PROSPECTOS = Quantidade de Prospectos
        prospectos = Prospecto.objects.count()
        
        # 4. VENDAS = Prospectos com status 'validacao_aprovada'
        vendas = Prospecto.objects.filter(status='validacao_aprovada').count()
        
        # Calcular métricas do período anterior para comparação (últimos 30 dias vs 30 dias anteriores)
        hoje = timezone.now()
        inicio_periodo_atual = hoje - timedelta(days=30)
        inicio_periodo_anterior = hoje - timedelta(days=60)
        fim_periodo_anterior = hoje - timedelta(days=30)
        
        # Métricas do período anterior
        atendimentos_anterior = HistoricoContato.objects.filter(
            status__in=['fluxo_finalizado', 'transferido_humano', 'convertido_lead', 'venda_confirmada'],
            data_hora_contato__gte=inicio_periodo_anterior,
            data_hora_contato__lt=fim_periodo_anterior
        ).count()
        
        leads_anterior = LeadProspecto.objects.filter(
            ativo=True,
            data_cadastro__gte=inicio_periodo_anterior,
            data_cadastro__lt=fim_periodo_anterior
        ).count()
        
        prospectos_anterior = Prospecto.objects.filter(
            data_criacao__gte=inicio_periodo_anterior,
            data_criacao__lt=fim_periodo_anterior
        ).count()
        
        vendas_anterior = Prospecto.objects.filter(
            status='validacao_aprovada',
            data_criacao__gte=inicio_periodo_anterior,
            data_criacao__lt=fim_periodo_anterior
        ).count()
        
        # Calcular diferenças e variações percentuais
        def calcular_variacao(atual, anterior):
            if anterior == 0:
                if atual > 0:
                    return "+100.0%", atual
                else:
                    return "0.0%", 0
            else:
                variacao = ((atual - anterior) / anterior) * 100
                sinal = "+" if variacao >= 0 else ""
                return f"{sinal}{variacao:.1f}%", atual - anterior
        
        atendimentos_variacao, atendimentos_diff = calcular_variacao(atendimentos, atendimentos_anterior)
        leads_variacao, leads_diff = calcular_variacao(leads, leads_anterior)
        prospectos_variacao, prospectos_diff = calcular_variacao(prospectos, prospectos_anterior)
        vendas_variacao, vendas_diff = calcular_variacao(vendas, vendas_anterior)
        
        # Calcular taxas de conversão entre as etapas
        taxa_atendimento_lead = f"{(leads/atendimentos*100):.2f}%" if atendimentos > 0 else "0.00%"
        taxa_lead_prospecto = f"{(prospectos/leads*100):.2f}%" if leads > 0 else "0.00%"
        taxa_prospecto_venda = f"{(vendas/prospectos*100):.2f}%" if prospectos > 0 else "0.00%"
        
        data = {
            'stats': {
                # Métricas principais conforme especificação
                'atendimentos': atendimentos,
                'atendimentos_variacao': atendimentos_variacao,
                'atendimentos_diff': atendimentos_diff,
                
                'leads': leads,
                'leads_variacao': leads_variacao,
                'leads_diff': leads_diff,
                
                'prospectos': prospectos,
                'prospectos_variacao': prospectos_variacao,
                'prospectos_diff': prospectos_diff,
                
                'vendas': vendas,
                'vendas_variacao': vendas_variacao,
                'vendas_diff': vendas_diff,
                
                # Taxas de conversão para as setas
                'taxa_atendimento_lead': taxa_atendimento_lead,
                'taxa_lead_prospecto': taxa_lead_prospecto,
                'taxa_prospecto_venda': taxa_prospecto_venda
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_charts_data(request):
    """API para dados dos gráficos - Evolução dos últimos 7 dias"""
    try:
        # Função auxiliar para gerar dados dos últimos 7 dias
        def gerar_ultimos_7_dias(query_func):
            dados = []
            for i in range(7):
                data = timezone.now().date() - timedelta(days=i)
                count = query_func(data)
                dados.append({
                    'date': data.strftime('%d/%m'),
                    'count': count
                })
            dados.reverse()
            return dados
        
        # 1. ATENDIMENTOS dos últimos 7 dias (contatos finalizados)
        def count_atendimentos(data):
            return HistoricoContato.objects.filter(
                data_hora_contato__date=data,
                status__in=['fluxo_finalizado', 'transferido_humano', 'convertido_lead', 'venda_confirmada']
            ).count()
        
        atendimentosUltimos7Dias = gerar_ultimos_7_dias(count_atendimentos)
        
        # 2. LEADS dos últimos 7 dias
        def count_leads(data):
            return LeadProspecto.objects.filter(
                data_cadastro__date=data,
                ativo=True
            ).count()
        
        leadsUltimos7Dias = gerar_ultimos_7_dias(count_leads)
        
        # 3. PROSPECTOS dos últimos 7 dias
        def count_prospectos(data):
            return Prospecto.objects.filter(
                data_criacao__date=data
            ).count()
        
        prospectosUltimos7Dias = gerar_ultimos_7_dias(count_prospectos)
        
        # 4. VENDAS dos últimos 7 dias
        def count_vendas(data):
            return HistoricoContato.objects.filter(
                data_conversao_venda__date=data,
                converteu_venda=True
            ).count()
        
        vendasUltimos7Dias = gerar_ultimos_7_dias(count_vendas)
        
        data = {
            # Dados para o gráfico de tendências (padrão será LEADS)
            'leadsUltimos7Dias': leadsUltimos7Dias,
            
            # Dados para troca dinâmica no frontend
            'atendimentosUltimos7Dias': atendimentosUltimos7Dias,
            'prospectosUltimos7Dias': prospectosUltimos7Dias,
            'vendasUltimos7Dias': vendasUltimos7Dias
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_tables_data(request):
    """API para dados das tabelas"""
    try:
        # Top empresas
        top_empresas = LeadProspecto.objects.filter(
            ativo=True,
            empresa__isnull=False
        ).exclude(empresa='').values('empresa').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Top origens
        top_origens = LeadProspecto.objects.filter(
            ativo=True
        ).values('origem').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        data = {
            'topEmpresas': list(top_empresas),
            'topOrigens': list(top_origens)
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_leads_data(request):
    """API para dados dos leads"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = 20
        search = request.GET.get('search', '')
        origem_filter = request.GET.get('origem', '')
        status_filter = request.GET.get('status', '')
        ativo_filter = request.GET.get('ativo', '')
        lead_id = request.GET.get('id', '')
        
        leads_query = LeadProspecto.objects.all()
        
        # Filtro por ID específico (para modal de detalhes)
        if lead_id:
            leads_query = leads_query.filter(id=lead_id)
        else:
            # Filtros normais
            if search:
                leads_query = leads_query.filter(
                    Q(nome_razaosocial__icontains=search) |
                    Q(email__icontains=search) |
                    Q(telefone__icontains=search) |
                    Q(empresa__icontains=search) |
                    Q(cpf_cnpj__icontains=search) |
                    Q(id_hubsoft__icontains=search)
                )
            
            if origem_filter:
                leads_query = leads_query.filter(origem=origem_filter)
            
            if status_filter:
                leads_query = leads_query.filter(status_api=status_filter)
            
            if ativo_filter:
                leads_query = leads_query.filter(ativo=(ativo_filter.lower() == 'true'))
        
        total = leads_query.count()
        start = (page - 1) * per_page
        end = start + per_page
        
        leads = leads_query.order_by('-data_cadastro')[start:end]
        
        leads_data = []
        for lead in leads:
            leads_data.append({
                'id': lead.id,
                'nome_razaosocial': lead.nome_razaosocial,
                'email': lead.email,
                'telefone': lead.telefone,
                'id_hubsoft': lead.id_hubsoft,
                'valor': lead.get_valor_formatado(),
                'empresa': lead.empresa or '-',
                'origem': lead.get_origem_display(),
                'data_cadastro': lead.data_cadastro.strftime('%d/%m/%Y %H:%M'),
                'status_api': lead.get_status_api_display(),
                'ativo': lead.ativo,
                'cpf_cnpj': lead.cpf_cnpj or '-',
                'endereco': lead.endereco or '-',
                'cidade': lead.cidade or '-',
                'estado': lead.estado or '-',
                'cep': lead.cep or '-',
                'observacoes': lead.observacoes or '-',
                'data_atualizacao': lead.data_atualizacao.strftime('%d/%m/%Y %H:%M')
            })
        
        # Choices para filtros
        origem_choices = [
            {'value': choice[0], 'label': choice[1]}
            for choice in LeadProspecto.ORIGEM_CHOICES
        ]
        
        status_choices = [
            {'value': choice[0], 'label': choice[1]}
            for choice in LeadProspecto.STATUS_API_CHOICES
        ]
        
        data = {
            'leads': leads_data,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'origemChoices': origem_choices,
            'statusChoices': status_choices
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_prospectos_data(request):
    """API para dados dos prospectos"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = 20
        search = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        prioridade_filter = request.GET.get('prioridade', '')
        prospecto_id = request.GET.get('id', '')
        
        prospectos_query = Prospecto.objects.select_related('lead')
        
        # Filtro por ID específico (para modal de detalhes)
        if prospecto_id:
            prospectos_query = prospectos_query.filter(id=prospecto_id)
        else:
            # Filtros normais
            if search:
                prospectos_query = prospectos_query.filter(
                    Q(nome_prospecto__icontains=search) |
                    Q(id_prospecto_hubsoft__icontains=search) |
                    Q(lead__nome_razaosocial__icontains=search)
                )
            
            if status_filter:
                prospectos_query = prospectos_query.filter(status=status_filter)
            
            if prioridade_filter:
                prospectos_query = prospectos_query.filter(prioridade=prioridade_filter)
        
        total = prospectos_query.count()
        start = (page - 1) * per_page
        end = start + per_page
        
        prospectos = prospectos_query.order_by('-data_criacao')[start:end]
        
        prospectos_data = []
        for prospecto in prospectos:
            lead_data = None
            if prospecto.lead:
                lead_data = {
                    'id': prospecto.lead.id,
                    'nome_razaosocial': prospecto.lead.nome_razaosocial,
                    'email': prospecto.lead.email,
                    'telefone': prospecto.lead.telefone,
                    'empresa': prospecto.lead.empresa,
                    'valor': f"R$ {prospecto.lead.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if prospecto.lead.valor else 'R$ 0,00'
                }
            
            prospectos_data.append({
                'id': prospecto.id,
                'nome_prospecto': prospecto.nome_prospecto,
                'lead': lead_data,
                'id_prospecto_hubsoft': prospecto.id_prospecto_hubsoft or '-',
                'status': prospecto.status,  # Status raw para o frontend
                'status_display': prospecto.get_status_display(),
                'prioridade': prospecto.prioridade,
                'score_conversao': float(prospecto.score_conversao) if prospecto.score_conversao else None,
                'data_criacao': prospecto.data_criacao.strftime('%d/%m/%Y %H:%M'),
                'data_processamento': prospecto.data_processamento.strftime('%d/%m/%Y %H:%M') if prospecto.data_processamento else '-',
                # Campos técnicos (apenas para admin/debug)
                'tentativas_processamento': prospecto.tentativas_processamento,
                'tempo_processamento': prospecto.get_tempo_processamento_formatado(),
                'erro_processamento': prospecto.erro_processamento[:50] + '...' if prospecto.erro_processamento and len(prospecto.erro_processamento) > 50 else (prospecto.erro_processamento or '-'),
                'dados_processamento': prospecto.dados_processamento,
                'resultado_processamento': prospecto.resultado_processamento
            })
        
        # Status choices para o filtro
        status_choices = [
            {'value': choice[0], 'label': choice[1]}
            for choice in Prospecto.STATUS_CHOICES
        ]
        
        data = {
            'prospectos': prospectos_data,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'statusChoices': status_choices
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_historico_data(request):
    """API para dados do histórico de contatos"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = 20
        search = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        sucesso_filter = request.GET.get('sucesso', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        contato_id = request.GET.get('id', '')
        
        historico_query = HistoricoContato.objects.select_related('lead')
        
        # Filtro por ID específico (para modal de detalhes)
        if contato_id:
            historico_query = historico_query.filter(id=contato_id)
        else:
            # Filtros normais
            if search:
                historico_query = historico_query.filter(
                    Q(telefone__icontains=search) |
                    Q(nome_contato__icontains=search) |
                    Q(lead__nome_razaosocial__icontains=search)
                )
            
            if status_filter:
                historico_query = historico_query.filter(status=status_filter)
            
            if sucesso_filter:
                historico_query = historico_query.filter(sucesso=(sucesso_filter.lower() == 'true'))
            
            if data_inicio:
                try:
                    data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    historico_query = historico_query.filter(data_hora_contato__date__gte=data_inicio_obj)
                except ValueError:
                    pass
            
            if data_fim:
                try:
                    data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                    historico_query = historico_query.filter(data_hora_contato__date__lte=data_fim_obj)
                except ValueError:
                    pass
        
        total = historico_query.count()
        start = (page - 1) * per_page
        end = start + per_page
        
        historico = historico_query.order_by('-data_hora_contato')[start:end]
        
        historico_data = []
        for contato in historico:
            historico_data.append({
                'id': contato.id,
                'telefone': contato.telefone,
                'nome_contato': contato.nome_contato or '-',
                'lead_relacionado': contato.lead.nome_razaosocial if contato.lead else None,
                'status': contato.get_status_display(),
                'status_color': contato.get_status_display_color(),
                'data_hora_contato': contato.data_hora_contato.strftime('%d/%m/%Y %H:%M'),
                'duracao_formatada': contato.get_duracao_formatada(),
                'sucesso': contato.sucesso,
                'converteu_lead': contato.converteu_lead,
                'converteu_venda': contato.converteu_venda,
                'valor_venda': contato.get_valor_venda_formatado() if contato.valor_venda else None,
                'data_conversao_lead': contato.data_conversao_lead.strftime('%d/%m/%Y %H:%M') if contato.data_conversao_lead else None,
                'data_conversao_venda': contato.data_conversao_venda.strftime('%d/%m/%Y %H:%M') if contato.data_conversao_venda else None,
                'origem_contato': contato.get_origem_contato_display() if contato.origem_contato else None,
                'transcricao': contato.transcricao or '-',
                'observacoes': contato.observacoes or '-',
                'ip_origem': contato.ip_origem or '-',
                'tempo_relativo': contato.get_tempo_relativo(),
                'dados_extras': contato.dados_extras,
                'bem_sucedido': contato.is_contato_bem_sucedido(),
                'conversao_completa': contato.is_conversao_completa()
            })
        
        # Status choices para o filtro
        status_choices = [
            {'value': choice[0], 'label': choice[1]}
            for choice in HistoricoContato.STATUS_CHOICES
        ]
        
        data = {
            'historico': historico_data,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'statusChoices': status_choices
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_contatos_realtime(request):
    """API para contatos em tempo real"""
    try:
        # Últimos 10 contatos
        contatos_recentes = HistoricoContato.objects.order_by('-data_hora_contato')[:10]
        
        contatos_data = []
        for contato in contatos_recentes:
            contatos_data.append({
                'id': contato.id,
                'telefone': contato.telefone,
                'nome_contato': contato.nome_contato or 'Não identificado',
                'status': contato.get_status_display(),
                'data_hora_contato': contato.data_hora_contato.strftime('%d/%m/%Y %H:%M:%S'),
                'tempo_relativo': contato.get_tempo_relativo(),
                'sucesso': contato.sucesso
            })
        
        data = {
            'contatos': contatos_data
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_contato_historico(request, telefone):
    """API para histórico detalhado de um telefone"""
    try:
        # Buscar todos os contatos deste telefone
        contatos = HistoricoContato.objects.filter(
            telefone=telefone
        ).order_by('-data_hora_contato')
        
        # Estatísticas básicas do telefone
        total_contatos = contatos.count()
        contatos_sucesso = contatos.filter(sucesso=True).count()
        contatos_finalizados = contatos.filter(status='fluxo_finalizado').count()
        contatos_transferidos = contatos.filter(status='transferido_humano').count()
        contatos_inicializados = contatos.filter(status='fluxo_inicializado').count()
        contatos_convertidos_lead = contatos.filter(converteu_lead=True).count()
        contatos_vendas = contatos.filter(converteu_venda=True).count()
        duracao_total = sum([c.duracao_segundos or 0 for c in contatos])
        
        # Calcular taxas
        taxa_sucesso = (contatos_sucesso / total_contatos * 100) if total_contatos > 0 else 0
        taxa_finalizacao = ((contatos_finalizados + contatos_transferidos) / total_contatos * 100) if total_contatos > 0 else 0
        taxa_conversao_lead = (contatos_convertidos_lead / total_contatos * 100) if total_contatos > 0 else 0
        taxa_conversao_venda = (contatos_vendas / contatos_convertidos_lead * 100) if contatos_convertidos_lead > 0 else 0
        
        # Último contato
        ultimo_contato = contatos.first()
        ultimo_contato_data = ultimo_contato.data_hora_contato.strftime('%d/%m/%Y %H:%M') if ultimo_contato else None
        
        # Valor total das vendas
        valor_total_vendas = contatos.filter(converteu_venda=True).aggregate(
            total=Sum('valor_venda')
        )['total'] or 0
        
        # Timeline dos contatos com informações detalhadas
        timeline_data = []
        for contato in contatos:
            timeline_data.append({
                'id': contato.id,
                'data_hora_contato': contato.data_hora_contato.strftime('%d/%m/%Y %H:%M:%S'),
                'status': contato.get_status_display(),
                'nome_contato': contato.nome_contato or 'Não identificado',
                'duracao_formatada': contato.get_duracao_formatada(),
                'sucesso': contato.sucesso,
                'converteu_lead': contato.converteu_lead,
                'converteu_venda': contato.converteu_venda,
                'valor_venda': contato.get_valor_venda_formatado() if contato.valor_venda else None,
                'observacoes': contato.observacoes or '',
                'transcricao': contato.transcricao or '',
                'tempo_relativo': contato.get_tempo_relativo(),
                'origem_contato': contato.get_origem_contato_display() if contato.origem_contato else None
            })
        
        data = {
            'telefone': telefone,
            'total': total_contatos,
            'ultimo_contato': ultimo_contato_data,
            'taxa_sucesso': f"{taxa_sucesso:.1f}%",
            'estatisticas': {
                'total_contatos': total_contatos,
                'contatos_sucesso': contatos_sucesso,
                'contatos_finalizados': contatos_finalizados,
                'contatos_transferidos': contatos_transferidos,
                'contatos_inicializados': contatos_inicializados,
                'contatos_convertidos_lead': contatos_convertidos_lead,
                'contatos_vendas': contatos_vendas,
                'duracao_total_minutos': duracao_total // 60 if duracao_total else 0,
                'taxa_sucesso': taxa_sucesso,
                'taxa_finalizacao': taxa_finalizacao,
                'taxa_conversao_lead': taxa_conversao_lead,
                'taxa_conversao_venda': taxa_conversao_venda,
                'valor_total_vendas': valor_total_vendas,
                'valor_total_vendas_formatado': f"R$ {valor_total_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            },
            'historico': timeline_data,
            'timeline': timeline_data
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_ultimas_conversoes(request):
    """API para últimas conversões de leads"""
    try:
        # Buscar últimos leads cadastrados (conversões)
        limite = int(request.GET.get('limite', 6))  # Padrão 6 como no template
        
        ultimos_leads = LeadProspecto.objects.filter(
            ativo=True
        ).order_by('-data_cadastro')[:limite]
        
        conversoes = []
        for lead in ultimos_leads:
            conversoes.append({
                'nome': lead.nome_razaosocial,
                'empresa': lead.empresa or '-',
                'origem': lead.get_origem_display(),
                'data_cadastro': lead.data_cadastro.strftime('%d/%m/%Y às %H:%M'),
                'valor': lead.get_valor_formatado(),
                'telefone': lead.telefone,
                'email': lead.email or '-',
                'status': lead.get_status_api_display()
            })
        
        data = {
            'conversoes': conversoes
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def aprovar_venda_api(request):
    """API para aprovar uma venda"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        prospecto_id = data.get('prospecto_id')
        observacoes = data.get('observacoes', '')
        
        if not prospecto_id:
            return JsonResponse({'error': 'ID do prospecto é obrigatório'}, status=400)
        
        if not observacoes.strip():
            return JsonResponse({'error': 'Observações da validação são obrigatórias'}, status=400)
        
        # Buscar prospecto
        prospecto = Prospecto.objects.get(id=prospecto_id)
        
        # Verificar se pode ser aprovado
        if prospecto.status not in ['processado', 'aguardando_validacao']:
            return JsonResponse({'error': 'Prospecto não pode ser aprovado neste status'}, status=400)
        
        # Atualizar status
        prospecto.status = 'validacao_aprovada'
        prospecto.save()
        
        # Criar registro de validação (pode adicionar uma tabela específica depois)
        # Por enquanto, armazenar nos dados de processamento
        usuario_validacao = f"{request.user.username}" if request.user.is_authenticated else "Sistema"
        if request.user.is_authenticated and (request.user.first_name or request.user.last_name):
            usuario_validacao = f"{request.user.first_name} {request.user.last_name}".strip()
        
        validacao_data = {
            'observacoes': observacoes,
            'data_validacao': timezone.now().isoformat(),
            'status_validacao': 'aprovada',
            'usuario_validacao': usuario_validacao
        }
        
        if prospecto.resultado_processamento:
            prospecto.resultado_processamento.update(validacao_data)
        else:
            prospecto.resultado_processamento = validacao_data
        
        prospecto.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Venda aprovada com sucesso',
            'prospecto_id': prospecto.id,
            'novo_status': prospecto.status
        })
        
    except Prospecto.DoesNotExist:
        return JsonResponse({'error': 'Prospecto não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)


def rejeitar_venda_api(request):
    """API para rejeitar uma venda"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        prospecto_id = data.get('prospecto_id')
        motivo_rejeicao = data.get('motivo_rejeicao', '')
        
        if not prospecto_id:
            return JsonResponse({'error': 'ID do prospecto é obrigatório'}, status=400)
        
        if not motivo_rejeicao.strip():
            return JsonResponse({'error': 'Motivo da rejeição é obrigatório'}, status=400)
        
        # Buscar prospecto
        prospecto = Prospecto.objects.get(id=prospecto_id)
        
        # Verificar se pode ser rejeitado
        if prospecto.status not in ['processado', 'aguardando_validacao']:
            return JsonResponse({'error': 'Prospecto não pode ser rejeitado neste status'}, status=400)
        
        # Atualizar status
        prospecto.status = 'validacao_rejeitada'
        prospecto.save()
        
        # Criar registro de rejeição
        usuario_validacao = f"{request.user.username}" if request.user.is_authenticated else "Sistema"
        if request.user.is_authenticated and (request.user.first_name or request.user.last_name):
            usuario_validacao = f"{request.user.first_name} {request.user.last_name}".strip()
        
        rejeicao_data = {
            'motivo_rejeicao': motivo_rejeicao,
            'data_validacao': timezone.now().isoformat(),
            'status_validacao': 'rejeitada',
            'usuario_validacao': usuario_validacao
        }
        
        if prospecto.resultado_processamento:
            prospecto.resultado_processamento.update(rejeicao_data)
        else:
            prospecto.resultado_processamento = rejeicao_data
        
        prospecto.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Venda rejeitada',
            'prospecto_id': prospecto.id,
            'novo_status': prospecto.status
        })
        
    except Prospecto.DoesNotExist:
        return JsonResponse({'error': 'Prospecto não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)


def historico_contatos_api(request):
    """API para buscar histórico de contatos por lead ID ou telefone"""
    try:
        lead_id = request.GET.get('lead_id')
        prospecto_id = request.GET.get('prospecto_id')
        telefone = request.GET.get('telefone')
        
        if not lead_id and not prospecto_id and not telefone:
            return JsonResponse({'error': 'É necessário fornecer lead_id, prospecto_id ou telefone'}, status=400)
        
        historicos_query = HistoricoContato.objects.select_related('lead')
        
        # Buscar por lead_id
        if lead_id:
            try:
                lead = LeadProspecto.objects.get(id=lead_id)
                historicos_query = historicos_query.filter(
                    Q(lead_id=lead_id) | Q(telefone=lead.telefone)
                )
            except LeadProspecto.DoesNotExist:
                return JsonResponse({'error': 'Lead não encontrado'}, status=404)
        
        # Buscar por prospecto_id
        elif prospecto_id:
            try:
                prospecto = Prospecto.objects.get(id=prospecto_id)
                if prospecto.lead:
                    historicos_query = historicos_query.filter(
                        Q(lead_id=prospecto.lead.id) | Q(telefone=prospecto.lead.telefone)
                    )
                else:
                    # Se o prospecto não tem lead, buscar por nome semelhante (se houver telefone)
                    return JsonResponse({'historicos': [], 'total': 0, 'info': 'Prospecto sem lead associado'})
            except Prospecto.DoesNotExist:
                return JsonResponse({'error': 'Prospecto não encontrado'}, status=404)
        
        # Buscar por telefone
        elif telefone:
            historicos_query = historicos_query.filter(telefone=telefone)
        
        # Ordenar por data mais recente
        historicos = historicos_query.order_by('-data_hora_contato')[:50]  # Limitar a 50 registros mais recentes
        
        historicos_data = []
        for historico in historicos:
            # Formatar duração
            duracao_formatada = 'N/A'
            if historico.duracao_segundos:
                minutos = historico.duracao_segundos // 60
                segundos = historico.duracao_segundos % 60
                duracao_formatada = f"{minutos}m {segundos}s" if minutos > 0 else f"{segundos}s"
            
            # Status formatado
            status_info = {
                'status': historico.status,
                'display': historico.get_status_display(),
                'categoria': get_status_categoria(historico.status)
            }
            
            historico_item = {
                'id': historico.id,
                'data_hora': historico.data_hora_contato.strftime('%d/%m/%Y %H:%M:%S'),
                'status': status_info,
                'telefone': historico.telefone,
                'nome_contato': historico.nome_contato or 'Não identificado',
                'duracao': duracao_formatada,
                'duracao_segundos': historico.duracao_segundos,
                'transcricao': historico.transcricao[:200] + '...' if historico.transcricao and len(historico.transcricao) > 200 else (historico.transcricao or ''),
                'observacoes': historico.observacoes or '',
                'converteu_lead': historico.converteu_lead,
                'converteu_venda': historico.converteu_venda,
                'lead': {
                    'id': historico.lead.id,
                    'nome': historico.lead.nome_razaosocial,
                    'email': historico.lead.email,
                    'empresa': historico.lead.empresa
                } if historico.lead else None
            }
            
            historicos_data.append(historico_item)
        
        # Estatísticas do histórico
        total_contatos = len(historicos_data)
        contatos_convertidos = sum(1 for h in historicos_data if h['converteu_lead'])
        vendas_convertidas = sum(1 for h in historicos_data if h['converteu_venda'])
        
        data = {
            'historicos': historicos_data,
            'total': total_contatos,
            'estatisticas': {
                'total_contatos': total_contatos,
                'contatos_convertidos': contatos_convertidos,
                'vendas_convertidas': vendas_convertidas,
                'taxa_conversao_lead': (contatos_convertidos / total_contatos * 100) if total_contatos > 0 else 0,
                'taxa_conversao_venda': (vendas_convertidas / total_contatos * 100) if total_contatos > 0 else 0
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)


def get_status_categoria(status):
    """Categoriza o status para facilitar a exibição"""
    categorias = {
        'fluxo_inicializado': 'inicio',
        'fluxo_finalizado': 'sucesso',
        'transferido_humano': 'transferencia',
        'convertido_lead': 'conversao',
        'venda_confirmada': 'venda',
        'chamada_perdida': 'problema',
        'ocupado': 'problema',
        'desligou': 'problema',
        'nao_atendeu': 'problema',
        'erro_sistema': 'erro',
        'timeout': 'erro'
    }
    return categorias.get(status, 'outros')