from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import FluxoAtendimento, QuestaoFluxo, AtendimentoFluxo, RespostaQuestao


def _serialize_fluxo_atendimento(fluxo):
    """Serializa um objeto FluxoAtendimento"""
    return {
        'id': fluxo.id,
        'nome': fluxo.nome,
        'descricao': fluxo.descricao,
        'tipo_fluxo': fluxo.tipo_fluxo,
        'ativo': fluxo.ativo,
        'data_criacao': fluxo.data_criacao.isoformat() if fluxo.data_criacao else None,
        'data_atualizacao': fluxo.data_atualizacao.isoformat() if fluxo.data_atualizacao else None,
        'total_questoes': fluxo.get_total_questoes(),
        'total_atendimentos': fluxo.get_total_atendimentos(),
        'taxa_completacao': fluxo.get_taxa_completacao(),
        'status': fluxo.get_status_display(),
        'prioridade': fluxo.prioridade,
        'tags': fluxo.tags,
        'configuracoes': fluxo.configuracoes,
        'estatisticas': fluxo.get_estatisticas()
    }


def _serialize_questao_fluxo(questao):
    """Serializa um objeto QuestaoFluxo"""
    return {
        'id': questao.id,
        'fluxo_id': questao.fluxo.id,
        'fluxo_nome': questao.fluxo.nome,
        'indice': questao.indice,
        'titulo': questao.titulo,
        'descricao': questao.descricao,
        'tipo_questao': questao.tipo_questao,
        'tipo_validacao': questao.tipo_validacao,
        'opcoes_resposta': questao.get_opcoes_formatadas(),
        'resposta_padrao': questao.resposta_padrao,
        'regex_validacao': questao.regex_validacao,
        'tamanho_minimo': questao.tamanho_minimo,
        'tamanho_maximo': questao.tamanho_maximo,
        'valor_minimo': float(questao.valor_minimo) if questao.valor_minimo else None,
        'valor_maximo': float(questao.valor_maximo) if questao.valor_maximo else None,
        'questao_dependencia_id': questao.questao_dependencia.id if questao.questao_dependencia else None,
        'valor_dependencia': questao.valor_dependencia,
        'ativo': questao.ativo,
        'permite_voltar': questao.permite_voltar,
        'permite_editar': questao.permite_editar,
        'ordem_exibicao': questao.ordem_exibicao
    }


def _serialize_atendimento_fluxo(atendimento):
    """Serializa um objeto AtendimentoFluxo"""
    return {
        'id': atendimento.id,
        'lead_id': atendimento.lead.id,
        'lead_nome': atendimento.lead.nome_razaosocial,
        'fluxo_id': atendimento.fluxo.id,
        'fluxo_nome': atendimento.fluxo.nome,
        'historico_contato_id': atendimento.historico_contato.id if atendimento.historico_contato else None,
        'status': atendimento.status,
        'status_display': atendimento.get_status_display(),
        'questao_atual': atendimento.questao_atual,
        'total_questoes': atendimento.total_questoes,
        'questoes_respondidas': atendimento.questoes_respondidas,
        'progresso_percentual': atendimento.get_progresso_percentual(),
        'data_inicio': atendimento.data_inicio.isoformat() if atendimento.data_inicio else None,
        'data_ultima_atividade': atendimento.data_ultima_atividade.isoformat() if atendimento.data_ultima_atividade else None,
        'data_conclusao': atendimento.data_conclusao.isoformat() if atendimento.data_conclusao else None,
        'tempo_total': atendimento.tempo_total,
        'tempo_formatado': atendimento.get_tempo_formatado(),
        'tentativas_atual': atendimento.tentativas_atual,
        'max_tentativas': atendimento.max_tentativas,
        'dados_respostas': atendimento.dados_respostas,
        'respostas_formatadas': atendimento.get_respostas_formatadas(),
        'observacoes': atendimento.observacoes,
        'ip_origem': atendimento.ip_origem,
        'user_agent': atendimento.user_agent,
        'dispositivo': atendimento.dispositivo,
        'id_externo': atendimento.id_externo,
        'resultado_final': atendimento.resultado_final,
        'score_qualificacao': atendimento.score_qualificacao,
        'pode_avancar': atendimento.pode_avancar(),
        'pode_voltar': atendimento.pode_voltar(),
        'pode_ser_reiniciado': atendimento.pode_ser_reiniciado()
    }


