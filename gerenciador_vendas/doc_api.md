## Documentação das APIs – Dashboard Comercial

### Visão geral
- **Formato**: JSON (UTF-8)
- **Header**: `Content-Type: application/json`
- **Autenticação**: APIs de registro/atualização são públicas (`@csrf_exempt`), APIs de consulta requerem autenticação
- **Logs**: Todas as operações são automaticamente registradas no sistema
- **Status Dinâmicos**: Status são configuráveis via admin
- **Relacionamentos Automáticos**: Sistema relaciona automaticamente leads e prospectos via `id_hubsoft`

### Endpoints Disponíveis

#### APIs de Registro/Atualização (POST - Públicas)
- `POST /api/leads/registrar/`
- `POST /api/leads/atualizar/`  
- `POST /api/prospectos/registrar/`
- `POST /api/prospectos/atualizar/`
- `POST /api/historicos/registrar/`
- `POST /api/historicos/atualizar/`
- `POST /api/verificar-relacionamentos/`

#### APIs de Consulta (GET - Requerem Autenticação)
- `GET /api/consultar/leads/`
- `GET /api/consultar/historicos/`

#### APIs do Dashboard (GET - Requerem Autenticação)
- `GET /api/dashboard/data/`
- `GET /api/dashboard/charts/`
- `GET /api/dashboard/tables/`
- `GET /api/dashboard/leads/`
- `GET /api/dashboard/prospectos/`
- `GET /api/dashboard/historico/`
- `GET /api/dashboard/contatos-realtime/`
- `GET /api/dashboard/conversoes/`

#### APIs de Validação de Vendas (POST - Requerem Autenticação)  
- `POST /api/vendas/aprovar/`
- `POST /api/vendas/rejeitar/`
- `GET /api/vendas/historico-contatos/`

### Convenções de dados
- Datas em ISO 8601: por exemplo, `2025-08-13T15:04:05Z` ou `2025-08-13T15:04:05.123456Z`
- Decimais como número JSON (não string)
- Booleanos como `true`/`false`
- FKs podem ser enviadas como `lead` (número, id) ou `lead_id` (número)

### Códigos de resposta
- `201 Created`: criação OK
- `200 OK`: atualização OK
- `400 Bad Request`: JSON inválido, campos inválidos/ausentes, múltiplos registros no update, termo de busca inválido
- `404 Not Found`: registro não encontrado (update)
- `405 Method Not Allowed`: método não permitido


---

## Endpoints – Leads (`LeadProspecto`)

### POST `/api/leads/registrar/`
Cria um lead.

Campos aceitos (criação):

| Campo | Tipo | Obrigatório | Padrão/Validação | Observações |
|---|---|---|---|---|
| nome_razaosocial | string | Sim | — | — |
| telefone | string | Sim | Regex `^\+?1?\d{9,15}$` | Ex.: `+5585999999999` |
| email | string | Não | email válido | — |
| valor | decimal | Não | default `0.00` | Número JSON |
| empresa | string | Não | — | — |
| origem | string (choice) | Não | default `site` | Valores: `site`, `facebook`, `instagram`, `google`, `whatsapp`, `indicacao`, `telefone`, `email`, `outros` |
| data_cadastro | datetime | Não | default now | Pode ser omitido |
| status_api | string (choice) | Não | default `pendente` | Valores: `pendente`, `processado`, `erro`, `sucesso`, `rejeitado`, `aguardando_retry`, `processamento_manual` |
| id_hubsoft | string | Não | — | Índice para cruzamento |
| cpf_cnpj | string | Não | — | — |
| endereco | text | Não | — | — |
| cidade | string | Não | — | — |
| estado | string | Não | 2 caracteres | UF |
| cep | string | Não | — | — |
| observacoes | text | Não | — | — |
| data_atualizacao | datetime | Não | auto_now | Gerado automaticamente |
| canal_entrada | string (choice) | Não | — | Mesmo conjunto de `origem` |
| tipo_entrada | string (choice) | Não | — | Valores: `contato_whatsapp`, `cadastro_site`, `telefone`, `formulario`, `importacao`, `api_externa` |
| score_qualificacao | int | Não | 1 a 10 | — |
| tentativas_contato | int | Não | default 0 | — |
| data_ultimo_contato | datetime | Não | — | — |
| motivo_rejeicao | text | Não | — | — |
| custo_aquisicao | decimal | Não | — | Número JSON |
| ativo | boolean | Não | default true | — |

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/leads/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_razaosocial": "Maria LTDA",
    "telefone": "+5585999999999",
    "email": "maria@exemplo.com",
    "origem": "whatsapp",
    "valor": 1500.50,
    "empresa": "Maria LTDA",
    "tipo_entrada": "contato_whatsapp"
  }'
