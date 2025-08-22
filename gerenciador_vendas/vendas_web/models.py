from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


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
        ('aguardando_retry', 'Aguardando Retry'),
        ('processamento_manual', 'Processamento Manual'),
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
    
    TIPO_ENTRADA_CHOICES = [
        ('contato_whatsapp', 'Contato WhatsApp'),
        ('cadastro_site', 'Cadastro Site'),
        ('telefone', 'Telefone'),
        ('formulario', 'Formulário'),
        ('importacao', 'Importação'),
        ('api_externa', 'API Externa'),
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
        help_text="Email válido do cliente",
        null=True,
        blank=True
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
        default='pendente',
        verbose_name="Status API",
        help_text="Status do processamento na API"
    )
    
    # Identificador no Hubsoft para cruzamento automático com Prospecto
    id_hubsoft = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="ID Hubsoft",
        help_text="Identificador do lead no Hubsoft para relacionar automaticamente com prospectos",
        db_index=True,
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
    
    rua = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Rua",
        help_text="Logradouro do endereço"
    )
    
    numero_residencia = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Número da Residência",
        help_text="Número do endereço"
    )
    
    bairro = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="Bairro",
        help_text="Bairro do endereço"
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

    # Dados adicionais de relacionamento com RP/Comercial
    id_plano_rp = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID Plano (RP)",
        help_text="Identificador do plano no sistema RP"
    )
    
    id_dia_vencimento = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID Dia de Vencimento",
        help_text="Identificador do dia de vencimento no RP"
    )
    
    id_vendedor_rp = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID Vendedor (RP)",
        help_text="Identificador do vendedor no sistema RP"
    )
    
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento"
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
    
    # Novos campos para rastreamento melhorado
    canal_entrada = models.CharField(
        max_length=50,
        choices=ORIGEM_CHOICES,
        null=True,
        blank=True,
        verbose_name="Canal de Entrada",
        help_text="Canal por onde o lead entrou no sistema"
    )
    
    tipo_entrada = models.CharField(
        max_length=50,
        choices=TIPO_ENTRADA_CHOICES,
        null=True,
        blank=True,
        verbose_name="Tipo de Entrada",
        help_text="Tipo específico de entrada no sistema"
    )
    
    score_qualificacao = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Score de Qualificação",
        help_text="Score de 1 a 10 baseado na qualificação do lead"
    )
    
    tentativas_contato = models.PositiveIntegerField(
        default=0,
        verbose_name="Tentativas de Contato",
        help_text="Número de tentativas de contato realizadas"
    )
    
    data_ultimo_contato = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data do Último Contato"
    )
    
    motivo_rejeicao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Motivo da Rejeição",
        help_text="Motivo detalhado caso tenha sido rejeitado"
    )
    
    custo_aquisicao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Custo de Aquisição",
        help_text="Custo investido para adquirir este lead"
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
            models.Index(fields=['id_hubsoft']),
            # Novos índices para campos adicionados
            models.Index(fields=['canal_entrada']),
            models.Index(fields=['tipo_entrada']),
            models.Index(fields=['score_qualificacao']),
            models.Index(fields=['data_ultimo_contato']),
            models.Index(fields=['tentativas_contato']),
            # Índices compostos para consultas mais eficientes
            models.Index(fields=['canal_entrada', 'data_cadastro']),
            models.Index(fields=['score_qualificacao', 'status_api']),
            models.Index(fields=['tipo_entrada', 'ativo']),
            models.Index(fields=['data_ultimo_contato', 'tentativas_contato']),
        ]
    
    def __str__(self):
        return f"{self.nome_razaosocial} - {self.email}"

    def get_status_api_display(self):  # compatível com chamadas existentes
        try:
            return StatusConfiguravel.get_label('lead_status_api', self.status_api)
        except Exception:
            # fallback para rótulo definido em STATUS_API_CHOICES se existir
            mapping = dict(self.STATUS_API_CHOICES)
            return mapping.get(self.status_api, self.status_api)
    
    def get_valor_formatado(self):
        """Retorna o valor formatado em reais"""
        if self.valor:
            return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    
    def get_historico_contatos_relacionados(self):
        """
        Retorna o histórico de contatos relacionados a este lead/prospecto
        Busca por telefone e também por relacionamento direto
        """
        contatos_diretos = self.historico_contatos.all()
        contatos_por_telefone = HistoricoContato.objects.filter(
            telefone=self.telefone
        ).exclude(
            id__in=contatos_diretos.values_list('id', flat=True)
        )
        
        # Combina os dois querysets e ordena por data
        from django.db.models import Q
        todos_contatos = HistoricoContato.objects.filter(
            Q(lead=self) | Q(telefone=self.telefone)
        ).distinct().order_by('-data_hora_contato')
        
        return todos_contatos
    
    def get_primeiro_contato(self):
        """Retorna o primeiro contato relacionado a este lead"""
        contatos = self.get_historico_contatos_relacionados()
        return contatos.last() if contatos.exists() else None
    
    def get_ultimo_contato(self):
        """Retorna o último contato relacionado a este lead"""
        contatos = self.get_historico_contatos_relacionados()
        return contatos.first() if contatos.exists() else None
    
    def get_total_contatos(self):
        """Retorna o número total de contatos relacionados"""
        return self.get_historico_contatos_relacionados().count()
    
    def get_contatos_bem_sucedidos(self):
        """Retorna contatos que tiveram sucesso (finalizaram fluxo ou foram transferidos)"""
        return self.get_historico_contatos_relacionados().filter(
            status__in=['fluxo_finalizado', 'transferido_humano', 'convertido_lead', 'venda_confirmada']
        )
    
    def get_taxa_sucesso_contatos(self):
        """Calcula a taxa de sucesso dos contatos deste lead"""
        total = self.get_total_contatos()
        if total == 0:
            return 0
        sucessos = self.get_contatos_bem_sucedidos().count()
        return (sucessos / total) * 100
    
    def marcar_como_convertido_de_contato(self, contato_id):
        """
        Marca um contato específico como convertido em lead
        e atualiza o relacionamento
        """
        try:
            contato = HistoricoContato.objects.get(id=contato_id)
            contato.lead = self
            contato.converteu_lead = True
            contato.data_conversao_lead = timezone.now()
            contato.status = 'convertido_lead'
            contato.save()
            return True
        except HistoricoContato.DoesNotExist:
            return False
    
    # Novos métodos de business logic
    def calcular_score_qualificacao(self):
        """
        Calcula score de qualificação baseado em dados do lead
        Retorna valor entre 1 e 10
        """
        score = 5  # Score base
        
        # Fatores que aumentam o score
        if self.empresa:
            score += 1
        if self.valor and self.valor > 1000:
            score += 1
        if self.origem in ['indicacao', 'telefone']:
            score += 1
        if self.get_total_contatos() > 0:
            score += 1
        if self.get_taxa_sucesso_contatos() > 50:
            score += 1
            
        # Fatores que diminuem o score
        if self.tentativas_contato > 3:
            score -= 1
        if self.status_api == 'erro':
            score -= 1
        if self.motivo_rejeicao:
            score -= 2
            
        # Garantir que o score esteja entre 1 e 10
        return max(1, min(10, score))
    
    def pode_reprocessar(self):
        """
        Verifica se o lead pode ser reprocessado
        """
        if not self.ativo:
            return False
        if self.status_api == 'sucesso':
            return False
        if self.tentativas_contato >= 5:
            return False
        return True
    
    def incrementar_tentativa_contato(self, observacoes=None):
        """
        Incrementa contador de tentativas e atualiza data do último contato
        """
        self.tentativas_contato += 1
        self.data_ultimo_contato = timezone.now()
        if observacoes and not self.observacoes:
            self.observacoes = observacoes
        elif observacoes:
            self.observacoes += f"\n{timezone.now().strftime('%d/%m/%Y %H:%M')}: {observacoes}"
        
        # Atualizar score após tentativa
        self.score_qualificacao = self.calcular_score_qualificacao()
        self.save()
    
    def definir_canal_entrada_automatico(self):
        """
        Define canal_entrada baseado na origem se não estiver definido
        """
        if not self.canal_entrada:
            self.canal_entrada = self.origem
            self.save()
    
    def get_custo_aquisicao_formatado(self):
        """Retorna o custo de aquisição formatado em reais"""
        if self.custo_aquisicao:
            return f"R$ {self.custo_aquisicao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    
    def get_score_qualificacao_display(self):
        """Retorna descrição textual do score de qualificação"""
        if not self.score_qualificacao:
            return "Não avaliado"
        
        score_descriptions = {
            (1, 3): "Baixa Qualificação",
            (4, 6): "Qualificação Média",
            (7, 8): "Boa Qualificação",
            (9, 10): "Excelente Qualificação"
        }
        
        for range_tuple, description in score_descriptions.items():
            if range_tuple[0] <= self.score_qualificacao <= range_tuple[1]:
                return description
        return "Qualificação não definida"

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
        # Novos status para validação
        ('aguardando_validacao', 'Aguardando Validação'),
        ('validacao_aprovada', 'Validação Aprovada'),
        ('validacao_rejeitada', 'Validação Rejeitada'),
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
    
    # Novos campos para controle melhorado
    data_inicio_processamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data Início Processamento"
    )
    
    data_fim_processamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data Fim Processamento"
    )
    
    usuario_processamento = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Usuário que Processou"
    )
    
    score_conversao = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Score de Conversão",
        help_text="Probabilidade de conversão calculada (0-100%)"
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
            # Novos índices para campos adicionados
            models.Index(fields=['data_inicio_processamento']),
            models.Index(fields=['data_fim_processamento']),
            models.Index(fields=['usuario_processamento']),
            models.Index(fields=['score_conversao']),
            # Índices compostos para consultas mais eficientes
            models.Index(fields=['status', 'data_inicio_processamento']),
            models.Index(fields=['prioridade', 'data_criacao']),
            models.Index(fields=['score_conversao', 'status']),
        ]
    
    def __str__(self):
        return f"{self.nome_prospecto} - {self.status}"

    def get_status_display(self):  # compatível com chamadas existentes
        try:
            return StatusConfiguravel.get_label('prospecto_status', self.status)
        except Exception:
            mapping = dict(self.STATUS_CHOICES)
            return mapping.get(self.status, self.status)
    
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
    
    # Novos métodos de business logic
    def iniciar_processamento(self, usuario=None):
        """
        Marca início do processamento
        """
        self.status = 'processando'
        self.data_inicio_processamento = timezone.now()
        if usuario:
            self.usuario_processamento = usuario
        self.save()
    
    def finalizar_processamento(self, sucesso=True, erro=None, resultado=None):
        """
        Marca fim do processamento
        """
        self.data_fim_processamento = timezone.now()
        
        if sucesso:
            self.status = 'processado'
        else:
            self.status = 'erro'
            if erro:
                self.erro_processamento = erro
        
        if resultado:
            self.resultado_processamento = resultado
            
        # Calcular tempo de processamento
        if self.data_inicio_processamento:
            tempo_delta = self.data_fim_processamento - self.data_inicio_processamento
            self.tempo_processamento = tempo_delta.total_seconds()
            
        self.save()
    
    def calcular_tempo_processamento_total(self):
        """
        Calcula tempo total de processamento incluindo todas as tentativas
        """
        if self.data_inicio_processamento and self.data_fim_processamento:
            tempo_delta = self.data_fim_processamento - self.data_inicio_processamento
            return tempo_delta.total_seconds()
        return 0
    
    def pode_reprocessar(self):
        """
        Verifica se o prospecto pode ser reprocessado
        """
        return self.status in ['erro', 'pendente'] and self.tentativas_processamento < 3
    
    def incrementar_tentativa(self):
        """
        Incrementa tentativas de processamento
        """
        self.tentativas_processamento += 1
        self.save()
    
    def calcular_score_conversao_automatico(self):
        """
        Calcula score de conversão baseado nos dados disponíveis
        """
        if not self.lead:
            return 50.0  # Score padrão sem lead
            
        score = 50.0  # Base
        
        # Fatores do lead que influenciam conversão
        if self.lead.score_qualificacao:
            score += (self.lead.score_qualificacao - 5) * 5  # +/- 25 pontos baseado no score
            
        if self.lead.empresa:
            score += 10
            
        if self.lead.get_total_contatos() > 0:
            score += 15
            
        if self.lead.get_taxa_sucesso_contatos() > 70:
            score += 10
            
        # Fatores que diminuem
        if self.tentativas_processamento > 1:
            score -= self.tentativas_processamento * 5
            
        if self.status == 'erro':
            score -= 20
            
        return max(0, min(100, score))
    
    def atualizar_score_conversao(self):
        """
        Atualiza o score de conversão automaticamente
        """
        self.score_conversao = self.calcular_score_conversao_automatico()
        self.save()
    
    def get_score_conversao_display(self):
        """Retorna descrição textual do score de conversão"""
        if not self.score_conversao:
            return "Não calculado"
        
        if self.score_conversao >= 80:
            return f"{self.score_conversao:.1f}% - Muito Alta"
        elif self.score_conversao >= 60:
            return f"{self.score_conversao:.1f}% - Alta"
        elif self.score_conversao >= 40:
            return f"{self.score_conversao:.1f}% - Média"
        elif self.score_conversao >= 20:
            return f"{self.score_conversao:.1f}% - Baixa"
        else:
            return f"{self.score_conversao:.1f}% - Muito Baixa"

