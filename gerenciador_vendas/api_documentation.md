# 📋 Documentação Completa da API - Dashboard Comercial

## 🌟 Visão Geral

### Características Principais
- **Formato**: JSON (UTF-8)
- **Header**: `Content-Type: application/json`
- **Logs Automáticos**: Todas as operações são registradas no sistema
- **Status Dinâmicos**: Status configuráveis via admin Django
- **Relacionamentos Automáticos**: Sistema relaciona leads e prospectos via `id_hubsoft`
- **Suporte a Múltiplos Formatos de Data**: DD/MM/YYYY, YYYY-MM-DD, etc.

### Autenticação por Tipo de API
- **APIs Públicas**: Registro/Atualização (`@csrf_exempt`)
- **APIs Privadas**: Consultas e Dashboard (requerem login)

---

## 🔗 Endpoints Disponíveis

### 📝 APIs de Registro/Atualização (POST - Públicas)
```
POST /api/leads/registrar/
POST /api/leads/atualizar/
POST /api/prospectos/registrar/
POST /api/prospectos/atualizar/
POST /api/historicos/registrar/
POST /api/historicos/atualizar/
POST /api/verificar-relacionamentos/
```

### 🔍 APIs de Consulta (GET - Privadas)
```
GET /api/consultar/leads/
GET /api/consultar/historicos/
```

### 📊 APIs do Dashboard (GET - Privadas)
```
GET /api/dashboard/data/
GET /api/dashboard/charts/
GET /api/dashboard/tables/
GET /api/dashboard/leads/
GET /api/dashboard/prospectos/
GET /api/dashboard/historico/
GET /api/dashboard/contatos-realtime/
GET /api/dashboard/conversoes/
```

### 💰 APIs de Validação de Vendas (POST - Privadas)
```
POST /api/vendas/aprovar/
POST /api/vendas/rejeitar/
GET /api/vendas/historico-contatos/
```

---

## 🎯 Sistema de Status Configuráveis

O sistema agora permite configurar status via Django Admin:

### Grupos de Status
- **`lead_status_api`**: Status dos leads
- **`prospecto_status`**: Status dos prospectos  
- **`historico_status`**: Status dos contatos

### Como Gerenciar
1. Acesse Django Admin → **Status Configuravel**
2. Adicione/Edite/Desative status conforme necessário
3. Campos: `grupo`, `codigo`, `rotulo`, `ativo`, `ordem`

### Status Padrão

#### Lead Status API
- `pendente` → "Pendente"
- `processado` → "Processado"
- `erro` → "Erro"
- `sucesso` → "Sucesso"
- `rejeitado` → "Rejeitado"
- `aguardando_retry` → "Aguardando Retry"
- `processamento_manual` → "Processamento Manual"

#### Prospecto Status
- `pendente` → "Pendente"
- `processando` → "Processando"
- `processado` → "Processado"
- `erro` → "Erro"
- `finalizado` → "Finalizado"
- `cancelado` → "Cancelado"
- `aguardando_validacao` → "Aguardando Validação"
- `validacao_aprovada` → "Validação Aprovada"
- `validacao_rejeitada` → "Validação Rejeitada"

#### Histórico Status
- `fluxo_inicializado` → "Fluxo Inicializado"
- `fluxo_finalizado` → "Fluxo Finalizado"
- `transferido_humano` → "Transferido para Humano"
- `chamada_perdida` → "Chamada Perdida"
- `ocupado` → "Ocupado"
- `desligou` → "Desligou"
- `nao_atendeu` → "Não Atendeu"
- `abandonou_fluxo` → "Abandonou o Fluxo"
- `numero_invalido` → "Número Inválido"
- `erro_sistema` → "Erro do Sistema"
- `convertido_lead` → "Convertido em Lead"
- `venda_confirmada` → "Venda Confirmada"
- `venda_rejeitada` → "Venda Rejeitada"
- `venda_sem_viabilidade` → "Venda Sem Viabilidade"
- `cliente_desistiu` → "Cliente Desistiu"
- `aguardando_validacao` → "Aguardando Validação"
- `followup_agendado` → "Follow-up Agendado"
- `nao_qualificado` → "Não Qualificado"

