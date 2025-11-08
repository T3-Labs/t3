# T3 CLI

Uma ferramenta CLI poderosa construída com Typer e Rich para interface de linha de comando moderna.

## Características

- 🚀 Interface CLI moderna com suporte a cores e formatação
- 🔧 Sistema de configuração robusto
- 📦 Inicialização de projetos com templates
- 🛠 Comandos extensíveis
- ✅ Testes unitários abrangentes
- 🐍 Suporte completo ao Python 3.11+

## Instalação

### Para Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/T3-Labs/t3.git
cd t3

# Instale dependências usando uv (recomendado)
uv sync

# Instale o CLI em modo desenvolvimento (editable)
uv pip install -e .

# Ative o ambiente virtual
source .venv/bin/activate

# Verifique a instalação
t3 --version
t3 --help
```

**Ou usando pip:**

```bash
# Clone o repositório
git clone https://github.com/T3-Labs/t3.git
cd t3

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instale dependências e CLI
pip install -e .

# Verifique a instalação
t3 --version
```

### Para Uso (Produção)

```bash
# Instalar via pip (quando publicado no PyPI)
pip install t3labs-cli

# Ou instalar diretamente do GitHub
pip install git+https://github.com/T3-Labs/t3.git

# Verificar instalação
t3 --version
```

### Usando sem Instalação

Se você não quiser instalar, pode executar diretamente:

```bash
# Com ambiente virtual ativado
python -m t3.main --help
python -m t3.main status
python -m t3.main init docker
```

## Uso Básico

### Comandos Principais

```bash
# Mostrar ajuda
t3 --help

# Mostrar versão
t3 --version

# Saudação simples
t3 hello --name "Usuário"

# Verificar status do sistema
t3 status
```

### Inicialização de Projetos

```bash
# Inicializar projeto básico
t3 init project --name "meu-projeto"

# Inicializar projeto Python
t3 init project --name "projeto-python" --template python

# Inicializar projeto web
t3 init project --name "projeto-web" --template web

# Forçar substituição de arquivos existentes
t3 init project --name "projeto" --force
```

### Inicialização Docker

```bash
# Inicializar ambiente Docker com T3 Edge Video
t3 init docker

# Especificar arquivo de configuração customizado
t3 init docker --config ./custom-config.yaml

# Forçar download da imagem mesmo se já existir
t3 init docker --force

# O comando irá:
# 1. Fazer docker pull da imagem ghcr.io/t3-labs/edge-video:latest
# 2. Criar arquivo config.yaml com configurações completas
# 3. Criar diretórios necessários (data/, config/, logs/, recordings/)
# 4. Exibir comandos para executar o container
```

### Gerenciamento de Configuração

```bash
# Mostrar todas as configurações
t3 config show

# Definir uma configuração
t3 config set editor "code"
t3 config set theme "dark"

# Obter uma configuração
t3 config get editor

# Deletar uma configuração
t3 config delete theme

# Resetar todas as configurações
t3 config reset
```

## Estrutura do Projeto

```
t3/
├── t3/                      # Pacote principal
│   ├── __init__.py         # Metadados do pacote
│   ├── main.py             # Entry point principal da CLI
│   ├── commands/           # Comandos da CLI
│   │   ├── __init__.py
│   │   ├── init.py         # Comandos de inicialização
│   │   └── config.py       # Comandos de configuração
│   └── core/               # Funcionalidades principais
│       ├── __init__.py
│       ├── config.py       # Gerenciador de configuração
│       └── utils.py        # Utilitários gerais
├── tests/                  # Testes unitários
│   ├── __init__.py
│   └── test_config.py      # Testes para configuração
├── pyproject.toml          # Configuração do projeto
└── README.md              # Este arquivo
```

## Templates de Projeto

### Template Básico
- Estrutura de diretórios simples (src/, docs/, tests/)
- README.md
- .gitignore básico

### Template Python
- Estrutura básica + pyproject.toml
- Configurações do Ruff para linting
- Dependências de desenvolvimento (pytest, ruff)

### Template Web
- Estrutura para projetos web (public/, assets/, src/)
- arquivo HTML básico
- .gitignore para projetos web

## Configuração Docker (config.yaml)

O comando `t3 init docker` cria um arquivo `config.yaml` completo com as seguintes seções:

### Docker Configuration
```yaml
docker:
  image: ghcr.io/t3-labs/edge-video:latest
  container_name: t3-edge-video
  ports:
    web: 8080      # Interface web
    api: 3000      # API REST
    rtmp: 1935     # Streaming RTMP
  volumes:
    - ./data:/app/data
    - ./config:/app/config
    - ./logs:/app/logs
  environment:
    T3_ENV: production
    T3_LOG_LEVEL: INFO
    T3_ENABLE_API: "true"
    T3_ENABLE_WEB: "true"
