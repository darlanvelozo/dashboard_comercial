# APIs de Atendimento - Dashboard Comercial

Este documento descreve as APIs de consulta GET para os modelos de atendimento implementados no sistema.

## 📋 Visão Geral

As APIs de atendimento permitem consultar dados dos seguintes modelos:
- **FluxoAtendimento**: Fluxos de atendimento configurados
- **QuestaoFluxo**: Questões individuais dentro dos fluxos
- **AtendimentoFluxo**: Sessões de atendimento específicas
- **RespostaQuestao**: Respostas detalhadas das questões

## 🔐 Autenticação

Todas as APIs de consulta requerem autenticação via sessão Django. Faça login em `/admin/login/` primeiro.

## 📡 Endpoints Disponíveis

### 1. Consultar Fluxos de Atendimento

**GET** `/api/consultar/fluxos/`

Consulta fluxos de atendimento com filtros e paginação.

#### Parâmetros de Query:
- `search` (string): Busca por nome, descrição ou tags
- `tipo_fluxo` (string): Filtro por tipo de fluxo
  - Valores: `qualificacao`, `vendas`, `suporte`, `onboarding`, `outros`
- `ativo` (boolean): Filtro por status ativo
- `status` (string): Filtro por status configurável
- `data_inicio` (string): Data de início (formato: YYYY-MM-DD)
- `data_fim` (string): Data de fim (formato: YYYY-MM-DD)
- `page` (integer): Número da página (padrão: 1)
- `per_page` (integer): Itens por página (padrão: 20, máximo: 100)
- `ordering` (string): Campo para ordenação (prefixo `-` para descendente)

#### Exemplo de Uso:
```bash
# Listar todos os fluxos
GET /api/consultar/fluxos/

# Buscar fluxos de qualificação ativos
GET /api/consultar/fluxos/?tipo_fluxo=qualificacao&ativo=true

# Buscar fluxos criados nos últimos 30 dias
GET /api/consultar/fluxos/?data_inicio=2024-01-01&data_fim=2024-01-31

# Paginação e ordenação
GET /api/consultar/fluxos/?page=2&per_page=10&ordering=-data_criacao
```

#### Resposta:
```json
{
  "results": [
    {
      "id": 1,
      "nome": "Qualificação Básica",
      "descricao": "Fluxo para qualificar leads",
      "tipo_fluxo": "qualificacao",
      "ativo": true,
      "status": "ativo",
      "total_questoes": 5,
      "total_atendimentos": 12,
      "taxa_completacao": "75.0%"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1,
  "ordering": "-data_criacao"
}
```

### 2. Consultar Questões de Fluxo

**GET** `/api/consultar/questoes/`

Consulta questões de fluxo com filtros e paginação.

#### Parâmetros de Query:
- `fluxo_id` (integer): Filtro por ID do fluxo
- `search` (string): Busca por título ou descrição
- `tipo_questao` (string): Filtro por tipo de questão
  - Valores: `texto`, `numero`, `email`, `telefone`, `cpf_cnpj`, `cep`, `endereco`, `select`, `multiselect`, `data`, `hora`, `data_hora`, `boolean`, `escala`, `arquivo`
- `tipo_validacao` (string): Filtro por tipo de validação
  - Valores: `obrigatoria`, `opcional`, `condicional`
- `ativo` (boolean): Filtro por status ativo
- `indice` (integer): Filtro por índice específico
- `page` (integer): Número da página
- `per_page` (integer): Itens por página
- `ordering` (string): Campo para ordenação

#### Exemplo de Uso:
```bash
# Listar todas as questões
GET /api/consultar/questoes/

# Questões de um fluxo específico
GET /api/consultar/questoes/?fluxo_id=1

# Questões obrigatórias de seleção
GET /api/consultar/questoes/?tipo_questao=select&tipo_validacao=obrigatoria

# Buscar por texto
GET /api/consultar/questoes/?search=telefone
```

#### Resposta:
```json
{
  "results": [
    {
      "id": 1,
      "fluxo_id": 1,
      "fluxo_nome": "Qualificação Básica",
      "indice": 1,
      "titulo": "Qual é o seu nome?",
      "tipo_questao": "texto",
      "tipo_validacao": "obrigatoria",
      "ativo": true
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1,
  "ordering": "fluxo__id, indice"
}
```

### 3. Consultar Atendimentos de Fluxo

**GET** `/api/consultar/atendimentos/`

Consulta atendimentos de fluxo com filtros e paginação.

#### Parâmetros de Query:
- `lead_id` (integer): Filtro por ID do lead
- `fluxo_id` (integer): Filtro por ID do fluxo
- `status` (string): Filtro por status
  - Valores: `iniciado`, `em_andamento`, `pausado`, `completado`, `abandonado`, `erro`, `cancelado`, `aguardando_validacao`, `validado`, `rejeitado`
