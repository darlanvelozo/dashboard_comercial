from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db import models
from django import forms
from .models import (
    LeadProspecto, 
    Prospecto, 
    HistoricoContato, 
    ConfiguracaoSistema, 
    LogSistema,
    StatusConfiguravel,
    FluxoAtendimento,
    QuestaoFluxo,
    AtendimentoFluxo,
    RespostaQuestao,
    ConfiguracaoCadastro,
    PlanoInternet,
    OpcaoVencimento,
    CadastroCliente,
)


class AdminSiteCustom(admin.AdminSite):
    site_header = 'Painel Comercial'
    site_title = 'Admin - Comercial'
    index_title = 'Visão Geral'


admin.site.site_header = AdminSiteCustom.site_header
admin.site.site_title = AdminSiteCustom.site_title
admin.site.index_title = AdminSiteCustom.index_title


class ProspectoInline(admin.TabularInline):
    model = Prospecto
    fields = ('nome_prospecto', 'status', 'prioridade', 'data_criacao')
    readonly_fields = ('data_criacao',)
    extra = 0
    show_change_link = True


class HistoricoContatoInline(admin.TabularInline):
    model = HistoricoContato
    fields = ('telefone', 'status', 'sucesso', 'data_hora_contato')
    readonly_fields = ('data_hora_contato',)
    extra = 0
    show_change_link = True


class AtendimentoFluxoInline(admin.TabularInline):
    """Inline para atendimentos de fluxo dentro do lead"""
    model = AtendimentoFluxo
    fields = ('fluxo', 'status', 'questao_atual', 'questoes_respondidas', 'data_inicio')
    readonly_fields = ('data_inicio',)
    extra = 0
    show_change_link = True
    ordering = ['-data_inicio']
    verbose_name = "Atendimento de Fluxo"
    verbose_name_plural = "Atendimentos de Fluxo"


