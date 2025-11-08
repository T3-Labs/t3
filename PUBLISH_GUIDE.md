# 🚀 Guia de Publicação no PyPI

## Problema Identificado

O workflow estava configurado com **Trusted Publishing** (usando `permissions: id-token: write`), mas tentando usar API Token ao mesmo tempo. Isso causa conflito.

**Correção aplicada**: Removida a linha `permissions: id-token: write` para usar apenas API Token.

---

## ✅ Checklist de Configuração

### 1. Configurar API Token no PyPI

#### a) Criar conta no PyPI
- Acesse: https://pypi.org/account/register/
- Confirme seu e-mail

#### b) Criar API Token
1. Acesse: https://pypi.org/manage/account/token/
2. Clique em "Add API token"
3. **Nome**: `t3-cli-github-actions`
4. **Scope**: 
   - Primeira publicação: "Entire account (all projects)"
   - Depois da primeira publicação: "Project: t3-cli"
5. Copie o token (começa com `pypi-...`)

#### c) Adicionar Secret no GitHub
1. Vá em: https://github.com/T3-Labs/t3/settings/secrets/actions
2. Clique em "New repository secret"
3. **Name**: `PYPI_API_TOKEN`
4. **Value**: Cole o token do PyPI (com `pypi-` incluído)
5. Clique em "Add secret"

### 2. (Opcional) Configurar Test PyPI

Para testar antes de publicar no PyPI real:

#### a) Criar conta no Test PyPI
- Acesse: https://test.pypi.org/account/register/

#### b) Criar API Token no Test PyPI
- Acesse: https://test.pypi.org/manage/account/token/
- Crie um token com scope "Entire account"

#### c) Adicionar Secret no GitHub
- **Name**: `TEST_PYPI_API_TOKEN`
- **Value**: Token do Test PyPI

---

## 🎯 Como Publicar

### Opção 1: Usando o Script de Release (Recomendado)

```bash
# 1. Certifique-se de estar na branch main
git checkout main
git pull origin main

# 2. Execute o script de release
./scripts/release.sh 0.1.0

# 3. Vá para GitHub e crie a release
# https://github.com/T3-Labs/t3/releases/new
```

### Opção 2: Manual

```bash
# 1. Atualize a versão no pyproject.toml
# version = "0.1.0"

# 2. Commit e push
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push origin main

# 3. Crie a tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# 4. Crie a release no GitHub
# https://github.com/T3-Labs/t3/releases/new
# - Selecione a tag: v0.1.0
# - Título: v0.1.0 - Initial Release
# - Descrição: Veja exemplo abaixo
```

---

## 📝 Template de Release Notes

```markdown
# T3 CLI v0.1.0 - Initial Release

## 🎉 Primeira versão pública do T3 CLI!

### ✨ Features

- 🚀 CLI completa com Typer e Rich
- 🐳 Integração Docker com Edge Video
- 📦 Templates de projeto (basic, python, web)
- ⚙️ Sistema de configuração robusto
- ✅ 13 testes unitários (100% passing)
- 📚 Documentação completa

### 📦 Instalação

```bash
pip install t3-cli
```

### 🔧 Comandos Disponíveis

- `t3 hello` - Mensagem de boas-vindas
- `t3 status` - Status do sistema
- `t3 init project` - Inicializar projetos
- `t3 init docker` - Setup Docker Edge Video
- `t3 config` - Gerenciar configurações

### 📖 Documentação

- [README](https://github.com/T3-Labs/t3/blob/main/README.md)
- [Contributing Guide](https://github.com/T3-Labs/t3/blob/main/CONTRIBUTING.md)
- [Release Process](https://github.com/T3-Labs/t3/blob/main/RELEASE.md)

### 🙏 Agradecimentos

Obrigado a todos que contribuíram para esta primeira versão!
```

---

## 🔍 Verificar Publicação

### 1. Monitorar o Workflow

Após criar a release no GitHub:

1. Vá para: https://github.com/T3-Labs/t3/actions
2. Procure pelo workflow "CI/CD Pipeline"
3. Clique no workflow disparado pela release
4. Verifique se todos os jobs passaram:
   - ✅ Test
   - ✅ Build
   - ✅ Publish to PyPI

### 2. Verificar no PyPI

Depois que o workflow terminar:

1. Acesse: https://pypi.org/project/t3-cli/
2. Verifique se a versão 0.1.0 aparece
3. Teste a instalação:

```bash
# Em um novo ambiente
python -m venv test-env
source test-env/bin/activate
pip install t3-cli
t3 --version
t3 --help
```

---

## 🐛 Troubleshooting

### Erro: "Invalid or non-existent authentication information"

**Causa**: Token do PyPI não configurado ou inválido

**Solução**:
1. Verifique se o secret `PYPI_API_TOKEN` existe em: https://github.com/T3-Labs/t3/settings/secrets/actions
2. Certifique-se de que copiou o token completo (incluindo `pypi-`)
3. O token não pode ter espaços ou quebras de linha

### Erro: "Project name already exists"

**Causa**: Nome `t3-cli` já existe no PyPI (outro projeto)

**Solução**:
1. Mude o nome em `pyproject.toml`:
   ```toml
   name = "t3-labs-cli"  # ou outro nome único
   ```
2. Faça commit e push
3. Tente publicar novamente

### Workflow não dispara

**Causa**: Precisa ser um evento de "Release" no GitHub, não apenas uma tag

**Solução**:
1. Tags sozinhas não disparam o workflow
2. Você **precisa criar uma Release** no GitHub:
   - https://github.com/T3-Labs/t3/releases/new
   - Selecione a tag
   - Clique em "Publish release"

### Job "publish-pypi" não aparece

**Causa**: Condição `if: github.event_name == 'release'` não satisfeita

**Solução**:
1. Certifique-se de criar uma **Release** (não apenas uma tag)
2. A release precisa ser do tipo "published" (não "draft")

---

## 🧪 Testar Antes de Publicar no PyPI Real

Para testar o processo sem publicar no PyPI oficial:

```bash
# 1. Push para branch develop (dispara Test PyPI)
git checkout develop
git push origin develop

# 2. Monitore o workflow
# O job "publish-test-pypi" será executado

# 3. Verifique em Test PyPI
# https://test.pypi.org/project/t3-cli/

# 4. Teste a instalação do Test PyPI
pip install -i https://test.pypi.org/simple/ t3-cli
```

---

## 📊 Status Atual

- ✅ Workflow corrigido (removido conflito de Trusted Publishing)
- ✅ Secret name correto: `PYPI_API_TOKEN`
- ⏳ Aguardando: Configuração do token no GitHub
- ⏳ Aguardando: Criação da primeira release

---

## 🔗 Links Úteis

- **PyPI**: https://pypi.org
- **Test PyPI**: https://test.pypi.org
- **GitHub Actions**: https://github.com/T3-Labs/t3/actions
- **GitHub Releases**: https://github.com/T3-Labs/t3/releases
- **GitHub Secrets**: https://github.com/T3-Labs/t3/settings/secrets/actions

---

## 📞 Próximos Passos

1. ✅ Corrigir workflow (CONCLUÍDO)
2. ⏳ Criar API Token no PyPI
3. ⏳ Adicionar secret `PYPI_API_TOKEN` no GitHub
4. ⏳ Fazer commit do workflow corrigido
5. ⏳ Criar release v0.1.0 no GitHub
6. ⏳ Monitorar o workflow
7. ⏳ Verificar publicação no PyPI
8. ⏳ Testar instalação com `pip install t3-cli`

---

**Data**: 2025-11-08
**Versão do Guia**: 1.0