---

## 📋 APIs de Registro/Atualização

### 👤 LeadProspecto APIs

#### POST `/api/leads/registrar/`

**Campos aceitos:**

| Campo | Tipo | Obrigatório | Padrão | Observações |
|-------|------|-------------|---------|-------------|
| nome_razaosocial | string | ✅ | — | Nome/Razão social |
| telefone | string | ✅ | — | Formato: `+5585999999999` |
| email | string | ❌ | — | Email válido |
| valor | decimal | ❌ | 0.00 | Valor monetário |
| empresa | string | ❌ | — | Nome da empresa |
| origem | string | ❌ | `site` | Valores: `site`, `facebook`, `instagram`, `google`, `whatsapp`, `indicacao`, `telefone`, `email`, `outros` |
| status_api | string | ❌ | `pendente` | **Configurável via admin** |
| id_hubsoft | string | ❌ | — | Para relacionamento automático |
| cpf_cnpj | string | ❌ | — | CPF ou CNPJ |
| endereco | text | ❌ | — | Endereço completo |
| rua | string | ❌ | — | Logradouro |
| numero_residencia | string | ❌ | — | Número |
| bairro | string | ❌ | — | Bairro |
| cidade | string | ❌ | — | Cidade |
| estado | string | ❌ | — | UF (2 caracteres) |
| cep | string | ❌ | — | CEP |
| id_plano_rp | int | ❌ | — | ID do plano RP |
| id_dia_vencimento | int | ❌ | — | ID dia vencimento |
| id_vendedor_rp | int | ❌ | — | ID vendedor RP |
| data_nascimento | date | ❌ | — | Formatos: DD/MM/YYYY, YYYY-MM-DD |
| observacoes | text | ❌ | — | Observações |
| canal_entrada | string | ❌ | — | Canal de entrada |
| tipo_entrada | string | ❌ | — | Valores: `contato_whatsapp`, `cadastro_site`, `telefone`, `formulario`, `importacao`, `api_externa` |
| score_qualificacao | int | ❌ | — | 1 a 10 |
| tentativas_contato | int | ❌ | 0 | Contador |
| data_ultimo_contato | datetime | ❌ | — | Último contato |
| motivo_rejeicao | text | ❌ | — | Motivo se rejeitado |
| custo_aquisicao | decimal | ❌ | — | Custo de aquisição |
| ativo | boolean | ❌ | true | Lead ativo |

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/leads/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_razaosocial": "Maria Silva",
    "telefone": "+5585999999999",
    "email": "maria@exemplo.com",
    "origem": "whatsapp",
    "valor": 1500.50,
    "empresa": "Maria LTDA",
    "data_nascimento": "14/11/1985",
    "id_hubsoft": "HUB123"
  }'
```

**Resposta (201):**
```json
{
  "success": true,
  "id": 123,
  "lead": {
    "id": 123,
    "nome_razaosocial": "Maria Silva",
    "telefone": "+5585999999999",
    "status_api": "pendente",
    "data_cadastro": "2025-08-15T15:04:05.123456Z",
    "origem_display": "WhatsApp",
    "status_api_display": "Pendente"
  }
}
```

#### POST `/api/leads/atualizar/`

**Parâmetros obrigatórios:**
- `termo_busca`: Campo para filtrar (ex: `id`, `email`, `telefone`, `id_hubsoft`)
- `busca`: Valor a buscar

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/leads/atualizar/ \
  -H "Content-Type: application/json" \
  -d '{
    "termo_busca": "id_hubsoft",
    "busca": "HUB123",
    "status_api": "processado",
    "score_qualificacao": 8,
    "data_nascimento": "14/11/1985"
  }'
```