class HistoricoContato(models.Model):
    """
    Modelo para histórico de contatos/chamadas no funil de vendas
    Fluxo: Inicializado → Finalizado/Transferido → Lead/Prospecto → Venda
    """
    STATUS_CHOICES = [
        # Status principais do fluxo
        ('fluxo_inicializado', 'Fluxo Inicializado'),
        ('fluxo_finalizado', 'Fluxo Finalizado'),
        ('transferido_humano', 'Transferido para Humano'),
        
        # Status de abandono/problemas
        ('chamada_perdida', 'Chamada Perdida'),
        ('ocupado', 'Ocupado'),
        ('desligou', 'Desligou'),
        ('nao_atendeu', 'Não Atendeu'),
        ('abandonou_fluxo', 'Abandonou o Fluxo'),
        ('numero_invalido', 'Número Inválido'),
        ('erro_sistema', 'Erro do Sistema'),
        
        # Status de conversão
        ('convertido_lead', 'Convertido em Lead'),
        ('venda_confirmada', 'Venda Confirmada'),
        ('venda_rejeitada', 'Venda Rejeitada'),
        
        # Novos status expandidos
        ('venda_sem_viabilidade', 'Venda Sem Viabilidade'),
        ('cliente_desistiu', 'Cliente Desistiu'),
        ('aguardando_validacao', 'Aguardando Validação'),
        ('followup_agendado', 'Follow-up Agendado'),
        ('nao_qualificado', 'Não Qualificado'),
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
    
    # Campos para rastreamento do funil de vendas
    sucesso = models.BooleanField(
        default=False,
        verbose_name="Sucesso",
        help_text="Indica se o contato foi bem-sucedido"
    )
    
    converteu_lead = models.BooleanField(
        default=False,
        verbose_name="Converteu em Lead",
        help_text="Indica se este contato gerou um lead/prospecto"
    )
    
    data_conversao_lead = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conversão em Lead",
        help_text="Data quando foi convertido em lead/prospecto"
    )
    
    converteu_venda = models.BooleanField(
        default=False,
        verbose_name="Converteu em Venda",
        help_text="Indica se este lead se tornou uma venda confirmada"
    )
    
    data_conversao_venda = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conversão em Venda",
        help_text="Data quando foi confirmada a venda"
    )
    
    valor_venda = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor da Venda",
        help_text="Valor em reais da venda confirmada"
    )
    
    origem_contato = models.CharField(
        max_length=50,
        choices=LeadProspecto.ORIGEM_CHOICES,
        null=True,
        blank=True,
        verbose_name="Origem do Contato",
        help_text="Canal de origem do contato"
    )
    
    # Campo para identificar contatos relacionados (mesmo cliente, múltiplos contatos)
    identificador_cliente = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Identificador do Cliente",
        help_text="Hash ou ID único para agrupar contatos do mesmo cliente"
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
            models.Index(fields=['converteu_lead']),
            models.Index(fields=['converteu_venda']),
            models.Index(fields=['data_conversao_lead']),
            models.Index(fields=['data_conversao_venda']),
            models.Index(fields=['origem_contato']),
            models.Index(fields=['identificador_cliente']),
            # Índices compostos para consultas de funil
            models.Index(fields=['data_hora_contato', 'status']),
            models.Index(fields=['converteu_lead', 'data_conversao_lead']),
            models.Index(fields=['converteu_venda', 'data_conversao_venda']),
        ]
    
    def __str__(self):
        return f"{self.telefone} - {self.status} - {self.data_hora_contato.strftime('%d/%m/%Y %H:%M')}"

    def get_status_display(self):  # compatível com chamadas existentes
        try:
            return StatusConfiguravel.get_label('historico_status', self.status)
        except Exception:
            mapping = dict(self.STATUS_CHOICES)
            return mapping.get(self.status, self.status)