```

Resposta (201):
```json
{
  "success": true,
  "id": 123,
  "lead": {
    "id": 123,
    "nome_razaosocial": "Maria LTDA",
    "telefone": "+5585999999999",
    "status_api": "pendente",
    "data_cadastro": "2025-08-13T15:04:05.123456Z",
    "origem_display": "WhatsApp",
    "status_api_display": "Pendente"
  }
}
```

### POST `/api/leads/atualizar/`
Atualiza um lead por filtro dinâmico.

Parâmetros obrigatórios:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| termo_busca | string | Sim | Nome do campo para filtrar (ex.: `id`, `email`, `telefone`, `id_hubsoft`, `cpf_cnpj`) |
| busca | any | Sim | Valor a buscar para o `termo_busca` |

Demais campos enviados (qualquer campo concreto de `LeadProspecto`, exceto `id`/`pk`) serão atualizados.

Regras de retorno:
- 404 se nenhum registro
- 400 se múltiplos registros para o filtro
- 400 se `termo_busca` inválido ou sem campos para atualizar

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/leads/atualizar/ \
  -H "Content-Type: application/json" \
  -d '{
    "termo_busca": "id",
    "busca": 123,
    "status_api": "processado",
    "score_qualificacao": 8,
    "tentativas_contato": 1
  }'
```


---

## Endpoints – Prospectos (`Prospecto`)

### POST `/api/prospectos/registrar/`
Cria um prospecto.

Campos aceitos (criação):

| Campo | Tipo | Obrigatório | Padrão/Validação | Observações |
|---|---|---|---|---|
| nome_prospecto | string | Sim | — | — |
| lead | int (FK) | Não | — | Id de `LeadProspecto` (ou usar `lead_id`) |
| lead_id | int | Não | — | Alternativa a `lead` |
| id_prospecto_hubsoft | string | Não | unique | — |
| status | string (choice) | Não | default `pendente` | `pendente`, `processando`, `processado`, `erro`, `finalizado`, `cancelado`, `aguardando_validacao`, `validacao_aprovada`, `validacao_rejeitada` |
| data_criacao | datetime | Não | default now | — |
| data_processamento | datetime | Não | — | — |
| tentativas_processamento | int | Não | default 0 | — |
| tempo_processamento | decimal | Não | — | Segundos, número JSON |
| erro_processamento | text | Não | — | — |
| data_inicio_processamento | datetime | Não | — | — |
| data_fim_processamento | datetime | Não | — | — |
| usuario_processamento | string | Não | — | — |
| score_conversao | decimal | Não | 0–100 | Número JSON |
| prioridade | int | Não | default 1 | 1=baixa, 5=alta |
| dados_processamento | JSON | Não | — | — |
| resultado_processamento | JSON | Não | — | — |

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/prospectos/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome_prospecto": "Fulano da Silva",
    "lead": 123,
    "id_prospecto_hubsoft": "HBS-0001",
    "status": "pendente",
    "prioridade": 3
  }'
