#!/usr/bin/env bash
# Script para configurar o token do PyPI no GitHub Secrets

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo ""
echo "═══════════════════════════════════════════════"
echo "  🔐 Configuração de Secrets do GitHub"
echo "═══════════════════════════════════════════════"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) não está instalado"
    echo ""
    print_info "Instale com:"
    echo "  Ubuntu/Debian: sudo apt install gh"
    echo "  macOS: brew install gh"
    echo "  Arch: sudo pacman -S github-cli"
    echo ""
    print_info "Ou configure manualmente em:"
    echo "  https://github.com/T3-Labs/t3/settings/secrets/actions"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    print_warning "Você não está autenticado no GitHub CLI"
    echo ""
    print_info "Execute: gh auth login"
    exit 1
fi

print_success "GitHub CLI autenticado"
echo ""

# Get PyPI token
print_info "Cole o token do PyPI abaixo (começa com 'pypi-')"
echo ""
echo -n "Token do PyPI: "
read -s PYPI_TOKEN
echo ""
echo ""

# Validate token format
if [[ ! $PYPI_TOKEN =~ ^pypi- ]]; then
    print_error "Token inválido! Deve começar com 'pypi-'"
    exit 1
fi

# Add secret to GitHub
print_info "Adicionando secret PYPI_API_TOKEN ao repositório..."

if echo "$PYPI_TOKEN" | gh secret set PYPI_API_TOKEN; then
    print_success "Token PYPI_API_TOKEN configurado com sucesso!"
else
    print_error "Falha ao adicionar secret"
    exit 1
fi

echo ""
print_info "Deseja configurar o Test PyPI também? (y/N)"
read -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    print_info "Cole o token do Test PyPI (https://test.pypi.org)"
    echo -n "Token do Test PyPI: "
    read -s TEST_PYPI_TOKEN
    echo ""
    echo ""
    
    if [[ ! $TEST_PYPI_TOKEN =~ ^pypi- ]]; then
        print_warning "Token inválido! Pulando Test PyPI..."
    else
        print_info "Adicionando secret TEST_PYPI_API_TOKEN..."
        if echo "$TEST_PYPI_TOKEN" | gh secret set TEST_PYPI_API_TOKEN; then
            print_success "Token TEST_PYPI_API_TOKEN configurado!"
        else
            print_warning "Falha ao adicionar Test PyPI token"
        fi
    fi
fi

echo ""
echo "═══════════════════════════════════════════════"
print_success "Configuração concluída!"
echo "═══════════════════════════════════════════════"
echo ""
print_info "Próximos passos:"
echo "1. Faça merge da branch develop para main"
echo "2. Execute: ./scripts/release.sh 0.1.0"
echo "3. Crie a release no GitHub"
echo "4. Monitore em: https://github.com/T3-Labs/t3/actions"
echo ""
print_info "Verificar secrets configurados:"
echo "https://github.com/T3-Labs/t3/settings/secrets/actions"
echo ""
