# 🚀 Sistema de Cadastro de Clientes - Megalink

## 📋 Visão Geral

Sistema completo de cadastro de clientes via site que integra automaticamente com o sistema de leads existente. Permite configuração flexível para diferentes empresas e gera automaticamente leads e histórico de contatos.

## ✨ Funcionalidades Principais

### 🎯 **Cadastro em Etapas**
- **Etapa 1**: Seleção de plano de internet
- **Etapa 2**: Dados pessoais (nome, CPF, email, telefone, nascimento)
- **Etapa 3**: Endereço completo
- **Etapa 4**: Resumo e confirmação

### 🔧 **Configuração Flexível**
- Títulos e mensagens personalizáveis
- Campos obrigatórios configuráveis
- Validações ativáveis/desativáveis
- Suporte a múltiplas empresas

### 📊 **Integração Automática**
- Geração automática de leads
- Criação de histórico de contatos
- Status de lead definido como "pendente"
- Rastreamento completo do processo

## 🏗️ Arquitetura do Sistema

### **Modelos Criados**

#### 1. **ConfiguracaoCadastro**
Gerencia todas as configurações da página de cadastro:
- Informações da empresa
- Campos obrigatórios
- Mensagens personalizadas
- Configurações de validação
- Integração com sistema de leads

#### 2. **PlanoInternet**
Gerencia os planos de internet disponíveis:
- Velocidades de download/upload
- Preços e características
- Destaques (popular, premium, econômico)
- Integração com sistemas externos

#### 3. **OpcaoVencimento**
Gerencia as opções de vencimento de fatura:
- Dias de vencimento disponíveis
- Ordem de exibição
- Status ativo/inativo

#### 4. **CadastroCliente**
Armazena todos os cadastros realizados:
- Dados pessoais e endereço
- Plano e vencimento selecionados
- Status do processo
- Integração com lead gerado
- Metadados de auditoria

## 🚀 Como Usar

### **1. Configuração Inicial**

Execute o script de dados iniciais:

```bash
cd dashboard_comercial/gerenciador_vendas
python3 dados_iniciais_cadastro.py
```

### **2. Acessar a Página**

A página de cadastro estará disponível em:
```
http://seu-dominio.com/cadastro/
```

### **3. Configurar no Admin**

Acesse o Django Admin para:
- Personalizar mensagens e títulos
- Gerenciar planos de internet
- Configurar opções de vencimento
- Acompanhar cadastros realizados

## 📱 Interface do Usuário

### **Design Responsivo**
- Interface moderna e intuitiva
- Progress bar visual
- Validação em tempo real
- Máscaras de input (CPF, telefone, CEP)
- Modais de sucesso e erro

### **Validações Implementadas**
- CPF válido
- Email válido
- Telefone válido
- CEP válido
- Campos obrigatórios
- Validação de planos selecionados

## 🔌 APIs Disponíveis

### **1. Cadastro de Cliente**
```
POST /api/cadastro/cliente/
```
Processa o cadastro completo e gera o lead.

### **2. Consulta de Planos**
```
GET /api/planos/internet/
```
Retorna todos os planos ativos.

### **3. Consulta de Vencimentos**
```
GET /api/vencimentos/
```
Retorna todas as opções de vencimento ativas.

## 📊 Fluxo de Dados

### **Processo de Cadastro**

1. **Usuário acessa** a página de cadastro
2. **Seleciona plano** e vencimento
3. **Preenche dados** pessoais
4. **Informa endereço** completo
5. **Confirma informações** e aceita termos
6. **Sistema processa** e valida dados
7. **Lead é criado** automaticamente
8. **Histórico de contato** é registrado
9. **Status do lead** é definido como "pendente"
10. **Usuário recebe** confirmação de sucesso

### **Integração com Sistema Existente**

