# 🗃️ Comandos para Gerenciar o Banco de Dados

Este documento explica como usar os comandos personalizados para gerenciar os dados do seu sistema de vendas.

## 🧹 Comando para Zerar o Banco

### `zerar_banco` - Comando Simples e Rápido

Remove todos os dados das tabelas principais, mantendo a estrutura do banco intacta.

```bash
# Zerar o banco (requer confirmação)
python manage.py zerar_banco --confirm

# Zerar com backup automático
python manage.py zerar_banco --confirm --backup
```

**O que faz:**
- ✅ Remove todos os leads, prospectos, históricos e configurações
- ✅ Mantém a estrutura das tabelas
- ✅ Backup opcional em formato JSON
- ✅ Relatório detalhado do que foi removido

## 📊 Comando para Gerar Dados Fictícios

### `gerar_dados_ficticios` - Popula o Banco com Dados de Teste

```bash
# Gerar dados padrão (100 leads, 60 prospectos, 200 contatos)
python manage.py gerar_dados_ficticios

# Gerar quantidades personalizadas
python manage.py gerar_dados_ficticios --leads 50 --prospectos 30 --contatos 100

# Limpar tudo e gerar novos dados
python manage.py gerar_dados_ficticios --clear --leads 200

# Com todas as opções
python manage.py gerar_dados_ficticios --clear --leads 150 --prospectos 80 --contatos 250
```

## 🔄 Fluxo Recomendado

### Para Reiniciar o Sistema Completamente:

```bash
# 1. Zerar o banco com backup
python manage.py zerar_banco --confirm --backup

# 2. Gerar novos dados de teste
python manage.py gerar_dados_ficticios --leads 100 --prospectos 50 --contatos 200
```

### Para Desenvolvimento/Testes:

```bash
# Resetar rápido sem backup
python manage.py zerar_banco --confirm

# Gerar dados específicos para teste
python manage.py gerar_dados_ficticios --leads 10 --prospectos 5 --contatos 20
```

## 📦 Backups

Os backups são salvos na pasta `backups/` com o formato:
```
backup_banco_YYYYMMDD_HHMMSS.json
```

### Exemplo de estrutura do backup:
```json
{
  "timestamp": "2025-01-08T10:30:45",
  "leads": [...],
  "prospectos": [...],
  "historico_contatos": [...],
  "configuracoes": [...],
  "logs": [...]
}
```

## ⚠️ Importantes

1. **SEMPRE confirme** antes de zerar com `--confirm`
2. **Use backup** em produção com `--backup`
3. **Teste primeiro** em ambiente de desenvolvimento
4. **Os comandos são irreversíveis** sem backup

## 🚀 Casos de Uso

### Demonstrações
```bash
python manage.py zerar_banco --confirm
python manage.py gerar_dados_ficticios --leads 200 --prospectos 100 --contatos 500
```

### Reset para Desenvolvimento
```bash
python manage.py zerar_banco --confirm
python manage.py gerar_dados_ficticios --leads 20 --prospectos 10 --contatos 50
```

### Backup Antes de Mudanças
```bash
python manage.py zerar_banco --confirm --backup
```

## 💡 Dicas

- Use `--help` em qualquer comando para ver todas as opções
- Os dados gerados são realistas e seguem padrões brasileiros
- Leadse prospectos têm relacionamento automático com histórico de contatos
- Scores e valores são gerados de forma inteligente

## 🔧 Troubleshooting

Se encontrar erros:

1. **Verifique permissões** da pasta `backups/`
2. **Confirme que está no diretório correto** (`gerenciador_vendas/`)
3. **Use o ambiente virtual** ativado
4. **Verifique se o banco está acessível**

Para mais ajuda, execute:
```bash
python manage.py help zerar_banco
python manage.py help gerar_dados_ficticios
```
