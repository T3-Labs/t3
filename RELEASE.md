# Guia de Release - T3 CLI

Este documento descreve o processo completo para criar e publicar uma nova versão do T3 CLI.

## Pré-requisitos

1. **Permissões necessárias**:
   - Acesso de escrita ao repositório GitHub
   - Conta no PyPI (https://pypi.org)
   - Token de API do PyPI configurado nos secrets do GitHub

2. **Configuração local**:
   ```bash
   # Clone e configure o projeto
   git clone https://github.com/T3-Labs/t3.git
   cd t3
   uv sync
   source .venv/bin/activate
   ```

## Processo de Release

### 1. Preparação

#### 1.1 Criar branch de release (opcional)
```bash
git checkout main
git pull origin main
git checkout -b release/v0.2.0
```

#### 1.2 Atualizar versão
Edite `pyproject.toml`:
```toml
[project]
name = "t3-cli"
version = "0.2.0"  # ← Atualize aqui
```

#### 1.3 Atualizar CHANGELOG
Edite a seção `Changelog` no `README.md`:
```markdown
## Changelog

### v0.2.0 (2025-11-XX)
- ✨ Nova funcionalidade X
- 🐛 Correção do bug Y
- 📝 Documentação melhorada
- ⚡ Performance otimizada

### v0.1.0 (2025-11-08)
...
```

#### 1.4 Executar testes localmente
```bash
# Testes
make test

# Linting
make lint

# Build local
python -m build
twine check dist/*
```

### 2. Commit e Push

```bash
git add pyproject.toml README.md
git commit -m "chore: release v0.2.0"
git push origin release/v0.2.0
```

### 3. Criar Pull Request

1. Abra PR: `release/v0.2.0` → `main`
2. Aguarde CI/CD passar (✅ todos os checks)
3. Solicite review (se necessário)
4. Merge para `main`

### 4. Criar Tag e Release

#### 4.1 Criar tag localmente
```bash
git checkout main
git pull origin main
git tag -a v0.2.0 -m "Release v0.2.0 - Descrição breve"
git push origin v0.2.0
```

#### 4.2 Criar Release no GitHub

**Via Interface Web:**
1. Acesse: https://github.com/T3-Labs/t3/releases/new
2. Preencha:
   - **Tag**: `v0.2.0` (selecione a tag criada)
   - **Release title**: `v0.2.0 - Nome da Release`
   - **Description**:
     ```markdown
     ## 🎉 What's New in v0.2.0
     
     ### ✨ Features
     - Nova funcionalidade X
     - Suporte para Y
     
     ### 🐛 Bug Fixes
     - Correção do problema Z
     
     ### 📝 Documentation
     - Documentação melhorada
     
     ### 🔧 Internal
     - Refatoração de código
     
     ## 📦 Installation
     
     ```bash
     pip install --upgrade t3-cli
     ```
     
     ## 🔗 Links
     - [PyPI Package](https://pypi.org/project/t3labs-cli/)
     - [Documentation](https://github.com/T3-Labs/t3#readme)
     - [Full Changelog](https://github.com/T3-Labs/t3/compare/v0.1.0...v0.2.0)
     ```
3. **Marque como pre-release** (se aplicável)
4. Clique em **"Publish release"**

**Via GitHub CLI:**
```bash
gh release create v0.2.0 \
  --title "v0.2.0 - Nome da Release" \
  --notes-file release-notes.md
```

### 5. Publicação Automática

Ao publicar a release, o GitHub Actions automaticamente:

1. ✅ **Executa testes** em Python 3.11 e 3.12
2. 🔍 **Verifica linting** com Ruff
3. 📦 **Constrói o pacote** (wheel e source distribution)
4. ✅ **Valida o pacote** com twine
5. 🚀 **Publica no PyPI** usando `PYPI_API_TOKEN`

Acompanhe em: https://github.com/T3-Labs/t3/actions

### 6. Verificação Pós-Release

#### 6.1 Verificar publicação no PyPI
```bash
# Aguarde alguns minutos, então:
pip install --upgrade t3-cli
t3 --version  # Deve mostrar v0.2.0
```

#### 6.2 Testar instalação limpa
```bash
# Em um ambiente novo
python -m venv test-env
source test-env/bin/activate
pip install t3labs-cli
t3 --help
t3 init docker --help
```

#### 6.3 Atualizar documentação
- Verificar se README.md está atualizado no PyPI
- Atualizar Wiki se houver
- Anunciar release (Twitter, Blog, etc.)

## Configuração dos Secrets

### PyPI API Token

1. **Criar Token no PyPI**:
   - Acesse: https://pypi.org/manage/account/token/
   - Clique em "Add API token"
   - Nome: `t3-cli-github-actions`
   - Scope: "Entire account" ou "Project: t3-cli"
   - Copie o token (começa com `pypi-...`)

2. **Adicionar ao GitHub**:
   - Acesse: https://github.com/T3-Labs/t3/settings/secrets/actions
   - Clique em "New repository secret"
   - Nome: `PYPI_API_TOKEN`
   - Valor: Cole o token copiado
   - Clique em "Add secret"

### Test PyPI Token (Opcional)

1. **Criar Token no Test PyPI**:
   - Acesse: https://test.pypi.org/manage/account/token/
   - Mesmo processo do PyPI

2. **Adicionar ao GitHub**:
   - Nome: `TEST_PYPI_API_TOKEN`
   - Valor: Token do Test PyPI

## Estratégias de Versionamento

### Semantic Versioning (MAJOR.MINOR.PATCH)

- **MAJOR (X.0.0)**: Mudanças incompatíveis (breaking changes)
  - Exemplo: Remover comando, mudar interface de API
  
- **MINOR (0.X.0)**: Nova funcionalidade compatível
  - Exemplo: Novo comando `t3 deploy`, nova opção `--verbose`
  
- **PATCH (0.0.X)**: Correções de bugs compatíveis
  - Exemplo: Corrigir erro em parsing, melhorar mensagem

### Exemplos de Incremento

```
0.1.0 → 0.1.1  # Bug fix
0.1.1 → 0.2.0  # Nova funcionalidade
0.2.0 → 1.0.0  # API estável, breaking change
1.0.0 → 1.1.0  # Nova funcionalidade (compatível)
1.1.0 → 1.1.1  # Bug fix
```

## Troubleshooting

### Erro: "File already exists"
```bash
# O PyPI não permite substituir versões
# Solução: Incrementar versão e fazer nova release
```

### Erro: "Invalid authentication"
```bash
# Verificar se PYPI_API_TOKEN está configurado corretamente
# Regenerar token se necessário
```

### CI/CD falha no teste
```bash
# Verificar logs em: https://github.com/T3-Labs/t3/actions
# Corrigir problemas e fazer novo commit
# Não é necessário deletar a tag, apenas criar nova
```

### Reverter release
```bash
# 1. Deletar release no GitHub
gh release delete v0.2.0

# 2. Deletar tag
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0

# 3. Revertir commits se necessário
git revert <commit-hash>

# Nota: Não é possível deletar versão do PyPI
# Apenas marcar como "yanked" em casos extremos
```

## Checklist de Release

Use este checklist antes de cada release:

- [ ] Código revisado e testado
- [ ] Todos os testes passando localmente
- [ ] Versão atualizada em `pyproject.toml`
- [ ] CHANGELOG atualizado em `README.md`
- [ ] Documentação atualizada
- [ ] Secrets configurados no GitHub
- [ ] Branch principal (main) atualizado
- [ ] Tag criada e pushed
- [ ] Release criada no GitHub
- [ ] CI/CD executado com sucesso
- [ ] Pacote disponível no PyPI
- [ ] Instalação testada em ambiente limpo
- [ ] Anúncio da release feito

## Recursos Adicionais

- [Semantic Versioning](https://semver.org/)
- [PyPI Help](https://pypi.org/help/)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Python Packaging Guide](https://packaging.python.org/)
