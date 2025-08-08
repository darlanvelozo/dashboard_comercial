from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from decimal import Decimal


class LeadProspecto(models.Model):
    """
    Modelo para armazenar informações de leads e prospectos
    """
    STATUS_API_CHOICES = [
        ('pendente', 'Pendente'),
        ('processado', 'Processado'),
        ('erro', 'Erro'),
        ('sucesso', 'Sucesso'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    ORIGEM_CHOICES = [
        ('site', 'Site'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('google', 'Google Ads'),
        ('whatsapp', 'WhatsApp'),
        ('indicacao', 'Indicação'),
        ('telefone', 'Telefone'),
        ('email', 'Email'),
        ('outros', 'Outros'),
    ]
    
    # Campos principais
    nome_razaosocial = models.CharField(
        max_length=255,
        verbose_name="Nome/Razão Social",
        help_text="Nome completo ou razão social do cliente"
    )
    
    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator()],
        verbose_name="Email",
        help_text="Email válido do cliente"
    )
    
    telefone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    telefone = models.CharField(
        validators=[telefone_validator],
        max_length=17,
        verbose_name="Telefone",
        help_text="Telefone de contato"
    )
    
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal('0.00'),
        verbose_name="Valor",
        help_text="Valor em reais associado ao lead"
    )
    
    empresa = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Empresa",
        help_text="Nome da empresa do cliente"
    )
    
    origem = models.CharField(
        max_length=50,
        choices=ORIGEM_CHOICES,
        default='site',
        verbose_name="Origem",
        help_text="Canal de origem do lead"
    )
    
    data_cadastro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Cadastro",
        help_text="Data e hora do cadastro"
    )
    
    status_api = models.CharField(
        max_length=20,
        choices=STATUS_API_CHOICES,
        default='pendente',
        verbose_name="Status API",
        help_text="Status do processamento na API"
    )
    
    # Campos adicionais para completar o modelo
    cpf_cnpj = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        verbose_name="CPF/CNPJ",
        help_text="CPF ou CNPJ do cliente"
    )
    
    endereco = models.TextField(
        null=True,
        blank=True,
        verbose_name="Endereço",
        help_text="Endereço completo do cliente"
    )
    
    cidade = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Cidade"
    )
    
    estado = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name="Estado",
        help_text="UF do estado"
    )
    
    cep = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="CEP"
    )
    
    observacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observações",
        help_text="Observações adicionais sobre o lead"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o lead está ativo"
    )
    
    class Meta:
        db_table = 'leads_prospectos'
        verbose_name = "Lead/Prospecto"
        verbose_name_plural = "Leads/Prospectos"
        ordering = ['-data_cadastro']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['telefone']),
            models.Index(fields=['data_cadastro']),
            models.Index(fields=['status_api']),
            models.Index(fields=['origem']),
        ]
    
    def __str__(self):
        return f"{self.nome_razaosocial} - {self.email}"
    
    def get_valor_formatado(self):
        """Retorna o valor formatado em reais"""
        if self.valor:
            return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"