```

Resposta (201):
```json
{
  "success": true,
  "id": 45,
  "prospecto": { "id": 45, "nome_prospecto": "Fulano da Silva", "status": "pendente" }
}
```

Erros possíveis:
- 404: `Lead informado não encontrado` (quando `lead`/`lead_id` não existe)
- 400: JSON inválido, campos inválidos

### POST `/api/prospectos/atualizar/`
Atualiza um prospecto por filtro dinâmico.

Parâmetros obrigatórios:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| termo_busca | string | Sim | Ex.: `id`, `id_prospecto_hubsoft`, `nome_prospecto`, `lead_id` |
| busca | any | Sim | Valor a buscar |

Demais campos enviados (qualquer campo concreto de `Prospecto`, exceto `id`/`pk`) serão atualizados. Para relacionar a um lead, envie `lead` (int) ou `lead_id` (int).

Regras de retorno: 404 quando não encontrado, 400 quando múltiplos registros, termo inválido ou nenhum campo de atualização.

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/prospectos/atualizar/ \
  -H "Content-Type: application/json" \
  -d '{
    "termo_busca": "id_prospecto_hubsoft",
    "busca": "HBS-0001",
    "status": "processando",
    "usuario_processamento": "operador01"
  }'
```


---

## Endpoints – Histórico de Contato (`HistoricoContato`)

### POST `/api/historicos/registrar/`
Cria um registro de histórico de contato/chamada.

Campos aceitos (criação):

| Campo | Tipo | Obrigatório | Padrão/Validação | Observações |
|---|---|---|---|---|
| telefone | string | Sim | — | Ex.: `+5585988887777` |
| status | string (choice) | Sim | — | Ver lista abaixo |
| lead | int (FK) | Não | — | Id de `LeadProspecto` (ou usar `lead_id`) |
| lead_id | int | Não | — | Alternativa a `lead` |
| data_hora_contato | datetime | Não | default now | — |
| nome_contato | string | Não | — | — |
| duracao_segundos | int | Não | — | — |
| transcricao | text | Não | — | — |
| observacoes | text | Não | — | — |
| ip_origem | ip | Não | — | — |
| user_agent | text | Não | — | — |
| dados_extras | JSON | Não | — | — |
| sucesso | boolean | Não | default false | — |
| converteu_lead | boolean | Não | default false | — |
| data_conversao_lead | datetime | Não | — | — |
| converteu_venda | boolean | Não | default false | — |
| data_conversao_venda | datetime | Não | — | — |
| valor_venda | decimal | Não | — | Número JSON |
| origem_contato | string (choice) | Não | — | Mesmo conjunto de `origem` do lead |
| identificador_cliente | string | Não | — | Agrupar contatos do mesmo cliente |

Choices para `status`:
- Fluxo: `fluxo_inicializado`, `fluxo_finalizado`, `transferido_humano`
- Problemas: `chamada_perdida`, `ocupado`, `desligou`, `nao_atendeu`, `abandonou_fluxo`, `numero_invalido`, `erro_sistema`
- Conversão: `convertido_lead`, `venda_confirmada`, `venda_rejeitada`
- Extras: `venda_sem_viabilidade`, `cliente_desistiu`, `aguardando_validacao`, `followup_agendado`, `nao_qualificado`

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/historicos/registrar/ \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "+5585988887777",
    "status": "fluxo_inicializado",
    "lead": 123,
    "nome_contato": "João",
    "duracao_segundos": 42,
    "origem_contato": "telefone",
    "observacoes": "Ligação caiu"
  }'