- **LeadProspecto**: Criado automaticamente com status "pendente"
- **HistoricoContato**: Registra o processo de cadastro como "fluxo_finalizado"
- **Rastreamento**: IP, User Agent, tempo de cadastro
- **Auditoria**: Tentativas, campos preenchidos, erros de validação

## ⚙️ Configurações Disponíveis

### **Configurações Gerais**
- Título e subtítulo da página
- Informações de contato e suporte
- Status ativo/inativo

### **Configurações de Planos**
- Mostrar/ocultar seleção de plano
- Plano padrão para cadastros
- Ordem de exibição dos planos

### **Configurações de Campos**
- CPF obrigatório
- Email obrigatório
- Telefone obrigatório
- Endereço obrigatório

### **Configurações de Validação**
- Validar CEP
- Validar CPF
- Captcha obrigatório
- Limite de tentativas por dia

### **Configurações de Integração**
- Criar lead automático
- Origem padrão do lead
- Enviar email de confirmação
- Enviar WhatsApp de confirmação

## 🎨 Personalização

### **Mensagens Personalizáveis**
- Mensagem de sucesso
- Instruções pós-cadastro
- Títulos das etapas
- Textos de ajuda

### **Estilos CSS**
- Cores e gradientes personalizáveis
- Layout responsivo
- Animações e transições
- Ícones FontAwesome

## 🔒 Segurança

### **Validações Implementadas**
- Validação de CPF real
- Validação de email
- Validação de telefone
- Validação de CEP
- Sanitização de dados
- Proteção contra XSS

### **Auditoria e Rastreamento**
- IP do cliente
- User Agent
- Timestamp de início e fim
- Tempo total de cadastro
- Tentativas por etapa
- Erros de validação

## 📈 Monitoramento

### **Métricas Disponíveis**
- Total de cadastros realizados
- Taxa de conversão
- Tempo médio de cadastro
- Planos mais selecionados
- Vencimentos preferidos
- Erros de validação

### **Relatórios no Admin**
- Lista de todos os cadastros
- Filtros por status e data
- Ações em lote
- Exportação de dados
- Histórico de mudanças

## 🚨 Tratamento de Erros

### **Validações de Frontend**
- Campos obrigatórios
- Formato de dados
- Validação em tempo real
- Mensagens de erro claras

### **Validações de Backend**
- Validação de CPF
- Validação de email
- Validação de endereço
- Verificação de duplicatas

### **Tratamento de Exceções**
- Logs detalhados de erro
- Mensagens amigáveis ao usuário
- Fallbacks para campos opcionais
- Recuperação automática

## 🔄 Manutenção

### **Backup de Dados**
- Todos os cadastros são preservados
- Histórico de mudanças mantido
- Integridade referencial garantida

### **Atualizações**
- Scripts de migração automáticos
- Preservação de configurações
- Compatibilidade com versões anteriores

## 📞 Suporte

### **Canais de Ajuda**
- Telefone: (89) 2221-0068
- WhatsApp: (89) 2221-0068
- Email: contato@megalinkpiaui.com.br

### **Documentação Técnica**
- Código comentado
- Docstrings em português
- Exemplos de uso
- Guias de configuração

## 🎯 Próximos Passos

### **Funcionalidades Planejadas**
- [ ] Integração com WhatsApp Business API
- [ ] Sistema de notificações push
- [ ] Dashboard de analytics
- [ ] Relatórios avançados
- [ ] Integração com CRM
- [ ] Sistema de cupons e promoções

### **Melhorias Técnicas**
- [ ] Cache de configurações
- [ ] Rate limiting avançado
- [ ] Logs estruturados
- [ ] Métricas de performance
- [ ] Testes automatizados
- [ ] CI/CD pipeline

---

## 🚀 **Começando Agora**

1. **Execute o script de dados iniciais**
2. **Configure as opções no admin Django**
3. **Teste a página de cadastro**
4. **Monitore os leads gerados**
5. **Personalize conforme necessário**

---

**Desenvolvido com ❤️ para Megalink Piauí**
