from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
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

# Registrar sinais mesmo se o AppConfig não estiver referenciado diretamente em INSTALLED_APPS
from . import signals  # noqa: E402,F401