```

Resposta (201):
```json
{
  "success": true,
  "id": 456,
  "historico": { "id": 456, "telefone": "+5585988887777", "status": "fluxo_inicializado" }
}
```

Erros possíveis:
- 404: `Lead informado não encontrado` (quando `lead`/`lead_id` não existe)
- 400: JSON inválido, campos inválidos

### POST `/api/historicos/atualizar/`
Atualiza um histórico por filtro dinâmico.

Parâmetros obrigatórios:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| termo_busca | string | Sim | Ex.: `id` (recomendado), `telefone`, `identificador_cliente`, `lead_id` |
| busca | any | Sim | Valor a buscar |

Demais campos enviados (qualquer campo concreto de `HistoricoContato`, exceto `id`/`pk`) serão atualizados. Para vincular a um lead, envie `lead` (int) ou `lead_id` (int).

Regras de retorno: 404 quando não encontrado, 400 quando múltiplos registros, termo inválido ou nenhum campo de atualização.

Exemplo (cURL):
```bash
curl -X POST http://localhost:8000/api/historicos/atualizar/ \
  -H "Content-Type: application/json" \
  -d '{
    "termo_busca": "id",
    "busca": 456,
    "status": "fluxo_finalizado",
    "converteu_lead": true
  }'
```


---

## Respostas e serialização
Além dos campos do modelo, as respostas podem incluir:
- Datas auto: `data_cadastro`, `data_atualizacao`, `data_criacao`, `data_processamento`, `data_inicio_processamento`, `data_fim_processamento`, `data_hora_contato`, `data_conversao_lead`, `data_conversao_venda` (em ISO 8601)
- Displays de choices (quando aplicável):
  - `status_api_display`, `origem_display` (Lead)
  - `status_display`, `origem_contato_display` (Histórico)

Formato de erro (exemplos):
```json
{ "error": "JSON inválido" }
{ "error": "Campos obrigatórios ausentes: nome_razaosocial, telefone" }
{ "error": "Registro não encontrado" }
{ "error": "Múltiplos registros encontrados (2). Refine a busca." }
{ "error": "termo_busca inválido para LeadProspecto" }
{ "error": "Lead informado não encontrado" }
```


---

## Boas práticas e dicas
- Prefira `termo_busca = "id"` nos updates para evitar múltiplos resultados
- Respeite valores de choices e formatos (telefone, email, datas ISO)
- Envie ao menos um campo de atualização além de `termo_busca`/`busca`
- Para FKs use `lead` (int) ou `lead_id` (int)
- Campos com `auto_now`/`default now` são geridos pelo sistema; não é necessário enviar


---

## Exemplos rápidos (Python requests)
```python
import requests

# Criar Lead
r = requests.post(
    "http://localhost:8000/api/leads/registrar/",
    json={"nome_razaosocial": "ACME", "telefone": "+5585999999999"}
)
print(r.status_code, r.json())

# Atualizar Prospecto por id
r = requests.post(
    "http://localhost:8000/api/prospectos/atualizar/",
    json={"termo_busca": "id", "busca": 10, "status": "finalizado"}
)
print(r.status_code, r.json())
```


### APIs de Consulta (GET) — Leads e Histórico de Contato

Estas APIs permitem consultar `LeadProspecto` e `HistoricoContato` com filtros, paginação e ordenação.

### Autenticação

- **Obrigatória**: o projeto usa um middleware que exige usuário autenticado.
- Faça login em `/admin/login/` antes de chamar as APIs (cookies de sessão do Django).
- Em chamadas via `curl`/Postman, inclua o cookie de sessão: `Cookie: sessionid=SEU_SESSION_ID`.

### Convenções

- Datas: `YYYY-MM-DD` (ex.: `2025-01-31`).
- Booleanos: `true`/`false` (aceita também `1/0`, `sim/nao`).
- Paginação: `page` (1..N), `per_page` (1..100, padrão 20).
- Ordenação: use `ordering` com campos permitidos; prefixe com `-` para desc (ex.: `-data_cadastro`).

---

### GET /api/consultar/leads/

- **Parâmetros de filtro**:
  - **id**: filtra por ID exato
  - **search**: busca parcial em `nome_razaosocial`, `email`, `telefone`, `empresa`, `cpf_cnpj`, `id_hubsoft`
  - **origem**: ex.: `whatsapp`, `site`, `google`, `facebook`, `instagram`, `indicacao`, `telefone`, `email`, `outros`
  - **status_api**: ex.: `pendente`, `processado`, `erro`, `sucesso`, `rejeitado`, `aguardando_retry`, `processamento_manual`
  - **ativo**: `true` | `false`
  - **data_inicio**: filtra `data_cadastro` a partir de (inclusive)
  - **data_fim**: filtra `data_cadastro` até (inclusive)
- **Paginação**: `page`, `per_page`
- **Ordenação** (`ordering`): `id`, `data_cadastro`, `data_atualizacao`, `nome_razaosocial`, `valor` (use `-` para desc)

Exemplos:

```bash
curl -s \
  -H "Cookie: sessionid=SEU_SESSION_ID" \
  "http://localhost:8000/api/consultar/leads/?search=joao&origem=whatsapp&ordering=-data_cadastro&page=1&per_page=20"
