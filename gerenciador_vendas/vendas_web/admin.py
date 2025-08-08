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


@admin.register(LeadProspecto)
class LeadProspectoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_razaosocial', 
        'email', 
        'telefone', 
        'origem', 
        'get_valor_formatado', 
        'status_api', 
        'data_cadastro',
        'ativo'
    ]
    list_filter = [
        'origem', 
        'status_api', 
        'ativo', 
        'data_cadastro', 
        'estado'
    ]
    search_fields = [
        'nome_razaosocial', 
        'email', 
        'telefone', 
        'empresa', 
        'cpf_cnpj'
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
                'empresa'
            )
        }),
        ('Documentos e Localização', {
            'fields': (
                'cpf_cnpj', 
                'endereco', 
                'cidade', 
                'estado', 
                'cep'
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
    
    def get_valor_formatado(self, obj):
        return obj.get_valor_formatado()
    get_valor_formatado.short_description = 'Valor'
    get_valor_formatado.admin_order_field = 'valor'


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