class StatusConfiguravel(models.Model):
    """
    Tabela para gerenciar valores de status/labels via admin.
    grupos esperados:
      - lead_status_api
      - prospecto_status
      - historico_status
    """
    GRUPO_CHOICES = [
        ('lead_status_api', 'Lead: Status API'),
        ('prospecto_status', 'Prospecto: Status'),
        ('historico_status', 'Histórico: Status'),
        ('atendimento_status', 'Atendimento: Status'),
        ('fluxo_status', 'Fluxo: Status'),
    ]

    grupo = models.CharField(max_length=50, choices=GRUPO_CHOICES, db_index=True)
    codigo = models.CharField(max_length=50, db_index=True)
    rotulo = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'status_configuravel'
        unique_together = [('grupo', 'codigo')]
        ordering = ['grupo', 'ordem', 'codigo']

    def __str__(self):
        return f"{self.grupo}:{self.codigo} -> {self.rotulo} ({'ativo' if self.ativo else 'inativo'})"

    @classmethod
    def get_label(cls, grupo: str, codigo: str) -> str:
        registro = cls.objects.filter(grupo=grupo, codigo=codigo, ativo=True).first()
        return registro.rotulo if registro else codigo
    
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
    
    def get_valor_venda_formatado(self):
        """Retorna o valor da venda formatado em reais"""
        if self.valor_venda:
            return f"R$ {self.valor_venda:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    
    def get_status_display_color(self):
        """Retorna cor para exibição do status no dashboard"""
        status_colors = {
            'fluxo_inicializado': '#3498db',  # Azul
            'fluxo_finalizado': '#2ecc71',    # Verde
            'transferido_humano': '#f39c12',  # Laranja
            'convertido_lead': '#9b59b6',     # Roxo
            'venda_confirmada': '#27ae60',    # Verde escuro
            'venda_rejeitada': '#e74c3c',     # Vermelho
            'abandonou_fluxo': '#95a5a6',     # Cinza
            'erro_sistema': '#e67e22',        # Laranja escuro
        }
        return status_colors.get(self.status, '#7f8c8d')  # Cinza padrão
    
    def is_contato_bem_sucedido(self):
        """Verifica se o contato foi bem-sucedido (finalizou fluxo ou foi transferido)"""
        return self.status in ['fluxo_finalizado', 'transferido_humano', 'convertido_lead', 'venda_confirmada']
    
    def is_conversao_completa(self):
        """Verifica se houve conversão completa (de contato até venda)"""
        return self.converteu_venda and self.valor_venda and self.valor_venda > 0
    
    @classmethod
    def get_funil_insights(cls, data_inicio=None, data_fim=None):
        """
        Retorna insights do funil de vendas para um período específico
        """
        from django.utils import timezone
        from django.db.models import Count, Sum, Q
        from datetime import datetime, timedelta
        
        # Se não especificado, usa últimos 30 dias
        if not data_fim:
            data_fim = timezone.now()
        if not data_inicio:
            data_inicio = data_fim - timedelta(days=30)
        
        queryset = cls.objects.filter(
            data_hora_contato__gte=data_inicio,
            data_hora_contato__lte=data_fim
        )
        
        insights = {
            'total_contatos': queryset.count(),
            'fluxos_inicializados': queryset.filter(status='fluxo_inicializado').count(),
            'fluxos_finalizados': queryset.filter(status='fluxo_finalizado').count(),
            'transferidos_humano': queryset.filter(status='transferido_humano').count(),
            'convertidos_lead': queryset.filter(converteu_lead=True).count(),
            'vendas_confirmadas': queryset.filter(converteu_venda=True).count(),
            'valor_total_vendas': queryset.filter(converteu_venda=True).aggregate(
                total=Sum('valor_venda')
            )['total'] or 0,
            'abandonos': queryset.filter(status__in=[
                'abandonou_fluxo', 'desligou', 'nao_atendeu', 'chamada_perdida'
            ]).count(),
        }
        
        # Cálculos de taxa de conversão
        if insights['fluxos_inicializados'] > 0:
            insights['taxa_finalizacao'] = (
                (insights['fluxos_finalizados'] + insights['transferidos_humano']) / 
                insights['fluxos_inicializados'] * 100
            )
        else:
            insights['taxa_finalizacao'] = 0
            
        if insights['convertidos_lead'] > 0:
            insights['taxa_conversao_venda'] = (
                insights['vendas_confirmadas'] / insights['convertidos_lead'] * 100
            )
        else:
            insights['taxa_conversao_venda'] = 0
            
        # Taxa de conversão geral (contato → venda)
        if insights['total_contatos'] > 0:
            insights['taxa_conversao_geral'] = (
                insights['vendas_confirmadas'] / insights['total_contatos'] * 100
            )
        else:
            insights['taxa_conversao_geral'] = 0
        
        return insights

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

