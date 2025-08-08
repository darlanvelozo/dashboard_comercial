from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from faker import Faker
from decimal import Decimal
from vendas_web.models import LeadProspecto, Prospecto, HistoricoContato, ConfiguracaoSistema, LogSistema


class Command(BaseCommand):
    help = 'Gera dados fictícios para testar o dashboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--leads',
            type=int,
            default=50,
            help='Número de leads para criar (padrão: 50)'
        )
        parser.add_argument(
            '--prospectos',
            type=int,
            default=30,
            help='Número de prospectos para criar (padrão: 30)'
        )
        parser.add_argument(
            '--contatos',
            type=int,
            default=100,
            help='Número de contatos para criar (padrão: 100)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpar dados existentes antes de criar novos'
        )

    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        
        if options['clear']:
            self.stdout.write('Limpando dados existentes...')
            LeadProspecto.objects.all().delete()
            Prospecto.objects.all().delete()
            HistoricoContato.objects.all().delete()
            ConfiguracaoSistema.objects.all().delete()
            LogSistema.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Dados limpos com sucesso!'))

        # Gerar Leads
        self.stdout.write(f'Gerando {options["leads"]} leads...')
        leads_criados = self.gerar_leads(fake, options['leads'])
        
        # Gerar Prospectos
        self.stdout.write(f'Gerando {options["prospectos"]} prospectos...')
        self.gerar_prospectos(fake, options['prospectos'], leads_criados)
        
        # Gerar Histórico de Contatos
        self.stdout.write(f'Gerando {options["contatos"]} contatos...')
        self.gerar_contatos(fake, options['contatos'], leads_criados)
        
        # Gerar Configurações
        self.stdout.write('Gerando configurações do sistema...')
        self.gerar_configuracoes()
        
        # Gerar Logs
        self.stdout.write('Gerando logs do sistema...')
        self.gerar_logs(fake, 50)
        
        self.stdout.write(
            self.style.SUCCESS('Dados fictícios gerados com sucesso!')
        )

    def gerar_leads(self, fake, quantidade):
        """Gera leads fictícios"""
        leads = []
        empresas = [
            'Tech Solutions Ltda', 'Inovação Digital', 'Consultoria ABC',
            'Marketing Pro', 'Vendas Master', 'Gestão Moderna',
            'Empresa XYZ', 'Negócios Online', 'Soluções Web',
            'Desenvolvimento Ágil', None, None  # Alguns sem empresa
        ]
        
        origens = [choice[0] for choice in LeadProspecto.ORIGEM_CHOICES]
        status_api = [choice[0] for choice in LeadProspecto.STATUS_API_CHOICES]
        
        for i in range(quantidade):
            # Data de cadastro nos últimos 30 dias
            data_cadastro = fake.date_time_between(
                start_date='-30d',
                end_date='now',
                tzinfo=timezone.get_current_timezone()
            )
            
            lead = LeadProspecto.objects.create(
                nome_razaosocial=fake.name(),
                email=fake.email(),
                telefone=self.gerar_telefone_brasileiro(),
                valor=Decimal(random.uniform(100, 10000)).quantize(Decimal('0.01')) if random.choice([True, False, False]) else Decimal('0.00'),
                empresa=random.choice(empresas),
                origem=random.choice(origens),
                data_cadastro=data_cadastro,
                status_api=random.choice(status_api),
                cpf_cnpj=fake.cpf() if random.choice([True, False]) else None,
                endereco=fake.address() if random.choice([True, False]) else None,
                cidade=fake.city() if random.choice([True, False]) else None,
                estado=fake.state_abbr() if random.choice([True, False]) else None,
                cep=fake.postcode() if random.choice([True, False]) else None,
                observacoes=fake.text(max_nb_chars=200) if random.choice([True, False, False]) else None,
                ativo=random.choice([True, True, True, False])  # 75% ativos
            )
            leads.append(lead)
            
        self.stdout.write(f'✓ {len(leads)} leads criados')
        return leads

    def gerar_prospectos(self, fake, quantidade, leads_disponiveis):
        """Gera prospectos fictícios"""
        status_choices = [choice[0] for choice in Prospecto.STATUS_CHOICES]
        
        for i in range(quantidade):
            # Alguns prospectos terão leads associados
            lead = random.choice(leads_disponiveis) if random.choice([True, False]) else None
            
            data_criacao = fake.date_time_between(
                start_date='-20d',
                end_date='now',
                tzinfo=timezone.get_current_timezone()
            )
            
            # Data de processamento pode ser posterior à criação
            data_processamento = None
            if random.choice([True, False, False]):  # 33% foram processados
                data_processamento = fake.date_time_between(
                    start_date=data_criacao,
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                )
            
            status = random.choice(status_choices)
            
            Prospecto.objects.create(
                lead=lead,
                nome_prospecto=fake.name(),
                id_prospecto_hubsoft=f'HUB{fake.random_int(min=1000, max=9999)}' if random.choice([True, False]) else None,
                status=status,
                data_criacao=data_criacao,
                data_processamento=data_processamento,
                tentativas_processamento=random.randint(0, 5),
                tempo_processamento=Decimal(random.uniform(0.5, 30.0)).quantize(Decimal('0.001')) if data_processamento else None,
                erro_processamento=fake.text(max_nb_chars=100) if status == 'erro' else None,
                prioridade=random.randint(1, 5),
                dados_processamento={'origem': 'dashboard', 'versao': '1.0'} if random.choice([True, False]) else None,
                resultado_processamento={'sucesso': True, 'codigo': 200} if status == 'processado' else None
            )
            
        self.stdout.write(f'✓ {quantidade} prospectos criados')

    def gerar_contatos(self, fake, quantidade, leads_disponiveis):
        """Gera histórico de contatos fictícios"""
        status_choices = [choice[0] for choice in HistoricoContato.STATUS_CHOICES]
        
        # Gerar alguns telefones fixos para simular múltiplos contatos
        telefones_fixos = [self.gerar_telefone_brasileiro() for _ in range(10)]
        
        for i in range(quantidade):
            # 70% dos contatos usam telefones fixos (para simular recorrência)
            if random.random() < 0.7:
                telefone = random.choice(telefones_fixos)
            else:
                telefone = self.gerar_telefone_brasileiro()
            
            # Alguns contatos terão leads associados
            lead = random.choice(leads_disponiveis) if random.choice([True, False, False]) else None
            
            data_contato = fake.date_time_between(
                start_date='-7d',
                end_date='now',
                tzinfo=timezone.get_current_timezone()
            )
            
            status = random.choice(status_choices)
            duracao = random.randint(10, 300) if status in ['fluxo_finalizado', 'transferido_humano'] else random.randint(0, 60)
            
            HistoricoContato.objects.create(
                lead=lead,
                telefone=telefone,
                data_hora_contato=data_contato,
                status=status,
                nome_contato=fake.name() if random.choice([True, False]) else None,
                duracao_segundos=duracao,
                transcricao=fake.text(max_nb_chars=500) if random.choice([True, False, False, False]) else None,
                observacoes=fake.text(max_nb_chars=200) if random.choice([True, False, False]) else None,
                ip_origem=fake.ipv4() if random.choice([True, False]) else None,
                user_agent=fake.user_agent() if random.choice([True, False]) else None,
                dados_extras={'campanha': f'camp_{fake.random_int(1, 10)}'} if random.choice([True, False]) else None,
                sucesso=status in ['fluxo_finalizado', 'transferido_humano']
            )
            
        self.stdout.write(f'✓ {quantidade} contatos criados')

    def gerar_configuracoes(self):
        """Gera configurações do sistema"""
        configuracoes = [
            {
                'chave': 'api_hubsoft_url',
                'valor': 'https://api.hubsoft.com.br/v1/',
                'descricao': 'URL base da API do Hubsoft',
                'tipo': 'string'
            },
            {
                'chave': 'max_tentativas_processamento',
                'valor': '3',
                'descricao': 'Número máximo de tentativas de processamento',
                'tipo': 'integer'
            },
            {
                'chave': 'auto_refresh_dashboard',
                'valor': 'true',
                'descricao': 'Habilitar auto-refresh do dashboard',
                'tipo': 'boolean'
            },
            {
                'chave': 'tempo_limite_processamento',
                'valor': '30.0',
                'descricao': 'Tempo limite para processamento em segundos',
                'tipo': 'decimal'
            },
            {
                'chave': 'configuracao_avancada',
                'valor': '{"tema": "dark", "notificacoes": true}',
                'descricao': 'Configurações avançadas em JSON',
                'tipo': 'json'
            }
        ]
        
        for config in configuracoes:
            ConfiguracaoSistema.objects.get_or_create(
                chave=config['chave'],
                defaults={
                    'valor': config['valor'],
                    'descricao': config['descricao'],
                    'tipo': config['tipo']
                }
            )
            
        self.stdout.write(f'✓ {len(configuracoes)} configurações criadas')

    def gerar_logs(self, fake, quantidade):
        """Gera logs do sistema"""
        niveis = [choice[0] for choice in LogSistema.NIVEL_CHOICES]
        modulos = [
            'dashboard.views', 'api.leads', 'api.prospectos', 
            'core.models', 'auth.middleware', 'tasks.processamento',
            'integracoes.hubsoft', 'utils.helpers'
        ]
        
        for i in range(quantidade):
            nivel = random.choice(niveis)
            modulo = random.choice(modulos)
            
            # Mensagens baseadas no nível
            if nivel == 'ERROR':
                mensagem = f"Erro ao processar {fake.word()}: {fake.sentence()}"
            elif nivel == 'WARNING':
                mensagem = f"Aviso: {fake.sentence()}"
            elif nivel == 'INFO':
                mensagem = f"Processamento concluído: {fake.sentence()}"
            else:
                mensagem = fake.sentence()
            
            LogSistema.objects.create(
                nivel=nivel,
                modulo=modulo,
                mensagem=mensagem,
                dados_extras={'request_id': fake.uuid4()} if random.choice([True, False]) else None,
                usuario=fake.user_name() if random.choice([True, False]) else None,
                ip=fake.ipv4() if random.choice([True, False]) else None,
                data_criacao=fake.date_time_between(
                    start_date='-7d',
                    end_date='now',
                    tzinfo=timezone.get_current_timezone()
                )
            )
            
        self.stdout.write(f'✓ {quantidade} logs criados')

    def gerar_telefone_brasileiro(self):
        """Gera um telefone brasileiro válido"""
        ddd = random.choice([
            '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
            '21', '22', '24',  # RJ
            '27', '28',  # ES
            '31', '32', '33', '34', '35', '37', '38',  # MG
            '41', '42', '43', '44', '45', '46',  # PR
            '47', '48', '49',  # SC
            '51', '53', '54', '55',  # RS
            '61',  # DF
            '62', '64',  # GO
            '65', '66',  # MT
            '67',  # MS
            '68',  # AC
            '69',  # RO
            '71', '73', '74', '75', '77',  # BA
            '79',  # SE
            '81', '87',  # PE
            '82',  # AL
            '83',  # PB
            '84',  # RN
            '85', '88',  # CE
            '86', '89',  # PI
            '91', '93', '94',  # PA
            '92', '97',  # AM
            '95',  # RR
            '96',  # AP
            '98', '99'  # MA
        ])
        
        # Celular (9 dígitos) ou fixo (8 dígitos)
        if random.choice([True, False]):
            # Celular
            numero = f"9{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        else:
            # Fixo
            numero = f"{random.randint(2000, 5999)}{random.randint(1000, 9999)}"
        
        return f"+55{ddd}{numero}"