@require_http_methods(["GET"])
def consultar_fluxos_api(request):
    """API GET para consultar fluxos de atendimento"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        per_page = max(1, min(per_page, 100))

        fluxo_id = request.GET.get('id')
        search = request.GET.get('search')
        tipo_fluxo = request.GET.get('tipo_fluxo')
        ativo = request.GET.get('ativo')
        status = request.GET.get('status')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        ordering = request.GET.get('ordering')

        qs = FluxoAtendimento.objects.all()

        if fluxo_id:
            qs = qs.filter(id=fluxo_id)
        else:
            if search:
                qs = qs.filter(
                    Q(nome__icontains=search) |
                    Q(descricao__icontains=search) |
                    Q(tags__icontains=search)
                )

            if tipo_fluxo:
                qs = qs.filter(tipo_fluxo=tipo_fluxo)

            if ativo is not None:
                ativo_bool = ativo.lower() in ['true', '1', 'sim', 'yes']
                qs = qs.filter(ativo=ativo_bool)

            if status:
                qs = qs.filter(status=status)

            if data_inicio:
                try:
                    di = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    qs = qs.filter(data_criacao__date__gte=di)
                except ValueError:
                    pass

            if data_fim:
                try:
                    df = datetime.strptime(data_fim, '%Y-%m-%d').date()
                    qs = qs.filter(data_criacao__date__lte=df)
                except ValueError:
                    pass

        # Ordenação
        allowed_order_fields = {'id', 'nome', 'data_criacao', 'data_atualizacao', 'prioridade', 'tipo_fluxo'}
        if ordering and ordering.lstrip('-') in allowed_order_fields:
            order_by = ordering
        else:
            order_by = '-data_criacao'
        
        qs = qs.order_by(order_by)

        total = qs.count()
        start = (page - 1) * per_page
        end = start + per_page
        items = qs[start:end]

        results = []
        for item in items:
            results.append(_serialize_fluxo_atendimento(item))

        return JsonResponse({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'ordering': order_by,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def consultar_questoes_api(request):
    """API GET para consultar questões de fluxo"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        per_page = max(1, min(per_page, 100))

        questao_id = request.GET.get('id')
        fluxo_id = request.GET.get('fluxo_id')
        search = request.GET.get('search')
        tipo_questao = request.GET.get('tipo_questao')
        tipo_validacao = request.GET.get('tipo_validacao')
        ativo = request.GET.get('ativo')
        indice = request.GET.get('indice')
        ordering = request.GET.get('ordering')

        qs = QuestaoFluxo.objects.select_related('fluxo', 'questao_dependencia')

        if questao_id:
            qs = qs.filter(id=questao_id)
        else:
            if fluxo_id:
                qs = qs.filter(fluxo_id=fluxo_id)

            if search:
                qs = qs.filter(
                    Q(titulo__icontains=search) |
                    Q(descricao__icontains=search)
                )

            if tipo_questao:
                qs = qs.filter(tipo_questao=tipo_questao)

            if tipo_validacao:
                qs = qs.filter(tipo_validacao=tipo_validacao)

            if ativo is not None:
                ativo_bool = ativo.lower() in ['true', '1', 'sim', 'yes']
                qs = qs.filter(ativo=ativo_bool)

            if indice:
                try:
                    indice_int = int(indice)
                    qs = qs.filter(indice=indice_int)
                except ValueError:
                    pass

        # Ordenação
        allowed_order_fields = {'id', 'indice', 'titulo', 'tipo_questao', 'ordem_exibicao'}
        if ordering and ordering.lstrip('-') in allowed_order_fields:
            order_by = ordering
        else:
            order_by = 'fluxo__id, indice'
        
        qs = qs.order_by(order_by)

        total = qs.count()
        start = (page - 1) * per_page
        end = start + per_page
        items = qs[start:end]

        results = []
        for item in items:
            results.append(_serialize_questao_fluxo(item))

        return JsonResponse({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'ordering': order_by,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def consultar_atendimentos_api(request):
    """API GET para consultar atendimentos de fluxo"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        per_page = max(1, min(per_page, 100))

        atendimento_id = request.GET.get('id')
        lead_id = request.GET.get('lead_id')
        fluxo_id = request.GET.get('fluxo_id')
        status = request.GET.get('status')
        search = request.GET.get('search')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        score_min = request.GET.get('score_min')
        score_max = request.GET.get('score_max')
        ordering = request.GET.get('ordering')

        qs = AtendimentoFluxo.objects.select_related('lead', 'fluxo', 'historico_contato')

        if atendimento_id:
            qs = qs.filter(id=atendimento_id)
        else:
            if lead_id:
                qs = qs.filter(lead_id=lead_id)

            if fluxo_id:
                qs = qs.filter(fluxo_id=fluxo_id)

            if status:
                qs = qs.filter(status=status)

            if search:
                qs = qs.filter(
                    Q(lead__nome_razaosocial__icontains=search) |
                    Q(fluxo__nome__icontains=search) |
                    Q(observacoes__icontains=search)
                )

            if data_inicio:
                try:
                    di = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    qs = qs.filter(data_inicio__date__gte=di)
                except ValueError:
                    pass

            if data_fim:
                try:
                    df = datetime.strptime(data_fim, '%Y-%m-%d').date()
                    qs = qs.filter(data_inicio__date__lte=df)
                except ValueError:
                    pass

            if score_min:
                try:
                    score_min_int = int(score_min)
                    qs = qs.filter(score_qualificacao__gte=score_min_int)
                except ValueError:
                    pass

            if score_max:
                try:
                    score_max_int = int(score_max)
                    qs = qs.filter(score_qualificacao__lte=score_max_int)
                except ValueError:
                    pass

        # Ordenação
        allowed_order_fields = {'id', 'data_inicio', 'data_ultima_atividade', 'questao_atual', 'score_qualificacao'}
        if ordering and ordering.lstrip('-') in allowed_order_fields:
            order_by = ordering
        else:
            order_by = '-data_inicio'
        
        qs = qs.order_by(order_by)

        total = qs.count()
        start = (page - 1) * per_page
        end = start + per_page
        items = qs[start:end]

        results = []
        for item in items:
            results.append(_serialize_atendimento_fluxo(item))

        return JsonResponse({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'ordering': order_by,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def consultar_respostas_api(request):
    """API GET para consultar respostas de questões"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        per_page = max(1, min(per_page, 100))

        resposta_id = request.GET.get('id')
        atendimento_id = request.GET.get('atendimento_id')
        questao_id = request.GET.get('questao_id')
        valida = request.GET.get('valida')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        ordering = request.GET.get('ordering')

        qs = RespostaQuestao.objects.select_related('atendimento', 'questao')

        if resposta_id:
            qs = qs.filter(id=resposta_id)
        else:
            if atendimento_id:
                qs = qs.filter(atendimento_id=atendimento_id)

            if questao_id:
                qs = qs.filter(questao_id=questao_id)

            if valida is not None:
                valida_bool = valida.lower() in ['true', '1', 'sim', 'yes']
                qs = qs.filter(valida=valida_bool)

            if data_inicio:
                try:
                    di = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    qs = qs.filter(data_resposta__date__gte=di)
                except ValueError:
                    pass

            if data_fim:
                try:
                    df = datetime.strptime(data_fim, '%Y-%m-%d').date()
                    qs = qs.filter(data_resposta__date__lte=df)
                except ValueError:
                    pass

        # Ordenação
        allowed_order_fields = {'id', 'data_resposta', 'tentativas', 'tempo_resposta'}
        if ordering and ordering.lstrip('-') in allowed_order_fields:
            order_by = ordering
        else:
            order_by = '-data_resposta'
        
        qs = qs.order_by(order_by)

        total = qs.count()
        start = (page - 1) * per_page
        end = start + per_page
        items = qs[start:end]

        results = []
        for item in items:
            results.append({
                'id': item.id,
                'atendimento_id': item.atendimento.id,
                'questao_id': item.questao.id,
                'questao_titulo': item.questao.titulo,
                'resposta': item.resposta,
                'resposta_processada': item.resposta_processada,
                'valida': item.valida,
                'mensagem_erro': item.mensagem_erro,
                'tentativas': item.tentativas,
                'data_resposta': item.data_resposta.isoformat() if item.data_resposta else None,
                'tempo_resposta': item.tempo_resposta,
                'tempo_resposta_formatado': item.get_tempo_resposta_formatado(),
                'ip_origem': item.ip_origem,
                'user_agent': item.user_agent,
                'dados_extras': item.dados_extras
            })

        return JsonResponse({
            'results': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'ordering': order_by,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