class FluxoAtendimento(models.Model):
    """
    Modelo para definir fluxos de atendimento personalizáveis
    Cada fluxo pode ter múltiplas questões em ordem específica
    """
    TIPO_FLUXO_CHOICES = [
        ('qualificacao', 'Qualificação de Lead'),
        ('vendas', 'Vendas'),
        ('suporte', 'Suporte'),
        ('onboarding', 'Onboarding'),
        ('pesquisa', 'Pesquisa de Satisfação'),
        ('customizado', 'Customizado'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('rascunho', 'Rascunho'),
        ('teste', 'Em Teste'),
    ]
    
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Fluxo",
        help_text="Nome identificador do fluxo de atendimento"
    )
    
    descricao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada do fluxo"
    )
    
    tipo_fluxo = models.CharField(
        max_length=20,
        choices=TIPO_FLUXO_CHOICES,
        default='qualificacao',
        verbose_name="Tipo de Fluxo"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name="Status"
    )
    
    # Configurações do fluxo
    max_tentativas = models.PositiveIntegerField(
        default=3,
        verbose_name="Máximo de Tentativas",
        help_text="Número máximo de tentativas para completar o fluxo"
    )
    
    tempo_limite_minutos = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tempo Limite (minutos)",
        help_text="Tempo máximo para completar o fluxo (opcional)"
    )
    
    permite_pular_questoes = models.BooleanField(
        default=False,
        verbose_name="Permite Pular Questões",
        help_text="Se o usuário pode pular questões opcionais"
    )
    
    # Campos de controle
    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    criado_por = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Criado Por"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    class Meta:
        db_table = 'fluxos_atendimento'
        verbose_name = "Fluxo de Atendimento"
        verbose_name_plural = "Fluxos de Atendimento"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['tipo_fluxo']),
            models.Index(fields=['status']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_fluxo_display()})"
    
    def get_questoes_ordenadas(self):
        """Retorna questões ordenadas por índice"""
        return self.questoes.filter(ativo=True).order_by('indice')
    
    def get_total_questoes(self):
        """Retorna total de questões ativas"""
        return self.questoes.filter(ativo=True).count()
    
    def get_questao_por_indice(self, indice):
        """Retorna questão específica por índice"""
        return self.questoes.filter(indice=indice, ativo=True).first()
    
    def get_proxima_questao(self, indice_atual):
        """Retorna próxima questão após o índice atual"""
        return self.questoes.filter(
            indice__gt=indice_atual,
            ativo=True
        ).order_by('indice').first()
    
    def get_questao_anterior(self, indice_atual):
        """Retorna questão anterior ao índice atual"""
        return self.questoes.filter(
            indice__lt=indice_atual,
            ativo=True
        ).order_by('indice').last()
    
    def pode_ser_usado(self):
        """Verifica se o fluxo pode ser usado"""
        return self.status == 'ativo' and self.ativo and self.get_total_questoes() > 0
    
    def get_estatisticas(self):
        """Retorna estatísticas básicas do fluxo"""
        from django.db.models import Count, Avg
        
        atendimentos = self.atendimentos.all()
        total_atendimentos = atendimentos.count()
        atendimentos_completados = atendimentos.filter(status='completado').count()
        
        if total_atendimentos > 0:
            taxa_completacao = (atendimentos_completados / total_atendimentos) * 100
        else:
            taxa_completacao = 0
        
        tempo_medio = atendimentos.filter(
            tempo_total__isnull=False
        ).aggregate(
            tempo_medio=Avg('tempo_total')
        )['tempo_medio'] or 0
        
        return {
            'total_atendimentos': total_atendimentos,
            'atendimentos_completados': atendimentos_completados,
            'taxa_completacao': round(taxa_completacao, 2),
            'tempo_medio_segundos': round(tempo_medio, 2) if tempo_medio else 0,
        }