- `search` (string): Busca por nome do lead, fluxo ou observações
- `data_inicio` (string): Data de início (formato: YYYY-MM-DD)
- `data_fim` (string): Data de fim (formato: YYYY-MM-DD)
- `score_min` (integer): Score de qualificação mínimo (1-10)
- `score_max` (integer): Score de qualificação máximo (1-10)
- `page` (integer): Número da página
- `per_page` (integer): Itens por página
- `ordering` (string): Campo para ordenação

#### Exemplo de Uso:
```bash
# Listar todos os atendimentos
GET /api/consultar/atendimentos/

# Atendimentos de um lead específico
GET /api/consultar/atendimentos/?lead_id=123

# Atendimentos completados com score alto
GET /api/consultar/atendimentos/?status=completado&score_min=8

# Atendimentos de um fluxo específico
GET /api/consultar/atendimentos/?fluxo_id=1&status=em_andamento
```

#### Resposta:
```json
{
  "results": [
    {
      "id": 1,
      "lead_id": 123,
      "lead_nome": "João Silva",
      "fluxo_id": 1,
      "fluxo_nome": "Qualificação Básica",
      "status": "em_andamento",
      "status_display": "Em Andamento",
      "questao_atual": 3,
      "progresso_percentual": 60.0,
      "score_qualificacao": 7
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1,
  "ordering": "-data_inicio"
}
```

### 4. Consultar Respostas de Questões

**GET** `/api/consultar/respostas/`

Consulta respostas de questões com filtros e paginação.

#### Parâmetros de Query:
- `atendimento_id` (integer): Filtro por ID do atendimento
- `questao_id` (integer): Filtro por ID da questão
- `valida` (boolean): Filtro por respostas válidas
- `data_inicio` (string): Data de início (formato: YYYY-MM-DD)
- `data_fim` (string): Data de fim (formato: YYYY-MM-DD)
- `page` (integer): Número da página
- `per_page` (integer): Itens por página
- `ordering` (string): Campo para ordenação

#### Exemplo de Uso:
```bash
# Listar todas as respostas
GET /api/consultar/respostas/

# Respostas de um atendimento específico
GET /api/consultar/respostas/?atendimento_id=456

# Apenas respostas válidas
GET /api/consultar/respostas/?valida=true

# Respostas de uma questão específica
GET /api/consultar/respostas/?questao_id=789
```

#### Resposta:
```json
{
  "results": [
    {
      "id": 1,
      "atendimento_id": 456,
      "questao_id": 789,
      "questao_titulo": "Qual é o seu nome?",
      "resposta": "João Silva",
      "valida": true,
      "data_resposta": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1,
  "ordering": "-data_resposta"
}
```

## 🧪 Testando as APIs

Para testar as APIs, execute o script de teste:

```bash
cd dashboard_comercial/gerenciador_vendas
python teste_apis_atendimento.py
```

## 📊 Campos de Ordenação Disponíveis

### Fluxos:
- `id`, `nome`, `data_criacao`, `data_atualizacao`, `prioridade`, `tipo_fluxo`

### Questões:
- `id`, `indice`, `titulo`, `tipo_questao`, `ordem_exibicao`

### Atendimentos:
- `id`, `data_inicio`, `data_ultima_atividade`, `questao_atual`, `score_qualificacao`

### Respostas:
- `id`, `data_resposta`, `tentativas`, `tempo_resposta`

## 🔍 Filtros Avançados

### Filtros de Data
- Use formato `YYYY-MM-DD` para filtros de data
- Exemplo: `?data_inicio=2024-01-01&data_fim=2024-01-31`

### Filtros Booleanos
- Aceita: `true`, `false`, `1`, `0`, `sim`, `não`, `yes`, `no`
- Exemplo: `?ativo=true&valida=false`

### Filtros de Score
- Para atendimentos: `score_min` e `score_max` (1-10)
- Exemplo: `?score_min=5&score_max=10`

## 📱 Exemplos de Uso em JavaScript

```javascript
// Consultar fluxos ativos
fetch('/api/consultar/fluxos/?ativo=true')
  .then(response => response.json())
  .then(data => {
    console.log('Fluxos ativos:', data.results);
  });

// Consultar atendimentos de um lead
fetch('/api/consultar/atendimentos/?lead_id=123')
  .then(response => response.json())
  .then(data => {
    console.log('Atendimentos do lead:', data.results);
  });

// Consultar questões de um fluxo com paginação
fetch('/api/consultar/questoes/?fluxo_id=1&page=1&per_page=10')
  .then(response => response.json())
  .then(data => {
    console.log('Questões do fluxo:', data.results);
    console.log('Total de páginas:', data.pages);
  });
```

## ⚠️ Limitações e Considerações

1. **Paginação**: Máximo de 100 itens por página
2. **Autenticação**: Todas as APIs requerem login
3. **Performance**: Use filtros para limitar resultados grandes
4. **Ordenação**: Campos não permitidos são ignorados
5. **Datas**: Use formato ISO (YYYY-MM-DD) para filtros de data

## 🆘 Suporte

Para dúvidas ou problemas com as APIs:
1. Verifique a documentação Swagger em `/api/docs/`
2. Execute os testes para verificar funcionamento
3. Consulte os logs do sistema para erros
4. Verifique se os modelos estão migrados corretamente