```

### Video Processing
```yaml
video:
  input:
    source: camera
    resolution: "1920x1080"
    fps: 30
    format: h264
  processing:
    enable_ai: true
    model: "yolo-v8"
    confidence_threshold: 0.5
    batch_size: 4
  output:
    enable_streaming: true
    enable_recording: false
    output_path: "./recordings"
    stream_quality: high
```

### Network & Storage
```yaml
network:
  api_host: "0.0.0.0"
  api_port: 3000
  web_port: 8080
  rtmp_port: 1935
  enable_cors: true

storage:
  data_path: "./data"
  max_storage_gb: 100
  cleanup_older_than_days: 7
```

## Desenvolvimento

### Configuração do Ambiente

```bash
# Clone e configure
git clone <repository-url>
cd t3

# Instale dependências de desenvolvimento
uv sync --group dev

# Instale em modo de desenvolvimento
uv pip install -e .
```

### Executando Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=t3 --cov-report=html

# Executar testes específicos
pytest tests/test_config.py
```

### Linting e Formatação

```bash
# Verificar linting
ruff check .

# Corrigir problemas automaticamente
ruff check . --fix

# Formatação
ruff format .
```

### Estrutura dos Comandos

Para adicionar novos comandos:

1. Crie um novo arquivo em `t3/commands/`
2. Defina um app Typer para o comando
3. Adicione o app ao `main.py`

Exemplo:

```python
# t3/commands/novo_comando.py
import typer

novo_app = typer.Typer(help="Descrição do novo comando")

@novo_app.command()
def acao():
    """Descrição da ação."""
    print("Nova ação executada!")
```

```python
# t3/main.py
from t3.commands.novo_comando import novo_app

# Adicione ao app principal
app.add_typer(novo_app, name="novo")
```

## Configuração

A CLI armazena configurações em `~/.t3/config.json`. As configurações são persistidas automaticamente quando alteradas através dos comandos `config`.

### Localização dos Arquivos

- **Configuração**: `~/.t3/config.json`
- **Cache**: `~/.t3/cache/` (futuro)
- **Logs**: `~/.t3/logs/` (futuro)

## Contribuindo

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Diretrizes de Código

- Siga as convenções do PEP 8
- Use type hints em todas as funções
- Adicione docstrings para todas as funções públicas
- Escreva testes para novas funcionalidades
- Mantenha a cobertura de testes acima de 80%

## Publicação e Release

### Preparando uma Release

1. **Atualize a versão** em `pyproject.toml`:
   ```toml
   version = "0.2.0"  # Siga versionamento semântico
   ```

2. **Atualize o CHANGELOG** no README.md com as mudanças

3. **Commit e push** das mudanças:
   ```bash
   git add .
   git commit -m "chore: bump version to 0.2.0"
   git push origin main
   ```

4. **Crie uma tag de versão**:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

5. **Crie a Release no GitHub**:
   - Vá para https://github.com/T3-Labs/t3/releases/new
   - Selecione a tag criada (v0.2.0)
   - Título: `v0.2.0`
   - Descrição: Liste as mudanças principais
   - Clique em "Publish release"

6. **O CI/CD automaticamente**:
   - ✅ Executará todos os testes
   - ✅ Construirá o pacote
   - ✅ Publicará no PyPI automaticamente