class QuestaoFluxo(models.Model):
    """
    Modelo para questões individuais dentro de um fluxo
    Cada questão tem tipo específico, validação e opções de resposta
    """
    TIPO_QUESTAO_CHOICES = [
        ('texto', 'Texto Livre'),
        ('numero', 'Número'),
        ('email', 'Email'),
        ('telefone', 'Telefone'),
        ('cpf_cnpj', 'CPF/CNPJ'),
        ('cep', 'CEP'),
        ('endereco', 'Endereço'),
        ('select', 'Seleção Única'),
        ('multiselect', 'Seleção Múltipla'),
        ('data', 'Data'),
        ('hora', 'Hora'),
        ('data_hora', 'Data e Hora'),
        ('boolean', 'Sim/Não'),
        ('escala', 'Escala (1-10)'),
        ('arquivo', 'Upload de Arquivo'),
    ]
    
    TIPO_VALIDACAO_CHOICES = [
        ('obrigatoria', 'Obrigatória'),
        ('opcional', 'Opcional'),
        ('condicional', 'Condicional'),
    ]
    
    fluxo = models.ForeignKey(
        FluxoAtendimento,
        on_delete=models.CASCADE,
        related_name='questoes',
        verbose_name="Fluxo"
    )
    
    indice = models.PositiveIntegerField(
        verbose_name="Índice",
        help_text="Ordem da questão no fluxo (1, 2, 3...)"
    )
    
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título da Questão",
        help_text="Texto da pergunta para o usuário"
    )
    
    descricao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descrição",
        help_text="Descrição adicional ou instruções"
    )
    
    tipo_questao = models.CharField(
        max_length=20,
        choices=TIPO_QUESTAO_CHOICES,
        default='texto',
        verbose_name="Tipo de Questão"
    )
    
    tipo_validacao = models.CharField(
        max_length=20,
        choices=TIPO_VALIDACAO_CHOICES,
        default='obrigatoria',
        verbose_name="Tipo de Validação"
    )
    
    # Configurações de resposta
    opcoes_resposta = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Opções de Resposta",
        help_text="Lista de opções para questões de seleção"
    )
    
    resposta_padrao = models.TextField(
        null=True,
        blank=True,
        verbose_name="Resposta Padrão",
        help_text="Resposta padrão ou placeholder"
    )
    
    # Validações
    regex_validacao = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Regex de Validação",
        help_text="Expressão regular para validação customizada"
    )
    
    tamanho_minimo = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tamanho Mínimo",
        help_text="Tamanho mínimo da resposta"
    )
    
    tamanho_maximo = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tamanho Máximo",
        help_text="Tamanho máximo da resposta"
    )
    
    valor_minimo = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Mínimo",
        help_text="Valor mínimo para questões numéricas"
    )
    
    valor_maximo = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Máximo",
        help_text="Valor máximo para questões numéricas"
    )
    
    # Lógica condicional
    questao_dependencia = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Questão de Dependência",
        help_text="Questão que deve ser respondida antes desta"
    )
    
    valor_dependencia = models.TextField(
        null=True,
        blank=True,
        verbose_name="Valor de Dependência",
        help_text="Valor específico da questão de dependência para mostrar esta"
    )
    
    # Campos de controle
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativa"
    )
    
    permite_voltar = models.BooleanField(
        default=True,
        verbose_name="Permite Voltar",
        help_text="Se o usuário pode voltar para esta questão"
    )
    
    permite_editar = models.BooleanField(
        default=True,
        verbose_name="Permite Editar",
        help_text="Se a resposta pode ser editada após enviada"
    )
    
    ordem_exibicao = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição",
        help_text="Ordem para exibição na interface"
    )
    
    class Meta:
        db_table = 'questoes_fluxo'
        verbose_name = "Questão do Fluxo"
        verbose_name_plural = "Questões do Fluxo"
        ordering = ['fluxo', 'indice']
        unique_together = [('fluxo', 'indice')]
        indexes = [
            models.Index(fields=['fluxo', 'indice']),
            models.Index(fields=['tipo_questao']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.fluxo.nome} - Q{self.indice}: {self.titulo}"
    
    def get_opcoes_formatadas(self):
        """Retorna opções de resposta formatadas"""
        if self.opcoes_resposta and isinstance(self.opcoes_resposta, list):
            return self.opcoes_resposta
        return []
    
    def validar_resposta(self, resposta):
        """
        Valida uma resposta baseada nas regras da questão
        Retorna (valido, mensagem_erro)
        """
        if not resposta and self.tipo_validacao == 'obrigatoria':
            return False, "Esta questão é obrigatória"
        
        if not resposta:
            return True, ""
        
        # Validação de tamanho
        if self.tamanho_minimo and len(str(resposta)) < self.tamanho_minimo:
            return False, f"Resposta deve ter pelo menos {self.tamanho_minimo} caracteres"
        
        if self.tamanho_maximo and len(str(resposta)) > self.tamanho_maximo:
            return False, f"Resposta deve ter no máximo {self.tamanho_maximo} caracteres"
        
        # Validação de regex
        if self.regex_validacao:
            import re
            if not re.match(self.regex_validacao, str(resposta)):
                return False, "Formato da resposta não é válido"
        
        # Validação de valores numéricos
        if self.tipo_questao == 'numero':
            try:
                valor = float(resposta)
                if self.valor_minimo is not None and valor < self.valor_minimo:
                    return False, f"Valor deve ser maior ou igual a {self.valor_minimo}"
                if self.valor_maximo is not None and valor > self.valor_maximo:
                    return False, f"Valor deve ser menor ou igual a {self.valor_maximo}"
            except ValueError:
                return False, "Resposta deve ser um número válido"
        
        # Validação de email
        if self.tipo_questao == 'email':
            from django.core.validators import EmailValidator
            validator = EmailValidator()
            try:
                validator(resposta)
            except:
                return False, "Email inválido"
        
        # Validação de opções
        if self.tipo_questao in ['select', 'multiselect'] and self.opcoes_resposta:
            if self.tipo_questao == 'select':
                if resposta not in self.opcoes_resposta:
                    return False, "Opção selecionada não é válida"
            else:  # multiselect
                if not isinstance(resposta, list):
                    return False, "Resposta deve ser uma lista de opções"
                for opcao in resposta:
                    if opcao not in self.opcoes_resposta:
                        return False, f"Opção '{opcao}' não é válida"
        
        return True, ""
    
    def deve_ser_exibida(self, respostas_anteriores):
        """
        Verifica se a questão deve ser exibida baseada em dependências
        """
        if not self.questao_dependencia:
            return True
        
        # Buscar resposta da questão de dependência
        resposta_dependencia = respostas_anteriores.get(str(self.questao_dependencia.indice))
        
        if not resposta_dependencia:
            return False
        
        # Se não há valor específico de dependência, sempre exibe
        if not self.valor_dependencia:
            return True
        
        # Verificar se a resposta corresponde ao valor esperado
        return str(resposta_dependencia) == str(self.valor_dependencia)
    
    def clean(self):
        """Validação personalizada do modelo"""
        from django.core.exceptions import ValidationError
        
        # Se não tem índice, calcular automaticamente
        if not self.indice and self.fluxo:
            ultimo_indice = self.fluxo.questoes.aggregate(
                models.Max('indice')
            )['indice__max'] or 0
            self.indice = ultimo_indice + 1
        
        # Verificar se o índice já existe para este fluxo
        if self.pk:  # Se é uma edição
            existing = QuestaoFluxo.objects.filter(
                fluxo=self.fluxo,
                indice=self.indice
            ).exclude(pk=self.pk).exists()
        else:  # Se é uma criação
            existing = QuestaoFluxo.objects.filter(
                fluxo=self.fluxo,
                indice=self.indice
            ).exists()
        
        if existing:
            raise ValidationError({
                'indice': f'Já existe uma questão com índice {self.indice} neste fluxo.'
            })
        
        super().clean()
    
    def save(self, *args, **kwargs):
        # Garantir que o índice seja preenchido antes de salvar
        if not self.indice and self.fluxo:
            ultimo_indice = self.fluxo.questoes.aggregate(
                models.Max('indice')
            )['indice__max'] or 0
            self.indice = ultimo_indice + 1
        
        super().save(*args, **kwargs)


class AtendimentoFluxo(models.Model):
    """
    Modelo para controlar uma sessão de atendimento específica
    Relaciona lead/prospecto com um fluxo e controla o progresso
    """
    STATUS_CHOICES = [
        ('iniciado', 'Iniciado'),
        ('em_andamento', 'Em Andamento'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
        ('abandonado', 'Abandonado'),
        ('erro', 'Erro'),
        ('cancelado', 'Cancelado'),
        ('aguardando_validacao', 'Aguardando Validação'),
        ('validado', 'Validado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    # Relacionamentos principais
    lead = models.ForeignKey(
        LeadProspecto,
        on_delete=models.CASCADE,
        related_name='atendimentos_fluxo',
        verbose_name="Lead/Prospecto"
    )
    
    fluxo = models.ForeignKey(
        FluxoAtendimento,
        on_delete=models.CASCADE,
        related_name='atendimentos',
        verbose_name="Fluxo"
    )
    
    # Relacionamento opcional com histórico de contato
    historico_contato = models.ForeignKey(
        HistoricoContato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='atendimentos_fluxo',
        verbose_name="Histórico de Contato"
    )
    
    # Controle de progresso
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='iniciado',
        verbose_name="Status"
    )
    
    questao_atual = models.PositiveIntegerField(
        default=1,
        verbose_name="Questão Atual",
        help_text="Índice da questão atual no fluxo"
    )
    
    total_questoes = models.PositiveIntegerField(
        verbose_name="Total de Questões",
        help_text="Total de questões no fluxo"
    )
    
    questoes_respondidas = models.PositiveIntegerField(
        default=0,
        verbose_name="Questões Respondidas"
    )
    
    # Controle de tempo
    data_inicio = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Início"
    )
    
    data_ultima_atividade = models.DateTimeField(
        auto_now=True,
        verbose_name="Data da Última Atividade"
    )
    
    data_conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )
    
    tempo_total = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tempo Total (segundos)",
        help_text="Tempo total para completar o fluxo"
    )
    
    # Controle de tentativas
    tentativas_atual = models.PositiveIntegerField(
        default=0,
        verbose_name="Tentativas Atuais"
    )
    
    max_tentativas = models.PositiveIntegerField(
        default=3,
        verbose_name="Máximo de Tentativas"
    )
    
    # Dados do atendimento
    dados_respostas = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        verbose_name="Dados das Respostas",
        help_text="JSON com todas as respostas do usuário"
        
        
    )
    
    observacoes = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observações",
        help_text="Observações sobre o atendimento"
    )
    
    # Campos de auditoria
    ip_origem = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP de Origem"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent"
    )
    
    dispositivo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Dispositivo",
        help_text="Tipo de dispositivo usado"
    )
    
    # Campos para integração
    id_externo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="ID Externo",
        help_text="ID em sistema externo (ex: Hubsoft)"
    )
    
    resultado_final = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Resultado Final",
        help_text="Resultado processado do atendimento"
    )
    
    score_qualificacao = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Score de Qualificação",
        help_text="Score calculado baseado nas respostas"
    )
    
    class Meta:
        db_table = 'atendimentos_fluxo'
        verbose_name = "Atendimento de Fluxo"
        verbose_name_plural = "Atendimentos de Fluxo"
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['lead']),
            models.Index(fields=['fluxo']),
            models.Index(fields=['status']),
            models.Index(fields=['data_inicio']),
            models.Index(fields=['questao_atual']),
            models.Index(fields=['id_externo']),
            # Índices compostos para consultas eficientes
            models.Index(fields=['lead', 'status']),
            models.Index(fields=['fluxo', 'status']),
            models.Index(fields=['data_inicio', 'status']),
        ]
    
    def __str__(self):
        return f"{self.lead.nome_razaosocial} - {self.fluxo.nome} ({self.status})"
    
    def get_status_display(self):  # compatível com chamadas existentes
        if not self.status:
            return "Não definido"
        try:
            return StatusConfiguravel.get_label('atendimento_status', self.status)
        except Exception:
            mapping = dict(self.STATUS_CHOICES)
            return mapping.get(self.status, self.status)
    
    def get_progresso_percentual(self):
        """Retorna progresso em percentual"""
        if not self.total_questoes or self.total_questoes == 0:
            return 0
        return round((self.questoes_respondidas / self.total_questoes) * 100, 1)
    
    def get_questao_atual_obj(self):
        """Retorna objeto da questão atual"""
        return self.fluxo.get_questao_por_indice(self.questao_atual)
    
    def get_proxima_questao(self):
        """Retorna próxima questão a ser exibida"""
        return self.fluxo.get_proxima_questao(self.questao_atual)
    
    def get_questao_anterior(self):
        """Retorna questão anterior"""
        return self.fluxo.get_questao_anterior(self.questao_atual)
    
    def pode_avancar(self):
        """Verifica se pode avançar para próxima questão"""
        questao_atual = self.get_questao_atual_obj()
        if not questao_atual:
            return False
        
        # Verificar se a questão atual foi respondida
        resposta_atual = self.dados_respostas.get(str(self.questao_atual))
        if questao_atual.tipo_validacao == 'obrigatoria' and not resposta_atual:
            return False
        
        return True
    
    def pode_voltar(self):
        """Verifica se pode voltar para questão anterior"""
        questao_atual = self.get_questao_atual_obj()
        if not questao_atual:
            return False
        
        return questao_atual.permite_voltar and self.questao_atual > 1
    
    def responder_questao(self, indice_questao, resposta, validar=True):
        """
        Registra resposta para uma questão específica
        Retorna (sucesso, mensagem)
        """
        questao = self.fluxo.get_questao_por_indice(indice_questao)
        if not questao:
            return False, "Questão não encontrada"
        
        # Validação se solicitada
        valido = True
        mensagem_erro = None
        if validar:
            valido, mensagem_erro = questao.validar_resposta(resposta)
            if not valido:
                return False, mensagem_erro
        
        # Verificar se esta questão já foi respondida antes
        questao_ja_respondida = str(indice_questao) in self.dados_respostas
        
        # Registrar resposta
        self.dados_respostas[str(indice_questao)] = {
            'resposta': resposta,
            'data_resposta': timezone.now().isoformat(),
            'valida': valido,
            'mensagem_erro': mensagem_erro
        }
        
        # Atualizar contadores - só incrementar se é a primeira vez que responde esta questão
        if not questao_ja_respondida:
            self.questoes_respondidas += 1
        
        # Recalcular total de questões respondidas baseado nos dados_respostas
        self.questoes_respondidas = len([
            k for k, v in self.dados_respostas.items() 
            if v.get('valida', False) and v.get('resposta') is not None
        ])
        
        self.save()
        return True, "Resposta registrada com sucesso"
    
    def avancar_questao(self):
        """
        Avança para próxima questão
        Retorna (sucesso, proxima_questao)
        """
        if not self.pode_avancar():
            return False, "Não é possível avançar"
        
        proxima_questao = self.get_proxima_questao()
        if proxima_questao:
            self.questao_atual = proxima_questao.indice
            self.save()
            return True, proxima_questao
        
        # Se não há próxima questão, finalizar
        self.finalizar_atendimento()
        return True, None
    
    def voltar_questao(self):
        """
        Volta para questão anterior
        Retorna (sucesso, questao_anterior)
        """
        if not self.pode_voltar():
            return False, "Não é possível voltar"
        
        questao_anterior = self.get_questao_anterior()
        if questao_anterior:
            self.questao_atual = questao_anterior.indice
            self.save()
            return True, questao_anterior
        
        return False, "Questão anterior não encontrada"
    
    def finalizar_atendimento(self, sucesso=True):
        """
        Finaliza o atendimento
        """
        self.status = 'completado' if sucesso else 'abandonado'
        self.data_conclusao = timezone.now()
        
        # Calcular tempo total
        if self.data_inicio and self.data_conclusao:
            tempo_delta = self.data_conclusao - self.data_inicio
            self.tempo_total = int(tempo_delta.total_seconds())
        
        # Calcular score de qualificação
        self.score_qualificacao = self.calcular_score_qualificacao()
        
        self.save()
        
        # Atualizar lead se necessário
        self.atualizar_lead_com_resultados()
    
    def calcular_score_qualificacao(self):
        """
        Calcula score de qualificação baseado nas respostas
        """
        score = 5  # Score base
        
        # Lógica de cálculo baseada no tipo de fluxo e respostas
        if self.fluxo.tipo_fluxo == 'qualificacao':
            # Score baseado em respostas específicas
            for indice, dados in self.dados_respostas.items():
                questao = self.fluxo.get_questao_por_indice(int(indice))
                if questao and dados.get('valida'):
                    # Lógica específica para cada tipo de questão
                    if questao.tipo_questao == 'escala':
                        try:
                            valor = int(dados['resposta'])
                            if valor >= 8:
                                score += 2
                            elif valor >= 6:
                                score += 1
                            elif valor <= 3:
                                score -= 1
                        except:
                            pass
        
        return max(1, min(10, score))
    
    def atualizar_lead_com_resultados(self):
        """
        Atualiza o lead com resultados do atendimento
        """
        if self.status == 'completado' and self.score_qualificacao:
            # Atualizar score do lead
            self.lead.score_qualificacao = self.score_qualificacao
            self.lead.save()
            
            # Adicionar observações sobre o fluxo
            if self.observacoes:
                if not self.lead.observacoes:
                    self.lead.observacoes = ""
                self.lead.observacoes += f"\n\nFluxo {self.fluxo.nome} ({self.data_conclusao.strftime('%d/%m/%Y %H:%M')}):\n{self.observacoes}"
                self.lead.save()
    
    def get_tempo_formatado(self):
        """Retorna tempo total formatado"""
        if self.tempo_total:
            if self.tempo_total < 60:
                return f"{self.tempo_total}s"
            elif self.tempo_total < 3600:
                minutos = self.tempo_total // 60
                segundos = self.tempo_total % 60
                return f"{minutos}m {segundos}s"
            else:
                horas = self.tempo_total // 3600
                minutos = (self.tempo_total % 3600) // 60
                return f"{horas}h {minutos}m"
        return "N/A"
    
    def get_respostas_formatadas(self):
        """Retorna respostas formatadas para exibição"""
        respostas_formatadas = []
        
        if not self.total_questoes or self.total_questoes == 0:
            return respostas_formatadas
        
        for indice in range(1, self.total_questoes + 1):
            questao = self.fluxo.get_questao_por_indice(indice)
            if questao:
                dados_resposta = self.dados_respostas.get(str(indice), {})
                resposta = dados_resposta.get('resposta', 'Não respondida')
                
                respostas_formatadas.append({
                    'indice': indice,
                    'questao': questao.titulo,
                    'resposta': resposta,
                    'respondida': bool(dados_resposta),
                    'valida': dados_resposta.get('valida', False),
                    'data_resposta': dados_resposta.get('data_resposta'),
                })
        
        return respostas_formatadas
    
    def pode_ser_reiniciado(self):
        """Verifica se o atendimento pode ser reiniciado"""
        return self.status in ['completado', 'abandonado', 'cancelado']
    
    def reiniciar_atendimento(self):
        """Reinicia o atendimento do início"""
        if not self.pode_ser_reiniciado():
            return False
        
        self.status = 'iniciado'
        self.questao_atual = 1
        self.questoes_respondidas = 0
        self.dados_respostas = {}
        self.data_inicio = timezone.now()
        self.data_conclusao = None
        self.tempo_total = None
        self.tentativas_atual += 1
        self.observacoes = None
        self.resultado_final = None
        self.score_qualificacao = None
        
        self.save()
        return True


