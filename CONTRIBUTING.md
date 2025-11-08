# Contributing to T3 CLI

Obrigado por considerar contribuir para o T3 CLI! 🎉

## Código de Conduta

- Seja respeitoso e profissional
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## Como Contribuir

### Reportando Bugs

Antes de criar um issue de bug:
1. Verifique se o bug já foi reportado
2. Use a versão mais recente do T3 CLI
3. Inclua o máximo de detalhes possível

**Modelo de Issue de Bug:**
```
**Descrição do Bug**
Descrição clara e concisa do bug.

**Para Reproduzir**
Passos para reproduzir o comportamento:
1. Execute '...'
2. Com parâmetros '....'
3. Observe o erro

**Comportamento Esperado**
Descrição clara do que você esperava que acontecesse.

**Ambiente:**
- OS: [e.g. Linux, macOS, Windows]
- Python Version: [e.g. 3.11]
- T3 CLI Version: [e.g. 0.1.0]

**Logs/Screenshots**
Se aplicável, adicione logs ou screenshots.
```

### Sugerindo Melhorias

**Modelo de Issue de Feature:**
```
**Problema a Resolver**
Descrição clara do problema que a feature resolve.

**Solução Proposta**
Descrição clara da solução proposta.

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Qualquer outro contexto sobre a feature.
```

### Pull Requests

1. **Fork o repositório**
2. **Clone seu fork:**
   ```bash
   git clone https://github.com/seu-usuario/t3.git
   cd t3
   ```

3. **Configure o ambiente de desenvolvimento:**
   ```bash
   ./scripts/dev.sh setup
   ```

4. **Crie uma branch para sua feature:**
   ```bash
   git checkout -b feature/minha-feature
   # ou
   git checkout -b fix/meu-bugfix
   ```

5. **Faça suas alterações:**
   - Siga as guidelines de código (veja abaixo)
   - Adicione testes para novas funcionalidades
   - Atualize a documentação se necessário

6. **Execute as verificações:**
   ```bash
   ./scripts/dev.sh check
   ```

7. **Commit suas mudanças:**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   ```
   
   Use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` Nova funcionalidade
   - `fix:` Correção de bug
   - `docs:` Mudanças na documentação
   - `style:` Formatação, sem mudanças de código
   - `refactor:` Refatoração de código
   - `test:` Adição/correção de testes
   - `chore:` Manutenção, configurações

8. **Push para seu fork:**
   ```bash
   git push origin feature/minha-feature
   ```

9. **Abra um Pull Request** no GitHub

### Guidelines de Código

#### Estilo Python

Seguimos as convenções definidas nos arquivos de instruções:

1. **KISS e Responsabilidade Única**
   - Mantenha funções e classes simples
   - Uma classe/função deve fazer uma coisa só

2. **Nomes Explícitos**
   ```python
   # ❌ Evite
   a = 0
   i = "string"
   
   # ✅ Prefira
   initial_number = 0
   text = "string"
   ```

3. **Type Hints e Docstrings**
   ```python
   def process_data(input_file: str, output_dir: Path) -> List[str]:
       """
       Processa dados do arquivo de entrada.
       
       Args:
           input_file: Caminho do arquivo de entrada
           output_dir: Diretório para salvar resultados
           
       Returns:
           Lista de arquivos processados
       """
       ...
   ```

4. **Organização de Imports**
   ```python
   # 1. Bibliotecas externas
   import boto3
   from typer import Typer
   
   # 2. Bibliotecas built-in
   from typing import List
   import sqlite3
   
   # 3. Importações locais
   from t3.core.config import ConfigManager
   ```

#### Testes

- Escreva testes para toda nova funcionalidade
- Use pytest e fixtures quando apropriado
- Nomeie testes descritivamente: `test_function_name_expected_behavior`
- Organize testes em classes quando fizer sentido

```python
def test_config_manager_set_valid_key():
    """Testa que ConfigManager.set() aceita chave válida."""
    manager = ConfigManager()
    manager.set("app.name", "T3")
    assert manager.get("app.name") == "T3"
```

#### Documentação

- Mantenha o README.md atualizado
- Adicione docstrings a classes e funções públicas
- Atualize CHANGELOG para mudanças significativas
- Inclua exemplos de uso quando apropriado

### Processo de Review

Pull Requests passarão por:

1. **CI/CD Automático:**
   - ✅ Testes em Python 3.11 e 3.12
   - 🔍 Linting com Ruff
   - 📦 Verificação de build

2. **Code Review Manual:**
   - Qualidade do código
   - Testes adequados
   - Documentação atualizada
   - Seguir guidelines do projeto

3. **Feedback e Iteração:**
   - Responda aos comentários
   - Faça ajustes conforme solicitado
   - Mantenha a discussão profissional

### Estrutura do Projeto

```
t3/
├── t3/                  # Código fonte principal
│   ├── commands/        # Comandos CLI
│   ├── core/           # Funcionalidades core
│   └── main.py         # Entry point
├── tests/              # Testes unitários
├── scripts/            # Scripts auxiliares
├── docs/               # Documentação adicional
└── pyproject.toml      # Configuração do projeto
```

### Desenvolvimento Local

```bash
# Setup inicial
./scripts/dev.sh setup

# Durante desenvolvimento
./scripts/dev.sh test        # Rodar testes
./scripts/dev.sh lint        # Verificar linting
./scripts/dev.sh format      # Formatar código

# Antes de commit
./scripts/dev.sh check       # Todas as verificações

# Testar CLI
t3 --help
t3 init --help
```

### Dúvidas?

- Abra uma issue com a tag `question`
- Consulte a documentação em [README.md](README.md)
- Revise issues e PRs existentes

## Reconhecimento

Contribuidores serão listados no README.md e nos release notes.

Obrigado por contribuir! 🚀