### Configuração dos Secrets do GitHub

Para que o CI/CD funcione, configure os seguintes secrets no GitHub:

1. Acesse: `Settings` → `Secrets and variables` → `Actions`

2. Adicione os secrets:
   - **PYPI_API_TOKEN**: Token da API do PyPI
     - Obtenha em: https://pypi.org/manage/account/token/
     - Permissões: "Upload packages"
   
   - **TEST_PYPI_API_TOKEN** (opcional): Token do Test PyPI
     - Obtenha em: https://test.pypi.org/manage/account/token/
     - Para testar publicações antes do release oficial

### Build Manual

Para testar o build localmente antes da release:

```bash
# Instalar ferramentas de build
pip install build twine

# Limpar builds anteriores
rm -rf dist/ build/ *.egg-info/

# Construir o pacote
python -m build

# Verificar o pacote
twine check dist/*

# Testar instalação local
pip install dist/t3_cli-0.1.0-py3-none-any.whl

# Testar publicação no Test PyPI (opcional)
twine upload --repository testpypi dist/*
```

### Versionamento Semântico

Seguimos o [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Nova funcionalidade compatível
- **PATCH** (0.0.X): Correções de bugs compatíveis

Exemplos:
- `0.1.0` → `0.2.0`: Novo comando adicionado
- `0.2.0` → `0.2.1`: Correção de bug
- `0.2.1` → `1.0.0`: API estável, mudanças breaking

## Development Scripts

Para facilitar o desenvolvimento, foram criados scripts auxiliares na pasta `scripts/`:

### Dev Helper (`scripts/dev.sh`)

Script para tarefas comuns de desenvolvimento:

```bash
# Configuração inicial
./scripts/dev.sh setup

# Executar testes
./scripts/dev.sh test

# Executar testes com cobertura
./scripts/dev.sh coverage

# Executar linter
./scripts/dev.sh lint

# Formatar código
./scripts/dev.sh format

# Executar todas as verificações (format + lint + test)
./scripts/dev.sh check

# Instalar CLI em modo editável
./scripts/dev.sh install

# Build do pacote
./scripts/dev.sh build

# Limpar artefatos de build
./scripts/dev.sh clean
```

### Release Helper (`scripts/release.sh`)

Script automatizado para criar releases:

```bash
# Criar release (ex: 0.2.0)
./scripts/release.sh 0.2.0
```

Este script irá:
1. ✅ Validar o formato da versão (semantic versioning)
2. 📝 Atualizar `pyproject.toml` com nova versão
3. 💾 Criar commit de bump de versão
4. 🏷️ Criar tag versionada
5. ⬆️ Push para o GitHub
6. 📋 Exibir próximos passos para criar a release

## CI/CD Pipeline

O projeto possui workflows automatizados do GitHub Actions:

### 🔄 CI/CD Principal (`ci-cd.yml`)
- **Trigger**: Push em main/develop, Pull Requests, Releases
- **Jobs**:
  - ✅ Testes em Python 3.11 e 3.12
  - 🔍 Linting com Ruff
  - 📦 Build do pacote
  - 🚀 Publicação automática no PyPI (em releases)
  - 🧪 Publicação no Test PyPI (branch develop)

### 🔍 Validação de PR (`pr-validation.yml`)
- **Trigger**: Pull Requests
- **Jobs**:
  - ✅ Formatação de código
  - 🔍 Linting
  - 🧪 Testes com cobertura
  - 📦 Verificação de build

## Contributing

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines detalhadas.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Changelog

### v0.1.0 (2025-11-08)
- ✨ Versão inicial
- 🚀 CLI básica com Typer e Rich
- 🔧 Sistema de configuração robusto
- 📦 Templates de inicialização de projeto (Python, Web, Basic)
- 🐳 Comando `t3 init docker` para setup do Edge Video
- ✅ Testes unitários com pytest
- 🎨 Linting e formatação com Ruff
- 🔄 CI/CD completo com GitHub Actions
- 📚 Documentação completa
