from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    LeadProspecto, 
    Prospecto, 
    HistoricoContato, 
    ConfiguracaoSistema, 
    LogSistema
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
    inlines = [ProspectoInline, HistoricoContatoInline]
    save_on_top = True
    actions = ['ativar_leads', 'inativar_leads', 'exportar_csv']
    
    def get_valor_formatado(self, obj):
        return obj.get_valor_formatado()
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
        return obj.get_tempo_processamento_formatado()
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
        return obj.get_duracao_formatada()
    get_duracao_formatada.short_description = 'Duração'
    get_duracao_formatada.admin_order_field = 'duracao_segundos'
    
    def get_tempo_relativo(self, obj):
        return obj.get_tempo_relativo()
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
