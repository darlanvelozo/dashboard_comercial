from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
import json
from .models import LeadProspecto, Prospecto, HistoricoContato, ConfiguracaoSistema, LogSistema


def dashboard_view(request):
    """View principal do dashboard"""
    return render(request, 'vendas_web/dashboard.html')


def dashboard_data(request):
    """API para dados principais do dashboard"""
    try:
        # Estatísticas gerais
        total_leads = LeadProspecto.objects.filter(ativo=True).count()
        total_prospectos = Prospecto.objects.count()
        
        # Leads de hoje
        hoje = timezone.now().date()
        leads_hoje = LeadProspecto.objects.filter(
            data_cadastro__date=hoje,
            ativo=True
        ).count()
        
        # Valor total
        valor_total = LeadProspecto.objects.filter(
            ativo=True
        ).aggregate(total=Sum('valor'))['total'] or 0
        
        # Contatos
        total_contatos = HistoricoContato.objects.count()
        contatos_hoje = HistoricoContato.objects.filter(
            data_hora_contato__date=hoje
        ).count()
        
        # Taxa de finalização (fluxo_finalizado vs total)
        contatos_finalizados = HistoricoContato.objects.filter(
            status='fluxo_finalizado'
        ).count()
        taxa_finalizacao = (contatos_finalizados / total_contatos * 100) if total_contatos > 0 else 0
        
        # Transferidos para humano
        transferidos_humano = HistoricoContato.objects.filter(
            status='transferido_humano'
        ).count()
        
        # Métricas de performance
        prospectos_erro = Prospecto.objects.filter(status='erro').count()
        
        # Tempo médio de processamento
        tempo_medio = Prospecto.objects.filter(
            tempo_processamento__isnull=False
        ).aggregate(media=Avg('tempo_processamento'))['media'] or 0
        
        # Valor médio por lead
        media_valor = LeadProspecto.objects.filter(
            ativo=True,
            valor__gt=0
        ).aggregate(media=Avg('valor'))['media'] or 0
        
        # Leads com valor
        leads_com_valor = LeadProspecto.objects.filter(
            ativo=True,
            valor__gt=0
        ).count()
        
        data = {
            'stats': {
                'totalLeads': total_leads,
                'totalProspectos': total_prospectos,
                'leadsHoje': leads_hoje,
                'valorTotal': f"R$ {valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'totalContatos': total_contatos,
                'contatosHoje': contatos_hoje,
                'taxaFinalizacao': f"{taxa_finalizacao:.1f}%",
                'transferidosHumano': transferidos_humano,
                'prospectosErro': prospectos_erro,
                'tempoMedio': f"{tempo_medio:.1f}s",
                'mediaValor': f"R$ {media_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'leadsComValor': leads_com_valor
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def dashboard_charts_data(request):
    """API para dados dos gráficos"""
    try:
        # Status dos prospectos
        status_prospectos = Prospecto.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Leads dos últimos 7 dias
        ultimos_7_dias = []
        for i in range(7):
            data = timezone.now().date() - timedelta(days=i)
            count = LeadProspecto.objects.filter(
                data_cadastro__date=data,
                ativo=True
            ).count()
            ultimos_7_dias.append({
                'date': data.strftime('%d/%m'),
                'count': count
            })
        ultimos_7_dias.reverse()
        
        # Status dos contatos
        status_contatos = HistoricoContato.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Contatos por hora (últimas 24h)
        contatos_por_hora = []
        agora = timezone.now()
        for i in range(24):
            hora_inicio = (agora - timedelta(hours=i+1)).replace(minute=0, second=0, microsecond=0)
            hora_fim = hora_inicio + timedelta(hours=1)
            count = HistoricoContato.objects.filter(
                data_hora_contato__gte=hora_inicio,
                data_hora_contato__lt=hora_fim
            ).count()
            contatos_por_hora.append({
                'hora': hora_inicio.strftime('%H:00'),
                'count': count
            })
        contatos_por_hora.reverse()
        
        # Contatos por dia (últimos 7 dias)
        contatos_por_dia = []
        for i in range(7):
            data = timezone.now().date() - timedelta(days=i)
            count = HistoricoContato.objects.filter(
                data_hora_contato__date=data
            ).count()
            contatos_por_dia.append({
                'date': data.strftime('%d/%m'),
                'count': count
            })
        contatos_por_dia.reverse()
        
        data = {
            'statusProspectos': list(status_prospectos),
            'leadsUltimos7Dias': ultimos_7_dias,
            'statusContatos': list(status_contatos),
            'contatosPorHora': contatos_por_hora,
            'contatosPorDia': contatos_por_dia
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
                    Q(cpf_cnpj__icontains=search)
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
            prospectos_data.append({
                'id': prospecto.id,
                'nome_prospecto': prospecto.nome_prospecto,
                'lead_relacionado': prospecto.lead.nome_razaosocial if prospecto.lead else None,
                'id_prospecto_hubsoft': prospecto.id_prospecto_hubsoft or '-',
                'status': prospecto.get_status_display(),
                'prioridade': prospecto.prioridade,
                'data_criacao': prospecto.data_criacao.strftime('%d/%m/%Y %H:%M'),
                'data_processamento': prospecto.data_processamento.strftime('%d/%m/%Y %H:%M') if prospecto.data_processamento else '-',
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
                'data_hora_contato': contato.data_hora_contato.strftime('%d/%m/%Y %H:%M'),
                'duracao_formatada': contato.get_duracao_formatada(),
                'sucesso': contato.sucesso,
                'transcricao': contato.transcricao or '-',
                'observacoes': contato.observacoes or '-',
                'ip_origem': contato.ip_origem or '-',
                'tempo_relativo': contato.get_tempo_relativo(),
                'dados_extras': contato.dados_extras
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
        
        # Estatísticas do telefone
        total_contatos = contatos.count()
        contatos_sucesso = contatos.filter(sucesso=True).count()
        contatos_finalizados = contatos.filter(status='fluxo_finalizado').count()
        duracao_total = sum([c.duracao_segundos or 0 for c in contatos])
        
        # Timeline dos contatos
        timeline_data = []
        for contato in contatos:
            timeline_data.append({
                'id': contato.id,
                'data_hora': contato.data_hora_contato.strftime('%d/%m/%Y %H:%M:%S'),
                'status': contato.get_status_display(),
                'nome': contato.nome_contato or 'Não identificado',
                'duracao': contato.get_duracao_formatada(),
                'sucesso': contato.sucesso,
                'observacoes': contato.observacoes or '',
                'tempo_relativo': contato.get_tempo_relativo()
            })
        
        data = {
            'telefone': telefone,
            'estatisticas': {
                'total_contatos': total_contatos,
                'contatos_sucesso': contatos_sucesso,
                'contatos_finalizados': contatos_finalizados,
                'duracao_total_minutos': duracao_total // 60 if duracao_total else 0
            },
            'timeline': timeline_data,
            'historico_detalhado': timeline_data  # Mesmo dados para a tabela detalhada
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)