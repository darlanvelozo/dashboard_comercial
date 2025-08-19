# 📋 Documentação Completa dos Models - Dashboard Comercial

## 🏗️ Visão Geral da Arquitetura

O sistema é composto por 6 models principais que trabalham em conjunto para gerenciar o funil completo de vendas, desde a captação de leads até a conversão em vendas confirmadas.

---

## 🔗 Models e Relacionamentos

### 1. 👤 **LeadProspecto** (Entidade Central)
**Função**: Armazena informações de leads/prospectos iniciais capturados através de diversos canais.

#### Campos Principais:
- **Identificação**: `nome_razaosocial`, `email`, `telefone`, `cpf_cnpj`
- **Comercial**: `valor`, `empresa`, `origem`, `status_api`
- **Rastreamento**: `id_hubsoft` (chave para relacionamentos automáticos)
- **Endereço**: `endereco`, `rua`, `numero_residencia`, `bairro`, `cidade`, `estado`, `cep`
- **RP Integration**: `id_plano_rp`, `id_dia_vencimento`, `id_vendedor_rp`
- **Analytics**: `score_qualificacao`, `tentativas_contato`, `custo_aquisicao`

#### Métodos Importantes:
- `calcular_score_qualificacao()`: Calcula score 1-10 baseado em dados do lead
- `get_historico_contatos_relacionados()`: Busca contatos por telefone e relacionamento direto
- `get_taxa_sucesso_contatos()`: Calcula taxa de sucesso dos contatos
- `incrementar_tentativa_contato()`: Controla tentativas e atualiza score automaticamente
- `pode_reprocessar()`: Verifica se pode ser reprocessado (max 5 tentativas)

### 2. 🎯 **Prospecto** (Processamento)
**Função**: Controla o processamento e validação de prospectos no funil de vendas.

#### Campos Principais:
- **Relacionamento**: `lead_id` (FK para LeadProspecto)
- **Identificação**: `nome_prospecto`, `id_prospecto_hubsoft`
- **Processamento**: `status`, `tentativas_processamento`, `tempo_processamento`
- **Controle**: `data_inicio_processamento`, `data_fim_processamento`, `usuario_processamento`
- **Analytics**: `score_conversao`, `prioridade`
- **Dados**: `dados_processamento`, `resultado_processamento` (JSON)

#### Métodos Importantes:
- `iniciar_processamento()`: Marca início e registra usuário
- `finalizar_processamento()`: Calcula tempo e atualiza status
- `calcular_score_conversao_automatico()`: Score baseado em dados do lead relacionado
- `pode_reprocessar()`: Máximo 3 tentativas para erro/pendente

### 3. 📞 **HistoricoContato** (Funil de Conversão)
**Função**: Registra todos os contatos/chamadas e controla o funil de conversão.

#### Campos Principais:
- **Relacionamento**: `lead_id` (FK opcional para LeadProspecto)
- **Contato**: `telefone`, `nome_contato`, `data_hora_contato`, `duracao_segundos`
- **Status**: `status` (configurável via admin)
- **Conversão**: `converteu_lead`, `converteu_venda`, `valor_venda`
- **Rastreamento**: `sucesso`, `origem_contato`, `identificador_cliente`
- **Dados**: `transcricao`, `observacoes`, `dados_extras` (JSON)

#### Métodos Importantes:
- `is_contato_bem_sucedido()`: Verifica se finalizou fluxo ou foi transferido
- `is_conversao_completa()`: Verifica conversão completa (contato → venda)
- `get_funil_insights()`: Métricas do funil para período específico
- `get_status_display_color()`: Cores para dashboard baseadas no status

### 4. ⚙️ **StatusConfiguravel** (Sistema Dinâmico)
**Função**: Permite configurar status via Django Admin sem alterar código.

#### Grupos de Status:
- **`lead_status_api`**: Status dos leads (pendente, processado, erro, etc.)
- **`prospecto_status`**: Status dos prospectos (pendente, processando, validacao_aprovada, etc.)
- **`historico_status`**: Status dos contatos (fluxo_inicializado, convertido_lead, etc.)

#### Funcionamento:
- Admin pode adicionar/editar/desativar status
- Models usam `get_status_display()` que consulta esta tabela
- Fallback para choices hardcoded se não encontrar na tabela
- Campo `ordem` permite ordenação customizada

### 5. 🔧 **ConfiguracaoSistema** (Configurações)
**Função**: Armazena configurações gerais do sistema de forma dinâmica.

#### Tipos Suportados:
- `string`, `integer`, `boolean`, `json`, `decimal`
- Versionamento via `data_criacao` e `data_atualizacao`
- Ativação/desativação via campo `ativo`

### 6. 📊 **LogSistema** (Auditoria)
**Função**: Registra automaticamente todas as operações do sistema.

