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
git clone <repository-url>
cd t3

# Instale usando uv (recomendado)
uv sync

# Ou usando pip
pip install -e .
```

### Para Uso

```bash
pip install t3
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

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Changelog

### v0.1.0
- ✨ Versão inicial
- 🚀 CLI básica com Typer e Rich
- 🔧 Sistema de configuração
- 📦 Templates de inicialização de projeto
- ✅ Testes unitários básicos
