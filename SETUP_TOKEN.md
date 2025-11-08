# 🔐 Configurar Token do PyPI no GitHub

## ⚡ Método Rápido (Manual)

### 1. Acesse a página de Secrets do repositório

🔗 **Link direto**: https://github.com/T3-Labs/t3/settings/secrets/actions

### 2. Adicione o Secret

1. Clique no botão **"New repository secret"**
2. Preencha:
   - **Name**: `PYPI_API_TOKEN`
   - **Value**: Cole seu token do PyPI aqui (começa com `pypi-`)
3. Clique em **"Add secret"**

**⚠️ IMPORTANTE**: O token foi enviado separadamente por segurança. Não coloque tokens em arquivos do repositório!

## ✅ Verificação

Depois de adicionar o secret, você verá:

- ✅ **PYPI_API_TOKEN** - Updated now

## 🚀 Próximos Passos

Após configurar o secret:

```bash
# 1. Commit as mudanças do workflow
git add .github/workflows/ci-cd.yml scripts/setup-secrets.sh
git commit -m "fix: add user field and verbose mode to PyPI publish

- Add user: __token__ to explicitly use API token authentication
- Add verbose: true for better debugging
- Prevents fallback to Trusted Publishing"

git push origin develop

# 2. Merge para main
git checkout main
git merge develop
git push origin main

# 3. Criar release
./scripts/release.sh 0.1.0

# Ou manualmente:
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## 🔍 O que foi corrigido

**Problema anterior:**
```yaml
# ❌ Action tentava usar Trusted Publishing por padrão
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
```

**Solução aplicada:**
```yaml
# ✅ Força uso de API Token explicitamente
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    user: __token__              # <- Adicionado
    password: ${{ secrets.PYPI_API_TOKEN }}
    verbose: true                 # <- Adicionado para debug
```

## 📊 Monitoramento

Após criar a release, monitore em:
- 🔗 **Actions**: https://github.com/T3-Labs/t3/actions
- 🔗 **PyPI**: https://pypi.org/project/t3/

## 🆘 Troubleshooting

### Se ainda falhar com "OIDC token permissions"

Isso indica que o secret não está sendo lido corretamente. Verifique:

1. **Nome exato**: `PYPI_API_TOKEN` (case-sensitive)
2. **Token completo**: Deve começar com `pypi-` e não ter espaços
3. **Ambiente**: Se você criou um "environment" chamado `pypi`, verifique as configurações em:
   - https://github.com/T3-Labs/t3/settings/environments

### Testar com Test PyPI primeiro

Se quiser testar antes:

1. Configure `TEST_PYPI_API_TOKEN` da mesma forma
2. Push para branch `develop`
3. O workflow publicará no Test PyPI automaticamente

---

**Data**: 2025-11-08
**Status**: ✅ Token fornecido e workflow corrigido