### 🎯 Prospecto APIs

#### POST `/api/prospectos/registrar/`

**Campos aceitos:**

| Campo | Tipo | Obrigatório | Padrão | Observações |
|-------|------|-------------|---------|-------------|
| nome_prospecto | string | ✅ | — | Nome do prospecto |
| lead | int | ❌ | — | ID do LeadProspecto |
| lead_id | int | ❌ | — | Alternativa a `lead` |
| id_prospecto_hubsoft | string | ❌ | — | ID único Hubsoft |
| status | string | ❌ | `pendente` | **Configurável via admin** |
| prioridade | int | ❌ | 1 | 1=baixa, 5=alta |
| score_conversao | decimal | ❌ | — | 0-100% |
| dados_processamento | JSON | ❌ | — | Dados do processamento |
| resultado_processamento | JSON | ❌ | — | Resultado do processamento |
| tentativas_processamento | int | ❌ | 0 | Contador |
| tempo_processamento | decimal | ❌ | — | Segundos |
| erro_processamento | text | ❌ | — | Detalhes do erro |
| data_processamento | datetime | ❌ | — | Data do processamento |
| data_inicio_processamento | datetime | ❌ | — | Início |
| data_fim_processamento | datetime | ❌ | — | Fim |
| usuario_processamento | string | ❌ | — | Usuário responsável |

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/prospectos/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_prospecto": "João da Silva",
    "lead": 123,
    "id_prospecto_hubsoft": "HUB123",
    "status": "pendente",
    "prioridade": 3,
    "score_conversao": 75.5
  }'
```

#### POST `/api/prospectos/atualizar/`

Similar ao lead, usa `termo_busca` e `busca` para localizar o prospecto.

### 📞 HistoricoContato APIs

#### POST `/api/historicos/registrar/`

**Campos aceitos:**

| Campo | Tipo | Obrigatório | Padrão | Observações |
|-------|------|-------------|---------|-------------|
| telefone | string | ✅ | — | Número do telefone |
| status | string | ✅ | — | **Configurável via admin** |
| lead | int | ❌ | — | ID do LeadProspecto |
| lead_id | int | ❌ | — | Alternativa a `lead` |
| nome_contato | string | ❌ | — | Nome identificado |
| data_hora_contato | datetime | ❌ | now | Data/hora do contato |
| duracao_segundos | int | ❌ | — | Duração em segundos |
| transcricao | text | ❌ | — | Transcrição da conversa |
| observacoes | text | ❌ | — | Observações |
| ip_origem | ip | ❌ | — | IP de origem |
| user_agent | text | ❌ | — | User agent |
| dados_extras | JSON | ❌ | — | Dados extras |
| sucesso | boolean | ❌ | false | Contato bem-sucedido |
| converteu_lead | boolean | ❌ | false | Converteu em lead |
| data_conversao_lead | datetime | ❌ | — | Data da conversão |
| converteu_venda | boolean | ❌ | false | Converteu em venda |
| data_conversao_venda | datetime | ❌ | — | Data da venda |
| valor_venda | decimal | ❌ | — | Valor da venda |
| origem_contato | string | ❌ | — | Origem do contato |
| identificador_cliente | string | ❌ | — | ID único do cliente |

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/historicos/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "+5585988887777",
    "status": "fluxo_inicializado",
    "lead": 123,
    "nome_contato": "João",
    "duracao_segundos": 42,
    "sucesso": true,
    "origem_contato": "telefone"
  }'
```

---

## 🔍 APIs de Consulta

### GET `/api/consultar/leads/`

**Parâmetros de filtro:**
- `id`: ID específico
- `search`: Busca em nome, email, telefone, empresa, CPF/CNPJ, id_hubsoft
- `origem`: Filtro por origem
- `status_api`: Filtro por status
- `ativo`: true/false
- `data_inicio`: Data início (YYYY-MM-DD)
- `data_fim`: Data fim (YYYY-MM-DD)
- `page`: Página (padrão: 1)
- `per_page`: Itens por página (1-100, padrão: 20)
- `ordering`: Ordenação (campos: id, data_cadastro, nome_razaosocial, valor)