class RespostaQuestao(models.Model):
    """
    Modelo para armazenar respostas individuais de questões
    Permite histórico detalhado e auditoria completa
    """
    atendimento = models.ForeignKey(
        AtendimentoFluxo,
        on_delete=models.CASCADE,
        related_name='respostas_detalhadas',
        verbose_name="Atendimento"
    )
    
    questao = models.ForeignKey(
        QuestaoFluxo,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name="Questão"
    )
    
    resposta = models.TextField(
        verbose_name="Resposta"
    )
    
    resposta_processada = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Resposta Processada",
        help_text="Resposta processada/validada em formato estruturado"
    )
    
    valida = models.BooleanField(
        default=True,
        verbose_name="Válida"
    )
    
    mensagem_erro = models.TextField(
        null=True,
        blank=True,
        verbose_name="Mensagem de Erro"
    )
    
    tentativas = models.PositiveIntegerField(
        default=1,
        verbose_name="Tentativas"
    )
    
    data_resposta = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data da Resposta"
    )
    
    tempo_resposta = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tempo de Resposta (segundos)",
        help_text="Tempo para responder esta questão"
    )
    
    # Campos de auditoria
    ip_origem = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP de Origem"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent"
    )
    
    dados_extras = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Dados Extras",
        help_text="Dados adicionais sobre a resposta"
    )
    
    class Meta:
        db_table = 'respostas_questao'
        verbose_name = "Resposta de Questão"
        verbose_name_plural = "Respostas de Questões"
        ordering = ['atendimento', 'questao', '-data_resposta']
        indexes = [
            models.Index(fields=['atendimento', 'questao']),
            models.Index(fields=['data_resposta']),
            models.Index(fields=['valida']),
        ]
    
    def __str__(self):
        return f"{self.atendimento} - Q{self.questao.indice}: {self.resposta[:50]}"
    
    def get_tempo_resposta_formatado(self):
        """Retorna tempo de resposta formatado"""
        if self.tempo_resposta:
            if self.tempo_resposta < 60:
                return f"{self.tempo_resposta}s"
            else:
                minutos = self.tempo_resposta // 60
                segundos = self.tempo_resposta % 60
                return f"{minutos}m {segundos}s"
        return "N/A"


