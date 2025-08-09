#!/bin/bash
# A linha abaixo é uma boa prática. Faz o script parar imediatamente se qualquer comando falhar.
set -e

# =================================================================
#  SCRIPT DE INICIALIZAÇÃO ROBUSTO v2 - PROJETO CAIXA DE SUGESTÕES
# =================================================================

# Define cores para facilitar a leitura
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

printf "${YELLOW}--- Iniciando a configuração do ambiente Backend ---${NC}\n"

# --- PASSO 1: Preparação do Ambiente Virtual Python ---
printf "\n▶️  ${CYAN}Passo 1/5: Configurando ambiente virtual Python...${NC}\n"
if [ ! -d ".venv" ]; then
    printf "Ambiente virtual '.venv' não encontrado. Criando...\n"
    python -m venv .venv
else
    printf "Ambiente virtual '.venv' já existe.\n"
fi

# --- PASSO 2: Detecção do SO e Definição do Comando de Ativação ---
printf "\n▶️  ${CYAN}Passo 2/5: Detectando Sistema Operacional para ativação do .venv...${NC}\n"

VENV_ACTIVATE_PATH=""
# Verifica se o caminho de ativação do Windows existe
if [ -f ".venv/Scripts/activate" ]; then
    printf "(Detectado ambiente Windows/Git Bash)\n"
    VENV_ACTIVATE_PATH=".venv/Scripts/activate"
# Senão, verifica se o caminho de ativação do Linux/macOS existe
elif [ -f ".venv/bin/activate" ]; then
    printf "(Detectado ambiente Linux/macOS)\n"
    VENV_ACTIVATE_PATH=".venv/bin/activate"
else
    # Se nenhum for encontrado, falha com uma mensagem clara.
    printf "❌ Erro: Script de ativação do ambiente virtual não encontrado em .venv/Scripts/ ou .venv/bin/\n"
    exit 1
fi
# Armazena o comando completo que o usuário precisará usar depois.
ACTIVATION_COMMAND="source ${VENV_ACTIVATE_PATH}"

# --- PASSO 3: Ativação do Ambiente Virtual (para a execução DESTE script) ---
printf "\n▶️  ${CYAN}Passo 3/5: Ativando ambiente virtual para este script...${NC}\n"
source "${VENV_ACTIVATE_PATH}"
printf "Ambiente virtual ativado nesta sessão.\n"

# --- PASSO 4: Instalação das Dependências ---
printf "\n▶️  ${CYAN}Passo 4/5: Instalando dependências...${NC}\n"
pip install -r requirements.txt
printf "Dependências instaladas com sucesso.\n"

# --- PASSO 5: Inicialização da Infraestrutura Docker e Banco ---
printf "\n▶️  ${CYAN}Passo 5/5: Iniciando contêineres e configurando o banco...${NC}\n"
docker-compose up -d
printf "Aguardando o banco de dados ficar pronto...\n"
sleep 10
docker-compose exec -T postgres psql -U dev -d sugestoes_db <<EOF
CREATE TABLE IF NOT EXISTS sugestoes (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(255),
    sugestao TEXT NOT NULL,
    data_recebimento TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
EOF
printf "Tabela 'sugestoes' verificada/criada.\n"

# --- Conclusão e Instruções Finais ---
printf "\n${GREEN}✅ AMBIENTE PRONTO! Infraestrutura no ar.${NC}\n"
printf "${YELLOW}------------------- AÇÃO NECESSÁRIA -------------------${NC}\n"
printf "Para iniciar a aplicação, abra ${GREEN}DOIS NOVOS TERMINAIS${NC}.\n"
printf "Em ${GREEN}CADA UM DELES${NC}, execute os seguintes comandos:\n\n"

printf "➡️  ${CYAN}NO TERMINAL 1 (para a API - Produtor):${NC}\n"
printf "   1. Ative o ambiente virtual:\n"
printf "      ${GREEN}${ACTIVATION_COMMAND}${NC}\n"
printf "   2. Inicie a API Flask:\n"
printf "      ${GREEN}python run_api.py${NC}\n\n"

printf "➡️  ${CYAN}NO TERMINAL 2 (para o Consumidor):${NC}\n"
printf "   1. Ative o ambiente virtual:\n"
printf "      ${GREEN}${ACTIVATION_COMMAND}${NC}\n"
printf "   2. Inicie o Consumidor Kafka:\n"
printf "      ${GREEN}python run_consumer.py${NC}\n"
printf "${YELLOW}-----------------------------------------------------------${NC}\n"