@admin.register(LeadProspecto)
class LeadProspectoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_razaosocial',
        'email',
        'telefone',
        'id_hubsoft',
        'origem_badge',
        'get_valor_formatado',
        'status_api_badge',
        'data_cadastro',
        'ativo_badge'
    ]
    list_filter = [
        'origem',
        'status_api',
        'ativo',
        'data_cadastro',
        'data_nascimento',
        'estado',
        'bairro'
    ]
    search_fields = [
        'nome_razaosocial',
        'email',
        'telefone',
        'empresa',
        'cpf_cnpj',
        'id_hubsoft',
        'rua',
        'bairro',
        'cidade',
        'cep'
    ]
    readonly_fields = [
        'data_cadastro',
        'data_atualizacao',
        'get_valor_formatado'
    ]
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                'nome_razaosocial',
                'email',
                'telefone',
                'empresa',
                'id_hubsoft'
            )
        }),
        ('Documentos e Localização', {
            'fields': (
                'cpf_cnpj',
                'endereco',
                'rua',
                'numero_residencia',
                'bairro',
                'cidade',
                'estado',
                'cep'
            ),
            'classes': ('collapse',)
        }),
        ('Dados RP / Comerciais', {
            'fields': (
                'id_plano_rp',
                'id_dia_vencimento',
                'id_vendedor_rp',
                'data_nascimento'
            ),
            'classes': ('collapse',)
        }),
        ('Vendas e Status', {
            'fields': (
                'valor',
                'origem',
                'status_api',
                'ativo'
            )
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Dados do Sistema', {
            'fields': (
                'data_cadastro',
                'data_atualizacao'
            ),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_cadastro'
    ordering = ['-data_cadastro']
    list_per_page = 25
    inlines = [ProspectoInline, HistoricoContatoInline, AtendimentoFluxoInline]
    save_on_top = True
    actions = ['ativar_leads', 'inativar_leads', 'exportar_csv']
    
    def get_valor_formatado(self, obj):
        try:
            return obj.get_valor_formatado()
        except (TypeError, AttributeError):
            return "R$ 0,00"
    get_valor_formatado.short_description = 'Valor'
    get_valor_formatado.admin_order_field = 'valor'

    def status_api_badge(self, obj):
        colors = {
            'pendente': '#f39c12',
            'processado': '#3498db',
            'erro': '#e74c3c',
            'sucesso': '#2ecc71',
            'rejeitado': '#c0392b',
            'aguardando_retry': '#8e44ad',
            'processamento_manual': '#16a085',
        }
        color = colors.get(obj.status_api, '#7f8c8d')
        label = obj.get_status_api_display() if hasattr(obj, 'get_status_api_display') else obj.status_api
        return format_html('<span style="padding:2px 8px;border-radius:12px;background:{};color:#fff;font-size:11px;">{}</span>', color, label)
    status_api_badge.short_description = 'Status'
    status_api_badge.admin_order_field = 'status_api'

    def origem_badge(self, obj):
        colors = {
            'whatsapp': '#25D366',
            'instagram': '#C13584',
            'facebook': '#1877F2',
            'google': '#DB4437',
            'site': '#2c3e50',
            'indicacao': '#16a085',
            'telefone': '#2980b9',
            'email': '#8e44ad',
            'outros': '#7f8c8d',
        }
        color = colors.get(obj.origem, '#7f8c8d')
        label = obj.get_origem_display() if hasattr(obj, 'get_origem_display') else obj.origem
        return format_html('<span style="padding:2px 8px;border-radius:12px;border:1px solid {};color:{};font-size:11px;">{}</span>', color, color, label)
    origem_badge.short_description = 'Origem'
    origem_badge.admin_order_field = 'origem'

    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html('<span style="color:#2ecc71;font-weight:600;">Ativo</span>')
        return format_html('<span style="color:#e74c3c;font-weight:600;">Inativo</span>')
    ativo_badge.short_description = 'Ativo'
    ativo_badge.admin_order_field = 'ativo'

    # Ações em massa
    def ativar_leads(self, request, queryset):
        updated = queryset.update(ativo=True)
        self.message_user(request, f"{updated} lead(s) ativado(s).")
    ativar_leads.short_description = 'Ativar selecionados'

    def inativar_leads(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f"{updated} lead(s) inativado(s).")
    inativar_leads.short_description = 'Inativar selecionados'

    def exportar_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="leads_export.csv"'
        writer = csv.writer(response)
        headers = [
            'id', 'nome_razaosocial', 'email', 'telefone', 'empresa', 'origem',
            'status_api', 'valor', 'cep', 'cidade', 'estado', 'bairro', 'rua',
            'numero_residencia', 'id_hubsoft', 'id_plano_rp', 'id_dia_vencimento',
            'id_vendedor_rp', 'data_nascimento', 'data_cadastro', 'data_atualizacao', 'ativo'
        ]
        writer.writerow(headers)
        for obj in queryset:
            writer.writerow([
                obj.id, obj.nome_razaosocial, obj.email, obj.telefone, obj.empresa, obj.origem,
                obj.status_api, obj.valor, obj.cep, obj.cidade, obj.estado, getattr(obj, 'bairro', ''), getattr(obj, 'rua', ''),
                getattr(obj, 'numero_residencia', ''), obj.id_hubsoft, getattr(obj, 'id_plano_rp', ''), getattr(obj, 'id_dia_vencimento', ''),
                getattr(obj, 'id_vendedor_rp', ''), getattr(obj, 'data_nascimento', ''), obj.data_cadastro, obj.data_atualizacao, obj.ativo
            ])
        return response
    exportar_csv.short_description = 'Exportar selecionados como CSV'


@admin.register(Prospecto)
class ProspectoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_prospecto', 
        'lead', 
        'status', 
        'tentativas_processamento', 
        'get_tempo_processamento_formatado', 
        'data_criacao',
        'data_processamento'
    ]
    list_filter = [
        'status', 
        'prioridade', 
        'data_criacao', 
        'tentativas_processamento'
    ]
    search_fields = [
        'nome_prospecto', 
        'id_prospecto_hubsoft', 
        'lead__nome_razaosocial', 
        'lead__email'
    ]
    readonly_fields = [
        'data_criacao', 
        'get_tempo_processamento_formatado'
    ]
    fieldsets = (
        ('Informações do Prospecto', {
            'fields': (
                'nome_prospecto', 
                'lead', 
                'id_prospecto_hubsoft', 
                'status', 
                'prioridade'
            )
        }),
        ('Processamento', {
            'fields': (
                'data_processamento', 
                'tentativas_processamento', 
                'tempo_processamento', 
                'erro_processamento'
            )
        }),
        ('Dados JSON', {
            'fields': (
                'dados_processamento', 
                'resultado_processamento'
            ),
            'classes': ('collapse',)
        }),
        ('Dados do Sistema', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_criacao'
    ordering = ['-data_criacao']
    list_per_page = 25
    autocomplete_fields = ('lead',)
    list_select_related = ('lead',)
    save_on_top = True
    
    def get_tempo_processamento_formatado(self, obj):
        try:
            return obj.get_tempo_processamento_formatado()
        except (TypeError, AttributeError):
            return "N/A"
    get_tempo_processamento_formatado.short_description = 'Tempo Processamento'
    get_tempo_processamento_formatado.admin_order_field = 'tempo_processamento'


@admin.register(HistoricoContato)
class HistoricoContatoAdmin(admin.ModelAdmin):
    list_display = [
        'telefone', 
        'nome_contato', 
        'status', 
        'get_duracao_formatada', 
        'sucesso', 
        'data_hora_contato',
        'lead'
    ]
    list_filter = [
        'status', 
        'sucesso', 
        'data_hora_contato'
    ]
    search_fields = [
        'telefone', 
        'nome_contato', 
        'lead__nome_razaosocial', 
        'lead__email'
    ]
    readonly_fields = [
        'data_hora_contato', 
        'get_duracao_formatada', 
        'get_tempo_relativo'
    ]
    fieldsets = (
        ('Informações do Contato', {
            'fields': (
                'telefone', 
                'nome_contato', 
                'lead', 
                'status', 
                'sucesso'
            )
        }),
        ('Detalhes da Chamada', {
            'fields': (
                'data_hora_contato', 
                'duracao_segundos', 
                'transcricao', 
                'observacoes'
            )
        }),
        ('Dados Técnicos', {
            'fields': (
                'ip_origem', 
                'user_agent', 
                'dados_extras'
            ),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_hora_contato'
    ordering = ['-data_hora_contato']
    list_per_page = 25
    
    def get_duracao_formatada(self, obj):
        try:
            return obj.get_duracao_formatada()
        except (TypeError, AttributeError):
            return "N/A"
    get_duracao_formatada.short_description = 'Duração'
    get_duracao_formatada.admin_order_field = 'duracao_segundos'
    
    def get_tempo_relativo(self, obj):
        try:
            return obj.get_tempo_relativo()
        except (TypeError, AttributeError):
            return "N/A"
    get_tempo_relativo.short_description = 'Há quanto tempo'


@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = [
        'chave', 
        'valor_truncado', 
        'tipo', 
        'ativo', 
        'data_atualizacao'
    ]
    list_filter = [
        'tipo', 
        'ativo', 
        'data_criacao'
    ]
    search_fields = [
        'chave', 
        'valor', 
        'descricao'
    ]
    readonly_fields = [
        'data_criacao', 
        'data_atualizacao'
    ]
    fieldsets = (
        ('Configuração', {
            'fields': (
                'chave', 
                'valor', 
                'tipo', 
                'ativo'
            )
        }),
        ('Descrição', {
            'fields': ('descricao',)
        }),
        ('Dados do Sistema', {
            'fields': (
                'data_criacao', 
                'data_atualizacao'
            ),
            'classes': ('collapse',)
        })
    )
    ordering = ['chave']
    list_per_page = 25
    
    def valor_truncado(self, obj):
        if len(obj.valor) > 50:
            return f"{obj.valor[:50]}..."
        return obj.valor
    valor_truncado.short_description = 'Valor'


@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = [
        'nivel', 
        'modulo', 
        'mensagem_truncada', 
        'usuario', 
        'ip', 
        'data_criacao'
    ]
    list_filter = [
        'nivel', 
        'modulo', 
        'data_criacao'
    ]
    search_fields = [
        'modulo', 
        'mensagem', 
        'usuario'
    ]
    readonly_fields = [
        'data_criacao'
    ]
    fieldsets = (
        ('Log', {
            'fields': (
                'nivel', 
                'modulo', 
                'mensagem'
            )
        }),
        ('Usuário e IP', {
            'fields': (
                'usuario', 
                'ip'
            )
        }),
        ('Dados Extras', {
            'fields': ('dados_extras',),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_criacao'
    ordering = ['-data_criacao']
    list_per_page = 25
    
    def mensagem_truncada(self, obj):
        if len(obj.mensagem) > 80:
            return f"{obj.mensagem[:80]}..."
        return obj.mensagem
    mensagem_truncada.short_description = 'Mensagem'
    
    def get_readonly_fields(self, request, obj=None):
        # Torna todos os campos readonly para logs (apenas visualização)
        if obj:
            return [field.name for field in obj._meta.fields]
        return self.readonly_fields


@admin.register(StatusConfiguravel)
class StatusConfiguravelAdmin(admin.ModelAdmin):
    list_display = ['grupo', 'codigo', 'rotulo', 'ativo', 'ordem']
    list_filter = ['grupo', 'ativo']
    search_fields = ['codigo', 'rotulo']
    list_editable = ['rotulo', 'ativo', 'ordem']
    ordering = ['grupo', 'ordem', 'codigo']


# ============================================================================
# ADMIN PARA FLUXOS DE ATENDIMENTO
# ============================================================================

class QuestaoFluxoInline(admin.TabularInline):
    """Inline para questões dentro do fluxo"""
    model = QuestaoFluxo
    fields = ('indice', 'titulo', 'tipo_questao', 'tipo_validacao', 'ativo')
    extra = 1
    show_change_link = True
    ordering = ['indice']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('questao_dependencia')
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        # Definir valores padrão para novos registros
        if obj:
            # Calcular próximo índice disponível
            ultimo_indice = obj.questoes.aggregate(
                models.Max('indice')
            )['indice__max'] or 0
            
            # Verificar se o campo indice existe antes de tentar acessá-lo
            if 'indice' in formset.form.base_fields:
                formset.form.base_fields['indice'].initial = ultimo_indice + 1
            if 'fluxo' in formset.form.base_fields:
                formset.form.base_fields['fluxo'].initial = obj
                formset.form.base_fields['fluxo'].widget = forms.HiddenInput()
        
        return formset
    
    def save_new_instance(self, request, instance, form, commit=True):
        # Garantir que o índice seja preenchido automaticamente
        if not instance.indice and instance.fluxo:
            ultimo_indice = instance.fluxo.questoes.aggregate(
                models.Max('indice')
            )['indice__max'] or 0
            instance.indice = ultimo_indice + 1
        
        return super().save_new_instance(request, instance, form, commit)


class AtendimentoFluxoInline(admin.TabularInline):
    """Inline para atendimentos dentro do fluxo"""
    model = AtendimentoFluxo
    fields = ('lead', 'status', 'questao_atual', 'questoes_respondidas', 'data_inicio')
    readonly_fields = ('data_inicio',)
    extra = 0
    show_change_link = True
    ordering = ['-data_inicio']


@admin.register(FluxoAtendimento)
class FluxoAtendimentoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'tipo_fluxo_badge',
        'status_badge',
        'get_total_questoes',
        'get_total_atendimentos',
        'get_taxa_completacao',
        'data_criacao',
        'ativo_badge'
    ]
    list_filter = [
        'tipo_fluxo',
        'status',
        'ativo',
        'data_criacao',
        'criado_por'
    ]
    search_fields = [
        'nome',
        'descricao',
        'criado_por'
    ]
    readonly_fields = [
        'data_criacao',
        'data_atualizacao',
        'get_total_questoes',
        'get_total_atendimentos',
        'get_estatisticas_formatadas'
    ]
    fieldsets = (
        ('Informações do Fluxo', {
            'fields': (
                'nome',
                'descricao',
                'tipo_fluxo',
                'status',
                'ativo'
            )
        }),
        ('Configurações', {
            'fields': (
                'max_tentativas',
                'tempo_limite_minutos',
                'permite_pular_questoes'
            )
        }),
        ('Controle', {
            'fields': (
                'criado_por',
                'data_criacao',
                'data_atualizacao'
            ),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('get_estatisticas_formatadas',),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_criacao'
    ordering = ['-data_criacao']
    list_per_page = 25
    inlines = [QuestaoFluxoInline, AtendimentoFluxoInline]
    save_on_top = True
    actions = ['ativar_fluxos', 'inativar_fluxos', 'duplicar_fluxos']
    
    def tipo_fluxo_badge(self, obj):
        colors = {
            'qualificacao': '#3498db',
            'vendas': '#2ecc71',
            'suporte': '#f39c12',
            'onboarding': '#9b59b6',
            'pesquisa': '#e67e22',
            'customizado': '#34495e',
        }
        color = colors.get(obj.tipo_fluxo, '#7f8c8d')
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;background:{};color:#fff;font-size:11px;">{}</span>',
            color, obj.get_tipo_fluxo_display()
        )
    tipo_fluxo_badge.short_description = 'Tipo'
    tipo_fluxo_badge.admin_order_field = 'tipo_fluxo'
    
    def status_badge(self, obj):
        colors = {
            'ativo': '#2ecc71',
            'inativo': '#e74c3c',
            'rascunho': '#95a5a6',
            'teste': '#f39c12',
        }
        color = colors.get(obj.status, '#7f8c8d')
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;background:{};color:#fff;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html('<span style="color:#2ecc71;font-weight:600;">✓ Ativo</span>')
        return format_html('<span style="color:#e74c3c;font-weight:600;">✗ Inativo</span>')
    ativo_badge.short_description = 'Ativo'
    ativo_badge.admin_order_field = 'ativo'
    
    def get_total_questoes(self, obj):
        try:
            return obj.get_total_questoes()
        except (TypeError, AttributeError):
            return 0
    get_total_questoes.short_description = 'Questões'
    get_total_questoes.admin_order_field = 'questoes__count'
    
    def get_total_atendimentos(self, obj):
        try:
            return obj.atendimentos.count()
        except (TypeError, AttributeError):
            return 0
    get_total_atendimentos.short_description = 'Atendimentos'
    
    def get_taxa_completacao(self, obj):
        try:
            estatisticas = obj.get_estatisticas()
            return f"{estatisticas['taxa_completacao']}%"
        except (TypeError, AttributeError):
            return "0%"
    get_taxa_completacao.short_description = 'Taxa Completação'
    
    def get_estatisticas_formatadas(self, obj):
        if not obj.pk:
            return "Salve o fluxo para ver estatísticas"
        
        try:
            estatisticas = obj.get_estatisticas()
            total_questoes = obj.get_total_questoes()
        except (TypeError, AttributeError):
            return "Erro ao carregar estatísticas"
        
        # Link para adicionar nova questão
        add_questao_url = f"/admin/vendas_web/questaofluxo/add/?fluxo={obj.id}"
        
        html = f"""
        <div style="background:#f8f9fa;padding:15px;border-radius:8px;border:1px solid #dee2e6;">
            <h4 style="margin-top:0;color:#495057;">📊 Estatísticas do Fluxo</h4>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
                <div>
                    <strong>Total de Atendimentos:</strong> {estatisticas['total_atendimentos']}<br>
                    <strong>Completados:</strong> {estatisticas['atendimentos_completados']}<br>
                    <strong>Taxa de Completação:</strong> {estatisticas['taxa_completacao']}%
                </div>
                <div>
                    <strong>Tempo Médio:</strong> {estatisticas['tempo_medio_segundos']}s<br>
                    <strong>Questões Ativas:</strong> {total_questoes}<br>
                    <strong>Status:</strong> {obj.get_status_display()}
                </div>
            </div>
            <div style="margin-top:15px;text-align:center;">
                <a href="{add_questao_url}" class="button" style="background:#007cba;color:#fff;padding:8px 16px;text-decoration:none;border-radius:4px;">
                    ➕ Adicionar Nova Questão
                </a>
            </div>
        </div>
        """
        return format_html(html)
    get_estatisticas_formatadas.short_description = 'Estatísticas'
    
    # Ações em massa
    def ativar_fluxos(self, request, queryset):
        updated = queryset.update(ativo=True, status='ativo')
        self.message_user(request, f"{updated} fluxo(s) ativado(s).")
    ativar_fluxos.short_description = 'Ativar selecionados'
    
    def inativar_fluxos(self, request, queryset):
        updated = queryset.update(ativo=False, status='inativo')
        self.message_user(request, f"{updated} fluxo(s) inativado(s).")
    inativar_fluxos.short_description = 'Inativar selecionados'
    
    def duplicar_fluxos(self, request, queryset):
        for fluxo in queryset:
            # Duplicar fluxo
            novo_fluxo = FluxoAtendimento.objects.create(
                nome=f"{fluxo.nome} (Cópia)",
                descricao=f"Cópia de: {fluxo.descricao}",
                tipo_fluxo=fluxo.tipo_fluxo,
                status='rascunho',
                max_tentativas=fluxo.max_tentativas,
                tempo_limite_minutos=fluxo.tempo_limite_minutos,
                permite_pular_questoes=fluxo.permite_pular_questoes,
                criado_por=request.user.username if request.user.is_authenticated else 'admin'
            )
            
            # Duplicar questões
            for questao in fluxo.questoes.all():
                QuestaoFluxo.objects.create(
                    fluxo=novo_fluxo,
                    indice=questao.indice,
                    titulo=questao.titulo,
                    descricao=questao.descricao,
                    tipo_questao=questao.tipo_questao,
                    tipo_validacao=questao.tipo_validacao,
                    opcoes_resposta=questao.opcoes_resposta,
                    resposta_padrao=questao.resposta_padrao,
                    regex_validacao=questao.regex_validacao,
                    tamanho_minimo=questao.tamanho_minimo,
                    tamanho_maximo=questao.tamanho_maximo,
                    valor_minimo=questao.valor_minimo,
                    valor_maximo=questao.valor_maximo,
                    permite_voltar=questao.permite_voltar,
                    permite_editar=questao.permite_editar,
                    ordem_exibicao=questao.ordem_exibicao,
                    ativo=questao.ativo
                )
        
        self.message_user(request, f"{queryset.count()} fluxo(s) duplicado(s).")
    duplicar_fluxos.short_description = 'Duplicar selecionados'


class RespostaQuestaoInline(admin.TabularInline):
    """Inline para respostas dentro da questão"""
    model = RespostaQuestao
    fields = ('atendimento', 'resposta', 'valida', 'data_resposta')
    readonly_fields = ('data_resposta',)
    extra = 0
    show_change_link = True
    ordering = ['-data_resposta']


@admin.register(QuestaoFluxo)
class QuestaoFluxoAdmin(admin.ModelAdmin):
    list_display = [
        'fluxo',
        'indice',
        'titulo',
        'tipo_questao_badge',
        'tipo_validacao_badge',
        'ativo_badge',
        'permite_voltar',
        'permite_editar'
    ]
    list_filter = [
        'fluxo',
        'tipo_questao',
        'tipo_validacao',
        'ativo',
        'permite_voltar',
        'permite_editar'
    ]
    search_fields = [
        'titulo',
        'descricao',
        'fluxo__nome'
    ]
    readonly_fields = [
        'get_opcoes_formatadas_display',
        'get_validacoes_display'
    ]
    fieldsets = (
        ('Questão', {
            'fields': (
                'fluxo',
                'indice',
                'titulo',
                'descricao'
            )
        }),
        ('Tipo e Validação', {
            'fields': (
                'tipo_questao',
                'tipo_validacao',
                'ativo'
            )
        }),
        ('Configurações de Resposta', {
            'fields': (
                'opcoes_resposta',
                'resposta_padrao',
                'get_opcoes_formatadas_display'
            ),
            'classes': ('collapse',)
        }),
        ('Validações', {
            'fields': (
                'regex_validacao',
                'tamanho_minimo',
                'tamanho_maximo',
                'valor_minimo',
                'valor_maximo',
                'get_validacoes_display'
            ),
            'classes': ('collapse',)
        }),
        ('Dependências', {
            'fields': (
                'questao_dependencia',
                'valor_dependencia'
            ),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': (
                'permite_voltar',
                'permite_editar',
                'ordem_exibicao'
            )
        })
    )
    ordering = ['fluxo', 'indice']
    list_per_page = 25
    inlines = [RespostaQuestaoInline]
    save_on_top = True
    autocomplete_fields = ['fluxo', 'questao_dependencia']
    list_select_related = ['fluxo']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Se é um novo registro, preencher índice automaticamente
        if not obj:
            # Tentar obter o fluxo do parâmetro GET
            fluxo_id = request.GET.get('fluxo')
            if fluxo_id:
                try:
                    fluxo = FluxoAtendimento.objects.get(id=fluxo_id)
                    ultimo_indice = fluxo.questoes.aggregate(
                        models.Max('indice')
                    )['indice__max'] or 0
                    form.base_fields['indice'].initial = ultimo_indice + 1
                    form.base_fields['fluxo'].initial = fluxo
                except FluxoAtendimento.DoesNotExist:
                    pass
        
        return form
    
    def save_model(self, request, obj, form, change):
        # Se é um novo registro e não tem índice, calcular automaticamente
        if not change and not obj.indice:
            if obj.fluxo:
                ultimo_indice = obj.fluxo.questoes.aggregate(
                    models.Max('indice')
                )['indice__max'] or 0
                obj.indice = ultimo_indice + 1
        
        super().save_model(request, obj, form, change)
    
    def tipo_questao_badge(self, obj):
        colors = {
            'texto': '#3498db',
            'numero': '#2ecc71',
            'email': '#9b59b6',
            'telefone': '#f39c12',
            'cpf_cnpj': '#e67e22',
            'cep': '#34495e',
            'endereco': '#16a085',
            'select': '#8e44ad',
            'multiselect': '#d35400',
            'data': '#27ae60',
            'hora': '#2980b9',
            'data_hora': '#c0392b',
            'boolean': '#e74c3c',
            'escala': '#f1c40f',
            'arquivo': '#95a5a6',
        }
        color = colors.get(obj.tipo_questao, '#7f8c8d')
        return format_html(
            '<span style="padding:2px 6px;border-radius:8px;background:{};color:#fff;font-size:10px;">{}</span>',
            color, obj.get_tipo_questao_display()
        )
    tipo_questao_badge.short_description = 'Tipo'
    tipo_questao_badge.admin_order_field = 'tipo_questao'
    
    def tipo_validacao_badge(self, obj):
        colors = {
            'obrigatoria': '#e74c3c',
            'opcional': '#95a5a6',
            'condicional': '#f39c12',
        }
        color = colors.get(obj.tipo_validacao, '#7f8c8d')
        return format_html(
            '<span style="padding:2px 6px;border-radius:8px;background:{};color:#fff;font-size:10px;">{}</span>',
            color, obj.get_tipo_validacao_display()
        )
    tipo_validacao_badge.short_description = 'Validação'
    tipo_validacao_badge.admin_order_field = 'tipo_validacao'
    
    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html('<span style="color:#2ecc71;font-weight:600;">✓</span>')
        return format_html('<span style="color:#e74c3c;font-weight:600;">✗</span>')
    ativo_badge.short_description = 'Ativa'
    ativo_badge.admin_order_field = 'ativo'
    
    def get_opcoes_formatadas_display(self, obj):
        if obj.opcoes_resposta:
            try:
                opcoes = obj.get_opcoes_formatadas()
                if opcoes:
                    html = '<div style="background:#f8f9fa;padding:8px;border-radius:4px;border:1px solid #dee2e6;">'
                    html += '<strong>Opções disponíveis:</strong><br>'
                    for i, opcao in enumerate(opcoes, 1):
                        html += f"{i}. {opcao}<br>"
                    html += '</div>'
                    return format_html(html)
            except (TypeError, AttributeError):
                return "Erro ao carregar opções"
        return "Nenhuma opção definida"
    get_opcoes_formatadas_display.short_description = 'Opções de Resposta'
    
    def get_validacoes_display(self, obj):
        try:
            validacoes = []
            if obj.regex_validacao:
                validacoes.append(f"Regex: {obj.regex_validacao}")
            if obj.tamanho_minimo:
                validacoes.append(f"Min: {obj.tamanho_minimo} chars")
            if obj.tamanho_maximo:
                validacoes.append(f"Max: {obj.tamanho_maximo} chars")
            if obj.valor_minimo is not None:
                validacoes.append(f"Valor min: {obj.valor_minimo}")
            if obj.valor_maximo is not None:
                validacoes.append(f"Valor max: {obj.valor_maximo}")
            
            if validacoes:
                html = '<div style="background:#f8f9fa;padding:8px;border-radius:4px;border:1px solid #dee2e6;">'
                html += '<strong>Validações ativas:</strong><br>'
                for validacao in validacoes:
                    html += f"• {validacao}<br>"
                html += '</div>'
                return format_html(html)
            return "Nenhuma validação específica"
        except (TypeError, AttributeError):
            return "Erro ao carregar validações"
    get_validacoes_display.short_description = 'Validações'


class RespostaQuestaoInlineAtendimento(admin.TabularInline):
    """Inline para respostas dentro do atendimento"""
    model = RespostaQuestao
    fields = ('questao', 'resposta', 'valida', 'tentativas', 'data_resposta')
    readonly_fields = ('data_resposta',)
    extra = 0
    show_change_link = True
    ordering = ['questao__indice']


@admin.register(AtendimentoFluxo)
class AtendimentoFluxoAdmin(admin.ModelAdmin):
    list_display = [
        'lead',
        'fluxo',
        'status_badge',
        'questao_atual',
        'get_progresso_display',
        'get_tempo_formatado',
        'score_qualificacao',
        'data_inicio'
    ]
    list_filter = [
        'status',
        'fluxo',
        'fluxo__tipo_fluxo',
        'data_inicio',
        'data_conclusao',
        'score_qualificacao'
    ]
    search_fields = [
        'lead__nome_razaosocial',
        'lead__email',
        'lead__telefone',
        'fluxo__nome',
        'id_externo'
    ]
    readonly_fields = [
        'data_inicio',
        'data_ultima_atividade',
        'data_conclusao',
        'get_progresso_display',
        'get_tempo_formatado',
        'get_respostas_formatadas_display',
        'get_estatisticas_display'
    ]
    fieldsets = (
        ('Atendimento', {
            'fields': (
                'lead',
                'fluxo',
                'status',
                'id_externo'
            )
        }),
        ('Progresso', {
            'fields': (
                'questao_atual',
                'total_questoes',
                'questoes_respondidas',
                'get_progresso_display'
            )
        }),
        ('Tempo', {
            'fields': (
                'data_inicio',
                'data_ultima_atividade',
                'data_conclusao',
                'get_tempo_formatado'
            )
        }),
        ('Controle', {
            'fields': (
                'tentativas_atual',
                'max_tentativas',
                'score_qualificacao'
            )
        }),
        ('Dados', {
            'fields': (
                'dados_respostas',
                'observacoes',
                'resultado_final'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': (
                'ip_origem',
                'user_agent',
                'dispositivo'
            ),
            'classes': ('collapse',)
        }),
        ('Respostas', {
            'fields': ('get_respostas_formatadas_display',),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('get_estatisticas_display',),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_inicio'
    ordering = ['-data_inicio']
    list_per_page = 25
    inlines = [RespostaQuestaoInlineAtendimento]
    save_on_top = True
    autocomplete_fields = ['lead', 'fluxo', 'historico_contato']
    list_select_related = ['lead', 'fluxo']
    actions = ['reiniciar_atendimentos', 'finalizar_atendimentos', 'calcular_scores']
    
    def status_badge(self, obj):
        colors = {
            'iniciado': '#3498db',
            'em_andamento': '#2ecc71',
            'pausado': '#f39c12',
            'completado': '#27ae60',
            'abandonado': '#e74c3c',
            'erro': '#c0392b',
            'cancelado': '#95a5a6',
            'aguardando_validacao': '#8e44ad',
            'validado': '#16a085',
            'rejeitado': '#d35400',
        }
        color = colors.get(obj.status, '#7f8c8d')
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;background:{};color:#fff;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def get_progresso_display(self, obj):
        try:
            progresso = obj.get_progresso_percentual()
        except (TypeError, AttributeError):
            progresso = 0
            
        if progresso == 0:
            color = '#95a5a6'
        elif progresso < 50:
            color = '#e74c3c'
        elif progresso < 80:
            color = '#f39c12'
        else:
            color = '#2ecc71'
        
        return format_html(
            '<div style="background:#f8f9fa;padding:4px;border-radius:4px;border:1px solid #dee2e6;">'
            '<div style="background:{};height:20px;border-radius:3px;width:{}%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:bold;">'
            '{}%</div></div>',
            color, progresso, progresso
        )
    get_progresso_display.short_description = 'Progresso'
    
    def get_tempo_formatado(self, obj):
        try:
            return obj.get_tempo_formatado()
        except (TypeError, AttributeError):
            return "N/A"
    get_tempo_formatado.short_description = 'Tempo'
    get_tempo_formatado.admin_order_field = 'tempo_total'
    
    def get_respostas_formatadas_display(self, obj):
        if not obj.pk:
            return "Salve o atendimento para ver respostas"
        
        try:
            respostas = obj.get_respostas_formatadas()
        except (TypeError, AttributeError):
            return "Erro ao carregar respostas"
            
        if not respostas:
            return "Nenhuma resposta registrada"
        
        html = '<div style="background:#f8f9fa;padding:15px;border-radius:8px;border:1px solid #dee2e6;">'
        html += '<h4 style="margin-top:0;color:#495057;">📝 Respostas do Usuário</h4>'
        
        for resp in respostas:
            status_icon = "✅" if resp['respondida'] else "❌"
            status_color = "#2ecc71" if resp['respondida'] else "#e74c3c"
            
            html += f'''
            <div style="margin-bottom:10px;padding:10px;background:#fff;border-radius:6px;border-left:4px solid {status_color};">
                <strong>{status_icon} Q{resp['indice']}: {resp['questao']}</strong><br>
                <span style="color:#666;font-size:12px;">Resposta: {resp['resposta']}</span><br>
                <span style="color:#999;font-size:11px;">Data: {resp['data_resposta'] or 'Não respondida'}</span>
            </div>
            '''
        
        html += '</div>'
        return format_html(html)
    get_respostas_formatadas_display.short_description = 'Respostas'
    
    def get_estatisticas_display(self, obj):
        if not obj.pk:
            return "Salve o atendimento para ver estatísticas"
        
        try:
            progresso = obj.get_progresso_percentual()
            tempo_formatado = obj.get_tempo_formatado()
        except (TypeError, AttributeError):
            progresso = 0
            tempo_formatado = "N/A"
        
        html = f'''
        <div style="background:#f8f9fa;padding:15px;border-radius:8px;border:1px solid #dee2e6;">
            <h4 style="margin-top:0;color:#495057;">📊 Estatísticas do Atendimento</h4>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
                <div>
                    <strong>Status:</strong> {obj.get_status_display()}<br>
                    <strong>Questão Atual:</strong> {obj.questao_atual}<br>
                    <strong>Progresso:</strong> {progresso}%
                </div>
                <div>
                    <strong>Questões Respondidas:</strong> {obj.questoes_respondidas}/{obj.total_questoes}<br>
                    <strong>Tempo Total:</strong> {tempo_formatado}<br>
                    <strong>Score:</strong> {obj.score_qualificacao or 'N/A'}/10
                </div>
            </div>
        </div>
        '''
        return format_html(html)
    get_estatisticas_display.short_description = 'Estatísticas'
    
    # Ações em massa
    def reiniciar_atendimentos(self, request, queryset):
        count = 0
        for atendimento in queryset:
            if atendimento.pode_ser_reiniciado():
                if atendimento.reiniciar_atendimento():
                    count += 1
        
        if count > 0:
            self.message_user(request, f"{count} atendimento(s) reiniciado(s) com sucesso.")
        else:
            self.message_user(request, "Nenhum atendimento pode ser reiniciado.")
    reiniciar_atendimentos.short_description = 'Reiniciar selecionados'
    
    def finalizar_atendimentos(self, request, queryset):
        count = 0
        for atendimento in queryset:
            if atendimento.status not in ['completado', 'abandonado', 'cancelado']:
                atendimento.finalizar_atendimento(sucesso=True)
                count += 1
        
        if count > 0:
            self.message_user(request, f"{count} atendimento(s) finalizado(s) com sucesso.")
        else:
            self.message_user(request, "Nenhum atendimento pode ser finalizado.")
    finalizar_atendimentos.short_description = 'Finalizar selecionados'
    
    def calcular_scores(self, request, queryset):
        count = 0
        for atendimento in queryset:
            if atendimento.status == 'completado' and not atendimento.score_qualificacao:
                atendimento.atualizar_score_conversao()
                count += 1
        
        if count > 0:
            self.message_user(request, f"{count} score(s) calculado(s) com sucesso.")
        else:
            self.message_user(request, "Nenhum score pode ser calculado.")
    calcular_scores.short_description = 'Calcular scores'


@admin.register(RespostaQuestao)
class RespostaQuestaoAdmin(admin.ModelAdmin):
    list_display = [
        'atendimento',
        'questao',
        'resposta_truncada',
        'valida_badge',
        'tentativas',
        'get_tempo_resposta_formatado',
        'data_resposta'
    ]
    list_filter = [
        'valida',
        'tentativas',
        'data_resposta',
        'questao__tipo_questao',
        'atendimento__fluxo'
    ]
    search_fields = [
        'resposta',
        'atendimento__lead__nome_razaosocial',
        'questao__titulo'
    ]
    readonly_fields = [
        'data_resposta',
        'get_tempo_resposta_formatado'
    ]
    fieldsets = (
        ('Resposta', {
            'fields': (
                'atendimento',
                'questao',
                'resposta',
                'resposta_processada'
            )
        }),
        ('Validação', {
            'fields': (
                'valida',
                'mensagem_erro',
                'tentativas'
            )
        }),
        ('Tempo', {
            'fields': (
                'data_resposta',
                'tempo_resposta',
                'get_tempo_resposta_formatado'
            )
        }),
        ('Auditoria', {
            'fields': (
                'ip_origem',
                'user_agent',
                'dados_extras'
            ),
            'classes': ('collapse',)
        })
    )
    date_hierarchy = 'data_resposta'
    ordering = ['-data_resposta']
    list_per_page = 25
    autocomplete_fields = ['atendimento', 'questao']
    list_select_related = ['atendimento', 'questao', 'atendimento__lead', 'atendimento__fluxo']
    save_on_top = True
    
    def resposta_truncada(self, obj):
        if len(obj.resposta) > 50:
            return f"{obj.resposta[:50]}..."
        return obj.resposta
    resposta_truncada.short_description = 'Resposta'
    resposta_truncada.admin_order_field = 'resposta'
    
    def valida_badge(self, obj):
        if obj.valida:
            return format_html('<span style="color:#2ecc71;font-weight:600;">✓ Válida</span>')
        return format_html('<span style="color:#e74c3c;font-weight:600;">✗ Inválida</span>')
    valida_badge.short_description = 'Válida'
    valida_badge.admin_order_field = 'valida'
    
    def get_tempo_resposta_formatado(self, obj):
        try:
            return obj.get_tempo_resposta_formatado()
        except (TypeError, AttributeError):
            return "N/A"
    get_tempo_resposta_formatado.short_description = 'Tempo de Resposta'
    get_tempo_resposta_formatado.admin_order_field = 'tempo_resposta'

# ============================================================================
# ADMIN PARA MODELOS DE CADASTRO
# ============================================================================

@admin.register(ConfiguracaoCadastro)
class ConfiguracaoCadastroAdmin(admin.ModelAdmin):
    list_display = [
        'empresa',
        'titulo_pagina',
        'mostrar_selecao_plano',
        'criar_lead_automatico',
        'ativo',
        'data_atualizacao'
    ]
    list_filter = [
        'ativo',
        'mostrar_selecao_plano',
        'criar_lead_automatico',
        'validar_cep',
        'validar_cpf'
    ]
    search_fields = ['empresa', 'titulo_pagina']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Configurações Gerais', {
            'fields': [
                'empresa',
                'titulo_pagina',
                'subtitulo_pagina',
                'ativo'
            ]
        }),
        ('Contato e Suporte', {
            'fields': [
                'telefone_suporte',
                'whatsapp_suporte',
                'email_suporte'
            ]
        }),
        ('Configurações de Planos', {
            'fields': [
                'mostrar_selecao_plano',
                'plano_padrao'
            ]
        }),
        ('Campos Obrigatórios', {
            'fields': [
                'cpf_obrigatorio',
                'email_obrigatorio',
                'telefone_obrigatorio',
                'endereco_obrigatorio'
            ]
        }),
        ('Validações', {
            'fields': [
                'validar_cep',
                'validar_cpf'
            ]
        }),
        ('Configurações de Fluxo', {
            'fields': [
                'mostrar_progress_bar',
                'numero_etapas'
            ]
        }),
        ('Mensagens', {
            'fields': [
                'mensagem_sucesso',
                'instrucoes_pos_cadastro'
            ]
        }),
        ('Integração', {
            'fields': [
                'criar_lead_automatico',
                'origem_lead_padrao'
            ]
        }),
        ('Notificações', {
            'fields': [
                'enviar_email_confirmacao',
                'enviar_whatsapp_confirmacao'
            ]
        }),
        ('Segurança', {
            'fields': [
                'captcha_obrigatorio',
                'limite_tentativas_dia'
            ]
        }),
        ('Metadados', {
            'fields': [
                'data_criacao',
                'data_atualizacao'
            ],
            'classes': ('collapse',)
        })
    )
    
    save_on_top = True


@admin.register(PlanoInternet)
class PlanoInternetAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'velocidade_download',
        'velocidade_upload',
        'valor_mensal',
        'destaque',
        'ativo',
        'ordem_exibicao'
    ]
    list_filter = [
        'ativo',
        'destaque',
        'wifi_6',
        'suporte_prioritario',
        'suporte_24h',
        'upload_simetrico'
    ]
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo', 'ordem_exibicao']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': [
                'nome',
                'descricao',
                'ativo'
            ]
        }),
        ('Velocidades', {
            'fields': [
                'velocidade_download',
                'velocidade_upload',
                'upload_simetrico'
            ]
        }),
        ('Preço', {
            'fields': [
                'valor_mensal',
                'id_sistema_externo'
            ]
        }),
        ('Características', {
            'fields': [
                'wifi_6',
                'suporte_prioritario',
                'suporte_24h'
            ]
        }),
        ('Exibição', {
            'fields': [
                'destaque',
                'ordem_exibicao'
            ]
        }),
        ('Metadados', {
            'fields': [
                'data_criacao',
                'data_atualizacao'
            ],
            'classes': ('collapse',)
        })
    )
    
    save_on_top = True


@admin.register(OpcaoVencimento)
class OpcaoVencimentoAdmin(admin.ModelAdmin):
    list_display = [
        'dia_vencimento',
        'descricao',
        'ordem_exibicao',
        'ativo'
    ]
    list_filter = ['ativo']
    list_editable = ['ativo', 'ordem_exibicao']
    ordering = ['ordem_exibicao', 'dia_vencimento']
    
    fieldsets = (
        ('Configuração', {
            'fields': [
                'dia_vencimento',
                'descricao',
                'ordem_exibicao',
                'ativo'
            ]
        }),
    )


@admin.register(CadastroCliente)
class CadastroClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo',
        'email',
        'telefone',
        'plano_selecionado',
        'status',
        'data_inicio',
        'lead_gerado'
    ]
    list_filter = [
        'status',
        'origem_cadastro',
        'data_inicio',
        'plano_selecionado'
    ]
    search_fields = [
        'nome_completo',
        'cpf',
        'email',
        'telefone',
        'cidade'
    ]
    readonly_fields = [
        'data_inicio',
        'data_finalizacao',
        'tempo_total_cadastro',
        'ip_cliente',
        'user_agent',
        'get_progresso_percentual',
        'get_etapa_atual'
    ]
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': [
                'nome_completo',
                'cpf',
                'email',
                'telefone',
                'data_nascimento'
            ]
        }),
        ('Endereço', {
            'fields': [
                'cep',
                'endereco',
                'numero',
                'bairro',
                'cidade',
                'estado'
            ]
        }),
        ('Plano e Vencimento', {
            'fields': [
                'plano_selecionado',
                'vencimento_selecionado'
            ]
        }),
        ('Status e Progresso', {
            'fields': [
                'status',
                'get_progresso_percentual',
                'get_etapa_atual',
                'data_inicio',
                'data_finalizacao',
                'tempo_total_cadastro'
            ]
        }),
        ('Integração', {
            'fields': [
                'lead_gerado',
                'origem_cadastro'
            ]
        }),
        ('Metadados', {
            'fields': [
                'ip_cliente',
                'user_agent'
            ],
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': [
                'tentativas_etapa',
                'campos_preenchidos',
                'erros_validacao'
            ],
            'classes': ('collapse',)
        })
    )
    
    actions = ['finalizar_cadastro', 'gerar_lead']
    
    def finalizar_cadastro(self, request, queryset):
        """Ação para finalizar cadastros selecionados"""
        count = 0
        for cadastro in queryset:
            if cadastro.status != 'finalizado':
                if cadastro.finalizar_cadastro():
                    count += 1
        
        self.message_user(
            request,
            f'{count} cadastro(s) finalizado(s) com sucesso.'
        )
    finalizar_cadastro.short_description = "Finalizar cadastros selecionados"
    
    def gerar_lead(self, request, queryset):
        """Ação para gerar leads para cadastros selecionados"""
        count = 0
        for cadastro in queryset:
            if not cadastro.lead_gerado:
                if cadastro.gerar_lead():
                    count += 1
        
        self.message_user(
            request,
            f'{count} lead(s) gerado(s) com sucesso.'
        )
    gerar_lead.short_description = "Gerar leads para cadastros selecionados"
    
    save_on_top = True