# Registrar sinais mesmo se o AppConfig não estiver referenciado diretamente em INSTALLED_APPS
from . import signals  # noqa: E402,F401


class ConfiguracaoCadastro(models.Model):
    """
    Modelo para gerenciar configurações da página de cadastro
    """
    empresa = models.CharField(
        max_length=100,
        verbose_name="Nome da Empresa",
        help_text="Nome da empresa para qual esta configuração se aplica"
    )
    
    # Configurações gerais
    titulo_pagina = models.CharField(
        max_length=200,
        default="Cadastro de Cliente",
        verbose_name="Título da Página"
    )
    
    subtitulo_pagina = models.CharField(
        max_length=300,
        default="Preencha seus dados para começar",
        verbose_name="Subtítulo da Página"
    )
    
    # Configurações de contato
    telefone_suporte = models.CharField(
        max_length=20,
        default="(89) 2221-0068",
        verbose_name="Telefone de Suporte"
    )
    
    whatsapp_suporte = models.CharField(
        max_length=20,
        default="558922210068",
        verbose_name="WhatsApp de Suporte"
    )
    
    email_suporte = models.EmailField(
        default="contato@megalinkpiaui.com.br",
        verbose_name="Email de Suporte"
    )
    
    # Configurações de planos
    mostrar_selecao_plano = models.BooleanField(
        default=True,
        verbose_name="Mostrar Seleção de Plano"
    )
    
    plano_padrao = models.ForeignKey(
        'PlanoInternet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Plano Padrão"
    )
    
    # Configurações de campos obrigatórios
    cpf_obrigatorio = models.BooleanField(
        default=True,
        verbose_name="CPF Obrigatório"
    )
    
    email_obrigatorio = models.BooleanField(
        default=True,
        verbose_name="Email Obrigatório"
    )
    
    telefone_obrigatorio = models.BooleanField(
        default=True,
        verbose_name="Telefone Obrigatório"
    )
    
    endereco_obrigatorio = models.BooleanField(
        default=True,
        verbose_name="Endereço Obrigatório"
    )
    
    # Configurações de validação
    validar_cep = models.BooleanField(
        default=True,
        verbose_name="Validar CEP"
    )
    
    validar_cpf = models.BooleanField(
        default=True,
        verbose_name="Validar CPF"
    )
    
    # Configurações de fluxo
    mostrar_progress_bar = models.BooleanField(
        default=True,
        verbose_name="Mostrar Barra de Progresso"
    )
    
    numero_etapas = models.PositiveIntegerField(
        default=4,
        verbose_name="Número de Etapas"
    )
    
    # Configurações de sucesso
    mensagem_sucesso = models.TextField(
        default="Parabéns! Seu cadastro foi realizado com sucesso.",
        verbose_name="Mensagem de Sucesso"
    )
    
    instrucoes_pos_cadastro = models.TextField(
        default="Em breve nossa equipe entrará em contato para agendar a instalação.",
        verbose_name="Instruções Pós-Cadastro"
    )
    
    # Configurações de integração
    criar_lead_automatico = models.BooleanField(
        default=True,
        verbose_name="Criar Lead Automático"
    )
    
    origem_lead_padrao = models.CharField(
        max_length=50,
        choices=LeadProspecto.ORIGEM_CHOICES,
        default='site',
        verbose_name="Origem Padrão do Lead"
    )
    
    # Configurações de notificação
    enviar_email_confirmacao = models.BooleanField(
        default=False,
        verbose_name="Enviar Email de Confirmação"
    )
    
    enviar_whatsapp_confirmacao = models.BooleanField(
        default=False,
        verbose_name="Enviar WhatsApp de Confirmação"
    )
    
    # Configurações de segurança
    captcha_obrigatorio = models.BooleanField(
        default=False,
        verbose_name="Captcha Obrigatório"
    )
    
    limite_tentativas_dia = models.PositiveIntegerField(
        default=5,
        verbose_name="Limite de Tentativas por Dia"
    )
    
    # Metadados
    ativo = models.BooleanField(
        default=True,
        verbose_name="Configuração Ativa"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    class Meta:
        db_table = 'configuracoes_cadastro'
        verbose_name = 'Configuração de Cadastro'
        verbose_name_plural = 'Configurações de Cadastro'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f"Configuração - {self.empresa}"
    
    def get_configuracao_ativa(self):
        """Retorna a configuração ativa para a empresa"""
        return ConfiguracaoCadastro.objects.filter(
            empresa=self.empresa,
            ativo=True
        ).first()


class PlanoInternet(models.Model):
    """
    Modelo para gerenciar planos de internet
    """
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Plano"
    )
    
    descricao = models.TextField(
        verbose_name="Descrição do Plano"
    )
    
    velocidade_download = models.PositiveIntegerField(
        verbose_name="Velocidade de Download (Mbps)"
    )
    
    velocidade_upload = models.PositiveIntegerField(
        verbose_name="Velocidade de Upload (Mbps)"
    )
    
    valor_mensal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Valor Mensal (R$)"
    )
    
    # IDs externos
    id_sistema_externo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="ID no Sistema Externo"
    )
    
    # Características do plano
    wifi_6 = models.BooleanField(
        default=False,
        verbose_name="Wi-Fi 6"
    )
    
    suporte_prioritario = models.BooleanField(
        default=False,
        verbose_name="Suporte Prioritário"
    )
    
    suporte_24h = models.BooleanField(
        default=True,
        verbose_name="Suporte 24h"
    )
    
    upload_simetrico = models.BooleanField(
        default=True,
        verbose_name="Upload Simétrico"
    )
    
    # Configurações de exibição
    ordem_exibicao = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    
    destaque = models.CharField(
        max_length=50,
        choices=[
            ('', 'Sem Destaque'),
            ('popular', 'Mais Popular'),
            ('premium', 'Premium'),
            ('economico', 'Mais Econômico'),
            ('recomendado', 'Recomendado')
        ],
        default='',
        verbose_name="Tipo de Destaque"
    )
    
    # Status
    ativo = models.BooleanField(
        default=True,
        verbose_name="Plano Ativo"
    )
    
    # Metadados
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
    
    class Meta:
        db_table = 'planos_internet'
        verbose_name = 'Plano de Internet'
        verbose_name_plural = 'Planos de Internet'
        ordering = ['ordem_exibicao', 'valor_mensal']
    
    def __str__(self):
        return f"{self.nome} - {self.velocidade_download}MB"
    
    def get_valor_formatado(self):
        """Retorna o valor formatado em reais"""
        return f"R$ {self.valor_mensal:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def get_velocidade_formatada(self):
        """Retorna a velocidade formatada"""
        if self.velocidade_download >= 1000:
            return f"{self.velocidade_download/1000:.1f} GB"
        return f"{self.velocidade_download} MB"