#### Níveis de Log:
- `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Captura: usuário, IP, módulo, dados extras em JSON
- Usado pelas APIs para rastreabilidade completa

---

## 🔄 Fluxo de Funcionamento

### 1. **Entrada de Dados**
```
Lead → API → LeadProspecto.create()
├── Signal verifica id_hubsoft
├── Se existe Prospecto com mesmo id → relaciona
└── Senão aguarda relacionamento futuro
```

### 2. **Processamento**
```
Prospecto → API → Prospecto.create()
├── Signal verifica id_prospecto_hubsoft  
├── Se existe Lead com mesmo id → relaciona
├── Calcula score_conversao automaticamente
└── Inicia processamento via métodos de controle
```

### 3. **Contatos e Conversão**
```
HistoricoContato → API → HistoricoContato.create()
├── Relaciona com Lead por telefone ou FK
├── Atualiza métricas de conversão
├── Calcula taxas de sucesso
└── Alimenta dashboard em tempo real
```

### 4. **Sistema de Status Dinâmico**
```
Model.get_status_display() 
├── Consulta StatusConfiguravel
├── Busca por grupo + codigo
├── Retorna rótulo personalizado
└── Fallback para choices hardcoded
```

---

## 🤖 Relacionamentos Automáticos

### Signal: `relate_lead_when_prospecto_has_hubsoft`
**Trigger**: `post_save` do `Prospecto`
**Função**: Relaciona Prospecto com Lead baseado no `id_hubsoft`

### Signal: `relate_prospecto_when_lead_has_hubsoft`
**Trigger**: `post_save` do `LeadProspecto`  
**Função**: Relaciona Lead com Prospectos órfãos baseado no `id_hubsoft`

### API: `/api/verificar-relacionamentos/`
**Função**: Execução manual/automática para verificar e criar relacionamentos
**Uso**: Chamada automática no carregamento de páginas

---

## 📈 Sistema de Métricas

### LeadProspecto
- **Score de Qualificação** (1-10): Baseado em empresa, valor, origem, histórico
- **Taxa de Sucesso**: Percentual de contatos bem-sucedidos
- **Custo de Aquisição**: Investimento para captar o lead

### Prospecto  
- **Score de Conversão** (0-100%): Probabilidade de conversão baseada no lead
- **Tempo de Processamento**: Controle de performance
- **Prioridade**: Sistema de filas (1=baixa, 5=alta)

### HistoricoContato
- **Funil de Conversão**: Métricas completas do funil
- **Taxa de Finalização**: Contatos que completaram o fluxo
- **Valor Total de Vendas**: Somatório de vendas confirmadas

---

## 🎨 Características Especiais

### 1. **Índices Otimizados**
- Índices simples em campos de busca frequente
- Índices compostos para consultas complexas
- Performance otimizada para grandes volumes

### 2. **Validação Robusta**
- Validators customizados (telefone, email, scores)
- Constraints de integridade (unique_together)
- Validação de ranges (1-10, 0-100%)

### 3. **JSON Fields**
- Dados flexíveis em `dados_processamento`, `resultado_processamento`
- `dados_extras` para informações dinâmicas
- Compatibilidade com sistemas externos

### 4. **Timestamps Automáticos**
- `auto_now` e `auto_now_add` para controle temporal
- Rastreamento completo de criação/atualização
- Histórico de modificações

### 5. **Soft Delete Pattern**
- Campo `ativo` em vez de DELETE real
- Preservação de dados para auditoria
- Consultas filtradas por ativo=True

---

## 🔧 Métodos de Business Logic

### Cálculo Automático de Scores
```python
# LeadProspecto
score = 5  # base
if self.empresa: score += 1
if self.valor > 1000: score += 1
if self.origem == 'indicacao': score += 1
if self.tentativas_contato > 3: score -= 1
return max(1, min(10, score))

# Prospecto  
score = 50.0  # base
score += (lead.score_qualificacao - 5) * 5
if lead.empresa: score += 10
if tentativas > 1: score -= tentativas * 5
return max(0, min(100, score))
```

### Controle de Reprocessamento
```python
# LeadProspecto.pode_reprocessar()
return (self.ativo and 
        self.status_api != 'sucesso' and 
        self.tentativas_contato < 5)

# Prospecto.pode_reprocessar()  
return (self.status in ['erro', 'pendente'] and 
        self.tentativas_processamento < 3)
```

### Insights do Funil
```python
insights = HistoricoContato.get_funil_insights(data_inicio, data_fim)
# Retorna: total_contatos, taxa_finalizacao, 
#          taxa_conversao_venda, valor_total_vendas
```

---

## 🚀 Benefícios da Arquitetura

### 1. **Flexibilidade**
- Status configuráveis sem deploy
- Campos JSON para extensibilidade
- Relacionamentos automáticos

### 2. **Escalabilidade**
- Índices otimizados
- Queries eficientes
- Paginação em todas as APIs

### 3. **Rastreabilidade**
- Logs automáticos de toda operação
- Histórico completo de modificações
- Auditoria completa

### 4. **Integração**
- APIs REST completas
- Webhooks via signals
- Compatibilidade com sistemas externos

### 5. **Analytics**
- Métricas calculadas automaticamente
- Dashboard em tempo real
- Insights de funil de vendas

Esta arquitetura oferece um sistema completo, flexível e escalável para gerenciamento do funil de vendas, com rastreabilidade total e capacidade de integração com sistemas externos.
