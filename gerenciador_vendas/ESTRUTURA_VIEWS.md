# Estrutura Organizada das Views

## 📁 Organização por Seções

### 1. IMPORTS
- **Localização**: Linhas 1-25
- **Conteúdo**: Todos os imports necessários organizados por categoria
- **Models**: Todos os models do sistema em uma única importação

### 2. FUNÇÕES DE SERIALIZAÇÃO - APIs de Atendimento
- **Localização**: Linhas 27-108
- **Funções**:
  - `_serialize_fluxo_atendimento()` - Serializa objetos FluxoAtendimento
  - `_serialize_questao_fluxo()` - Serializa objetos QuestaoFluxo
  - `_serialize_atendimento_fluxo()` - Serializa objetos AtendimentoFluxo

### 3. APIs de Atendimento - Fluxos, Questões, Atendimentos e Respostas
- **Localização**: Linhas 110-478
- **Funções**:
  - `consultar_fluxos_api()` - GET para consultar fluxos de atendimento
  - `consultar_questoes_api()` - GET para consultar questões de fluxo
  - `consultar_atendimentos_api()` - GET para consultar atendimentos de fluxo
  - `consultar_respostas_api()` - GET para consultar respostas de questões

### 4. FUNÇÕES UTILITÁRIAS
- **Localização**: Linhas 480-520
- **Funções**:
  - `_atualizar_resultado_processamento()` - Atualiza resultado_processamento de prospectos
  - `_criar_log_sistema()` - Cria logs no sistema
  - `_parse_json_request()` - Parse de requisições JSON
  - `_model_field_names()` - Obtém nomes dos campos de um model
  - `_serialize_instance()` - Serializa instâncias de models
  - `_resolve_fk()` - Resolve foreign keys
  - `_apply_updates()` - Aplica atualizações em instâncias

### 5. APIs de Registro e Atualização
- **Localização**: Linhas 522-920
- **Funções**:
  - `registrar_lead_api()` - POST para registrar leads
  - `atualizar_lead_api()` - POST para atualizar leads
  - `registrar_prospecto_api()` - POST para registrar prospectos
  - `atualizar_prospecto_api()` - POST para atualizar prospectos
  - `registrar_historico_api()` - POST para registrar histórico de contatos
  - `verificar_relacionamentos_api()` - POST para verificar relacionamentos
  - `atualizar_historico_api()` - POST para atualizar histórico de contatos

### 6. VIEWS DO DASHBOARD
- **Localização**: Linhas 922-980
- **Funções**:
  - `dashboard_view()` - View principal do dashboard
  - `dashboard1()` - Alias para dashboard_view
  - `leads_view()` - View para página de leads
  - `relatorio_leads_view()` - View para relatórios de leads
  - `vendas_view()` - View para página de vendas
  - `api_swagger_view()` - View para documentação Swagger
  - `api_documentation_view()` - View para documentação da API

### 7. APIs de Dados do Dashboard
- **Localização**: Linhas 982-1570
- **Funções**:
  - `dashboard_data()` - Dados principais do dashboard
  - `dashboard_charts_data()` - Dados dos gráficos
  - `dashboard_tables_data()` - Dados das tabelas
  - `dashboard_leads_data()` - Dados dos leads
  - `dashboard_prospectos_data()` - Dados dos prospectos
  - `dashboard_historico_data()` - Dados do histórico de contatos
  - `dashboard_contatos_realtime()` - Contatos em tempo real
  - `dashboard_contato_historico()` - Histórico detalhado de um telefone
  - `dashboard_ultimas_conversoes()` - Últimas conversões de leads

### 8. APIs de Validação de Vendas
- **Localização**: Linhas 1572-1680
- **Funções**:
  - `aprovar_venda_api()` - POST para aprovar vendas
  - `rejeitar_venda_api()` - POST para rejeitar vendas

### 9. APIs de Consulta
- **Localização**: Linhas 1682-2058
- **Funções**:
  - `historico_contatos_api()` - Busca histórico de contatos
  - `get_status_categoria()` - Categoriza status
  - `_parse_bool()` - Parse de valores booleanos
  - `_safe_ordering()` - Ordenação segura
  - `consultar_leads_api()` - GET para consultar leads
  - `consultar_historicos_api()` - GET para consultar histórico

## 🔍 Como Encontrar Funções

### Por Tipo de API:
- **APIs de Atendimento**: Buscar por "consultar_*_api"
- **APIs de Registro**: Buscar por "registrar_*_api"
- **APIs de Atualização**: Buscar por "atualizar_*_api"
- **APIs de Consulta**: Buscar por "consultar_*_api"
- **APIs de Validação**: Buscar por "*_venda_api"

### Por Funcionalidade:
- **Dashboard**: Buscar por "dashboard_*"
- **Leads**: Buscar por "*lead*"
- **Prospectos**: Buscar por "*prospecto*"
- **Histórico**: Buscar por "*historico*"
- **Vendas**: Buscar por "*venda*"

## ⚠️ Pontos de Atenção

### 1. Tratamento de Erros
- Todas as funções de serialização agora têm tratamento de erro com `try/except`
- Uso de `getattr()` com valores padrão para evitar erros de atributo

### 2. Imports Organizados
- Removidas duplicações de imports
- Models organizados em uma única importação
- Imports Django organizados por categoria

### 3. Estrutura Consistente
- Cabeçalhos de seção padronizados
- Espaçamento consistente entre seções
- Comentários explicativos para cada seção

## 🚀 Próximos Passos Recomendados

1. **Testar todas as APIs** para garantir que a organização não quebrou funcionalidades
2. **Adicionar docstrings** mais detalhadas para cada função
3. **Implementar logging** mais robusto nas funções críticas
4. **Adicionar validações** mais rigorosas nos parâmetros de entrada
5. **Criar testes unitários** para cada seção de funcionalidade