class OpcaoVencimento(models.Model):
    """
    Modelo para gerenciar opções de vencimento de fatura
    """
    dia_vencimento = models.PositiveIntegerField(
        verbose_name="Dia do Vencimento"
    )
    
    descricao = models.CharField(
        max_length=50,
        verbose_name="Descrição"
    )
    
    ordem_exibicao = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Opção Ativa"
    )
    
    class Meta:
        db_table = 'opcoes_vencimento'
        verbose_name = 'Opção de Vencimento'
        verbose_name_plural = 'Opções de Vencimento'
        ordering = ['ordem_exibicao', 'dia_vencimento']
    
    def __str__(self):
        return f"Dia {self.dia_vencimento} - {self.descricao}"


class CadastroCliente(models.Model):
    """
    Modelo para armazenar cadastros de clientes via site
    """
    # Dados pessoais
    nome_completo = models.CharField(
        max_length=255,
        verbose_name="Nome Completo"
    )
    
    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF"
    )
    
    email = models.EmailField(
        verbose_name="E-mail"
    )
    
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone/WhatsApp"
    )
    
    data_nascimento = models.DateField(
        verbose_name="Data de Nascimento"
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP"
    )
    
    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereço"
    )
    
    numero = models.CharField(
        max_length=20,
        verbose_name="Número"
    )
    
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro"
    )
    
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade"
    )
    
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado"
    )
    
    # Plano e vencimento
    plano_selecionado = models.ForeignKey(
        PlanoInternet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Plano Selecionado"
    )
    
    vencimento_selecionado = models.ForeignKey(
        OpcaoVencimento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vencimento Selecionado"
    )
    
    # Status do cadastro
    STATUS_CHOICES = [
        ('iniciado', 'Iniciado'),
        ('dados_pessoais', 'Dados Pessoais Preenchidos'),
        ('endereco', 'Endereço Preenchido'),
        ('finalizado', 'Finalizado'),
        ('erro', 'Erro'),
        ('cancelado', 'Cancelado')
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='iniciado',
        verbose_name="Status do Cadastro"
    )
    
    # Integração com Lead
    lead_gerado = models.ForeignKey(
        LeadProspecto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Lead Gerado"
    )
    
    # Metadados
    ip_cliente = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP do Cliente"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent"
    )
    
    origem_cadastro = models.CharField(
        max_length=50,
        default='site',
        verbose_name="Origem do Cadastro"
    )
    
    data_inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Início"
    )
    
    data_finalizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Finalização"
    )
    
    tempo_total_cadastro = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Tempo Total de Cadastro"
    )
    
    # Campos de auditoria
    tentativas_etapa = models.JSONField(
        default=dict,
        verbose_name="Tentativas por Etapa"
    )
    
    campos_preenchidos = models.JSONField(
        default=dict,
        verbose_name="Campos Preenchidos"
    )
    
    erros_validacao = models.JSONField(
        default=list,
        verbose_name="Erros de Validação"
    )
    
    class Meta:
        db_table = 'cadastros_clientes'
        verbose_name = 'Cadastro de Cliente'
        verbose_name_plural = 'Cadastros de Clientes'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['cpf']),
            models.Index(fields=['email']),
            models.Index(fields=['telefone']),
            models.Index(fields=['status']),
            models.Index(fields=['data_inicio']),
        ]
    
    def __str__(self):
        return f"{self.nome_completo} - {self.get_status_display()}"
    
    def finalizar_cadastro(self):
        """Finaliza o cadastro e gera o lead"""
        try:
            # Calcular tempo total
            if self.data_finalizacao:
                self.tempo_total_cadastro = self.data_finalizacao - self.data_inicio
            
            # Atualizar status
            self.status = 'finalizado'
            self.save()
            
            # Gerar lead automaticamente
            if not self.lead_gerado:
                self.gerar_lead()
            
            return True
        except Exception as e:
            self.status = 'erro'
            self.erros_validacao.append(str(e))
            self.save()
            return False
    
    def gerar_lead(self):
        """Gera um lead baseado no cadastro"""
        try:
            # Criar lead
            lead = LeadProspecto.objects.create(
                nome_razaosocial=self.nome_completo,
                email=self.email,
                telefone=self.telefone,
                valor=self.plano_selecionado.valor_mensal if self.plano_selecionado else None,
                origem=self.origem_cadastro,
                status_api='pendente',
                cpf_cnpj=self.cpf,
                endereco=f"{self.endereco}, {self.numero} - {self.bairro}",
                cidade=self.cidade,
                estado=self.estado,
                cep=self.cep,
                observacoes=f"Cadastro via site - Plano: {self.plano_selecionado.nome if self.plano_selecionado else 'Não selecionado'}"
            )
            
            # Atualizar referência
            self.lead_gerado = lead
            self.save()
            
            # Criar histórico de contato
            self.criar_historico_contato(lead)
            
            return lead
        except Exception as e:
            self.erros_validacao.append(f"Erro ao gerar lead: {str(e)}")
            self.save()
            return None
    
    def criar_historico_contato(self, lead):
        """Cria histórico de contato para o lead"""
        try:
            HistoricoContato.objects.create(
                lead=lead,
                nome_contato=self.nome_completo,
                telefone=self.telefone,
                status='fluxo_finalizado',
                observacoes=f"Cadastro finalizado via site - Plano: {self.plano_selecionado.nome if self.plano_selecionado else 'Não selecionado'}",
                data_hora_contato=self.data_finalizacao or timezone.now(),
                duracao=self.tempo_total_cadastro or timedelta(seconds=0),
                convertido_lead=True,
                data_conversao_lead=self.data_finalizacao or timezone.now(),
                origem_contato='site_cadastro',
                ip_contato=self.ip_cliente,
                user_agent=self.user_agent
            )
            return True
        except Exception as e:
            self.erros_validacao.append(f"Erro ao criar histórico: {str(e)}")
            self.save()
            return False
    
    def get_progresso_percentual(self):
        """Retorna o progresso do cadastro em percentual"""
        progresso_map = {
            'iniciado': 25,
            'dados_pessoais': 50,
            'endereco': 75,
            'finalizado': 100
        }
        return progresso_map.get(self.status, 0)
    
    def get_etapa_atual(self):
        """Retorna a etapa atual do cadastro"""
        etapas = {
            'iniciado': 1,
            'dados_pessoais': 2,
            'endereco': 3,
            'finalizado': 4
        }
        return etapas.get(self.status, 1)
    
    def validar_dados_pessoais(self):
        """Valida os dados pessoais preenchidos"""
        erros = []
        
        if not self.nome_completo or len(self.nome_completo.strip()) < 3:
            erros.append("Nome completo deve ter pelo menos 3 caracteres")
        
        if not self.cpf or len(self.cpf.replace('.', '').replace('-', '')) != 11:
            erros.append("CPF inválido")
        
        if not self.email or '@' not in self.email:
            erros.append("Email inválido")
        
        if not self.telefone or len(self.telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
            erros.append("Telefone inválido")
        
        if not self.data_nascimento:
            erros.append("Data de nascimento obrigatória")
        
        return erros
    
    def validar_endereco(self):
        """Valida os dados de endereço"""
        erros = []
        
        if not self.cep or len(self.cep.replace('-', '')) != 8:
            erros.append("CEP inválido")
        
        if not self.endereco or len(self.endereco.strip()) < 5:
            erros.append("Endereço deve ter pelo menos 5 caracteres")
        
        if not self.numero:
            erros.append("Número obrigatório")
        
        if not self.bairro or len(self.bairro.strip()) < 2:
            erros.append("Bairro deve ter pelo menos 2 caracteres")
        
        if not self.cidade or len(self.cidade.strip()) < 2:
            erros.append("Cidade deve ter pelo menos 2 caracteres")
        
        if not self.estado or len(self.estado) != 2:
            erros.append("Estado deve ter 2 caracteres")
        
        return erros