**Exemplo:**
```bash
curl -H "Cookie: sessionid=SEU_SESSION_ID" \
  "http://localhost:8000/api/consultar/leads/?search=joao&origem=whatsapp&page=1"
```

### GET `/api/consultar/historicos/`

**Parâmetros de filtro:**
- `id`: ID específico  
- `telefone`: Busca por telefone
- `lead_id`: Filtro por lead
- `status`: Filtro por status
- `sucesso`: true/false
- `converteu_lead`: true/false
- `converteu_venda`: true/false
- `data_inicio`: Data início (YYYY-MM-DD)
- `data_fim`: Data fim (YYYY-MM-DD)
- `page`: Página
- `per_page`: Itens por página
- `ordering`: Ordenação (campos: id, data_hora_contato, telefone, status)

---

## 📊 APIs do Dashboard

### GET `/api/dashboard/data/`
Retorna métricas principais: atendimentos, leads, prospectos, vendas com variações.

### GET `/api/dashboard/charts/`
Dados para gráficos dos últimos 7 dias.

### GET `/api/dashboard/prospectos/`
Lista de prospectos com filtros e paginação.

---

## 💰 APIs de Validação de Vendas

### POST `/api/vendas/aprovar/`
```json
{
  "prospecto_id": 123,
  "observacoes": "Venda aprovada após validação"
}
```

### POST `/api/vendas/rejeitar/`
```json
{
  "prospecto_id": 123,
  "motivo_rejeicao": "Dados inconsistentes"
}
```

---

## 🔄 API de Verificação de Relacionamentos

### POST `/api/verificar-relacionamentos/`

Verifica e cria relacionamentos automáticos entre leads e prospectos baseado no `id_hubsoft`.

**Exemplo:**
```bash
curl -X POST http://localhost:8000/api/verificar-relacionamentos/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Resposta:**
```json
{
  "success": true,
  "relacionamentos_criados": 5,
  "message": "Verificação concluída. 5 relacionamentos criados."
}
```

---

## 📝 Sistema de Logs

Todas as operações são automaticamente registradas com:
- **Nível**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Módulo**: Função que executou a operação
- **Mensagem**: Descrição da operação
- **Dados extras**: Informações detalhadas em JSON
- **Usuário e IP**: Quando disponível

---

## 🔧 Suporte a Formatos de Data

O sistema aceita múltiplos formatos:

**Para campos de data:**
- `14/11/2002` (brasileiro)
- `2002-11-14` (ISO)
- `14-11-2002`
- `2002/11/14`
- `11/14/2002`

**Para campos de datetime:**
- `14/11/2002 15:30:00`
- `14/11/2002 15:30`
- `2002-11-14 15:30:00`
- `2002-11-14T15:30:00`

---

## ⚠️ Códigos de Resposta

- `200 OK`: Operação bem-sucedida
- `201 Created`: Registro criado
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Registro não encontrado
- `405 Method Not Allowed`: Método não permitido
- `500 Internal Server Error`: Erro interno

---

## 🚀 Exemplos Python

```python
import requests

# Criar Lead
response = requests.post(
    "http://localhost:8000/api/leads/registrar/",
    json={
        "nome_razaosocial": "Empresa ABC",
        "telefone": "+5585999999999",
        "email": "contato@empresa.com",
        "id_hubsoft": "HUB456"
    }
)

# Consultar Leads (com autenticação)
response = requests.get(
    "http://localhost:8000/api/consultar/leads/",
    params={"search": "empresa", "page": 1},
    cookies={"sessionid": "seu_session_id"}
)

# Verificar relacionamentos
response = requests.post(
    "http://localhost:8000/api/verificar-relacionamentos/",
    json={}
)
```