```

```bash
curl -s \
  -H "Cookie: sessionid=SEU_SESSION_ID" \
  "http://localhost:8000/api/consultar/leads/?ativo=true&data_inicio=2025-01-01&data_fim=2025-01-31"
```

Resposta (exemplo):

```json
{
  "results": [
    {
      "id": 123,
      "nome_razaosocial": "João da Silva",
      "email": "joao@exemplo.com",
      "telefone": "+5551999999999",
      "empresa": "Empresa X",
      "origem": "whatsapp",
      "status_api": "pendente",
      "data_cadastro": "2025-01-20T12:34:56",
      "data_atualizacao": "2025-01-21T08:00:00",
      "valor": 1500.0,
      "valor_formatado": "R$ 1.500,00",
      "origem_display": "WhatsApp",
      "status_api_display": "Pendente"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1,
  "ordering": "-data_cadastro"
}
```

---

### GET /api/consultar/historicos/

- **Parâmetros de filtro**:
  - **id**: filtra por ID exato
  - **telefone**: busca parcial
  - **lead_id**: filtra contatos do lead
  - **status**: ex.: `fluxo_inicializado`, `fluxo_finalizado`, `transferido_humano`, `convertido_lead`, `venda_confirmada`, etc.
  - **sucesso**: `true` | `false`
  - **converteu_lead**: `true` | `false`
  - **converteu_venda**: `true` | `false`
  - **data_inicio**: filtra `data_hora_contato` a partir de (inclusive)
  - **data_fim**: filtra `data_hora_contato` até (inclusive)
- **Paginação**: `page`, `per_page`
- **Ordenação** (`ordering`): `id`, `data_hora_contato`, `telefone`, `status` (use `-` para desc)

Exemplos:

```bash
curl -s \
  -H "Cookie: sessionid=SEU_SESSION_ID" \
  "http://localhost:8000/api/consultar/historicos/?telefone=55999&sucesso=true&data_inicio=2025-01-01&data_fim=2025-01-31&ordering=-data_hora_contato"
```

```bash
curl -s \
  -H "Cookie: sessionid=SEU_SESSION_ID" \
  "http://localhost:8000/api/consultar/historicos/?lead_id=10&converteu_venda=true&page=1&per_page=10"
```

Resposta (exemplo):

```json
{
  "results": [
    {
      "id": 987,
      "telefone": "+5551999999999",
      "status": "venda_confirmada",
      "data_hora_contato": "2025-01-25T09:15:00",
      "duracao_segundos": 180,
      "converteu_lead": true,
      "converteu_venda": true,
      "valor_venda": 299.9,
      "status_display": "Venda Confirmada",
      "duracao_formatada": "3m 0s",
      "valor_venda_formatado": "R$ 299,90",
      "lead_info": {
        "id": 10,
        "nome_razaosocial": "Empresa ABC",
        "telefone": "+555188888888",
        "empresa": "Empresa ABC"
      }
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1,
  "ordering": "-data_hora_contato"
}
```

---

### Notas

- Em caso de erro de validação de método, a API retorna `405`.
- Erros internos retornam `500` com mensagem simplificada.
- Se precisar tornar as rotas públicas, isente-as no `LoginRequiredMiddleware` (arquivo `vendas_web/middleware.py`).