class Prospecto(models.Model):
    """
    Modelo para controle de processamento de prospectos
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('processado', 'Processado'),
        ('erro', 'Erro'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Referência ao lead original (opcional)
    lead = models.ForeignKey(
        LeadProspecto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='prospectos',
        verbose_name="Lead Relacionado"
    )
    
    nome_prospecto = models.CharField(
        max_length=255,
        verbose_name="Nome do Prospecto"
    )
    
    id_prospecto_hubsoft = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        verbose_name="ID Prospecto Hubsoft",
        help_text="ID único no sistema Hubsoft"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status",
        help_text="Status atual do processamento"
    )
    
    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Criação"
    )
    
    data_processamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Processamento",
        help_text="Data e hora do último processamento"
    )
    
    tentativas_processamento = models.PositiveIntegerField(
        default=0,
        verbose_name="Tentativas de Processamento",
        help_text="Número de tentativas de processamento"
    )
    
    tempo_processamento = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Tempo de Processamento",
        help_text="Tempo de processamento em segundos"
    )
    
    erro_processamento = models.TextField(
        null=True,
        blank=True,
        verbose_name="Erro de Processamento",
        help_text="Detalhes do erro durante o processamento"
    )
    
    # Campos adicionais
    prioridade = models.PositiveIntegerField(
        default=1,
        verbose_name="Prioridade",
        help_text="Prioridade do processamento (1=baixa, 5=alta)"
    )
    
    dados_processamento = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Dados de Processamento",
        help_text="Dados JSON com informações do processamento"
    )
    
    resultado_processamento = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Resultado do Processamento",
        help_text="Resultado JSON do processamento"
    )
    
    class Meta:
        db_table = 'prospectos'
        verbose_name = "Prospecto"
        verbose_name_plural = "Prospectos"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['data_criacao']),
            models.Index(fields=['id_prospecto_hubsoft']),
            models.Index(fields=['tentativas_processamento']),
        ]
    
    def __str__(self):
        return f"{self.nome_prospecto} - {self.status}"
    
    def get_tempo_processamento_formatado(self):
        """Retorna o tempo de processamento formatado"""
        if self.tempo_processamento:
            if self.tempo_processamento < 60:
                return f"{self.tempo_processamento:.1f}s"
            else:
                minutos = int(self.tempo_processamento // 60)
                segundos = self.tempo_processamento % 60
                return f"{minutos}m {segundos:.1f}s"
        return "N/A"

class HistoricoContato(models.Model):
    """
    Modelo para histórico de contatos/chamadas
    """
    STATUS_CHOICES = [
        ('fluxo_inicializado', 'Fluxo Inicializado'),
        ('fluxo_finalizado', 'Fluxo Finalizado'),
        ('transferido_humano', 'Transferido para Humano'),
        ('chamada_perdida', 'Chamada Perdida'),
        ('ocupado', 'Ocupado'),
        ('desligou', 'Desligou'),
        ('nao_atendeu', 'Não Atendeu'),
        ('erro_sistema', 'Erro do Sistema'),
    ]
    
    # Relacionamento opcional com lead
    lead = models.ForeignKey(
        LeadProspecto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='historico_contatos',
        verbose_name="Lead Relacionado"
    )
    
    telefone = models.CharField(
        max_length=17,
        verbose_name="Telefone",
        help_text="Número de telefone do contato"
    )
    
    data_hora_contato = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data/Hora do Contato"
    )
    
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        verbose_name="Status do Contato"
    )
    
    nome_contato = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Nome do Contato",
        help_text="Nome identificado durante o contato"
    )
    
    # Campos adicionais para melhor controle
    duracao_segundos = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Duração (segundos)",
        help_text="Duração da chamada em segundos"
    )
    
    transcricao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Transcrição",
        help_text="Transcrição da conversa"
    )
    
    observacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observações",
        help_text="Observações sobre o contato"
    )
    
    ip_origem = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP de Origem",
        help_text="IP de onde partiu a chamada"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent",
        help_text="User agent do sistema que fez a chamada"
    )
    
    dados_extras = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Dados Extras",
        help_text="Dados JSON com informações extras do contato"
    )
    
    sucesso = models.BooleanField(
        default=False,
        verbose_name="Sucesso",
        help_text="Indica se o contato foi bem-sucedido"
    )
    
    class Meta:
        db_table = 'historico_contato'
        verbose_name = "Histórico de Contato"
        verbose_name_plural = "Histórico de Contatos"
        ordering = ['-data_hora_contato']
        indexes = [
            models.Index(fields=['telefone']),
            models.Index(fields=['data_hora_contato']),
            models.Index(fields=['status']),
            models.Index(fields=['sucesso']),
        ]
    
    def __str__(self):
        return f"{self.telefone} - {self.status} - {self.data_hora_contato.strftime('%d/%m/%Y %H:%M')}"
    
    def get_duracao_formatada(self):
        """Retorna a duração formatada"""
        if self.duracao_segundos:
            if self.duracao_segundos < 60:
                return f"{self.duracao_segundos}s"
            else:
                minutos = self.duracao_segundos // 60
                segundos = self.duracao_segundos % 60
                return f"{minutos}m {segundos}s"
        return "N/A"
    
    def get_tempo_relativo(self):
        """Retorna o tempo relativo do contato"""
        from django.utils.timesince import timesince
        return timesince(self.data_hora_contato)

class ConfiguracaoSistema(models.Model):
    """
    Modelo para configurações gerais do sistema
    """
    chave = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Chave",
        help_text="Chave única da configuração"
    )
    
    valor = models.TextField(
        verbose_name="Valor",
        help_text="Valor da configuração"
    )
    
    descricao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição da configuração"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('boolean', 'Boolean'),
            ('json', 'JSON'),
            ('decimal', 'Decimal'),
        ],
        default='string',
        verbose_name="Tipo",
        help_text="Tipo do valor da configuração"
    )
    
    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    class Meta:
        db_table = 'configuracao_sistema'
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"
        ordering = ['chave']
    
    def __str__(self):
        return f"{self.chave}: {self.valor[:50]}"

class LogSistema(models.Model):
    """
    Modelo para logs do sistema
    """
    NIVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    nivel = models.CharField(
        max_length=10,
        choices=NIVEL_CHOICES,
        default='INFO',
        verbose_name="Nível"
    )
    
    modulo = models.CharField(
        max_length=100,
        verbose_name="Módulo",
        help_text="Módulo/função que gerou o log"
    )
    
    mensagem = models.TextField(
        verbose_name="Mensagem"
    )
    
    dados_extras = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Dados Extras",
        help_text="Dados JSON com informações extras"
    )
    
    usuario = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Usuário",
        help_text="Usuário relacionado ao log"
    )
    
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP"
    )
    
    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        db_table = 'log_sistema'
        verbose_name = "Log do Sistema"
        verbose_name_plural = "Logs do Sistema"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['nivel']),
            models.Index(fields=['data_criacao']),
            models.Index(fields=['modulo']),
        ]
    
    def __str__(self):
        return f"{self.nivel} - {self.modulo} - {self.data_criacao.strftime('%d/%m/%Y %H:%M')}"