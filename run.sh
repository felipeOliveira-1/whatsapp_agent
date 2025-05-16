#!/bin/bash

# Script para iniciar o servidor de desenvolvimento

# Ativa o ambiente virtual
if [ -d "venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate  # No Windows, use: .\venv\Scripts\activate
else
    echo "❌ Ambiente virtual não encontrado. Execute setup.sh primeiro."
    exit 1
fi

# Define variáveis de ambiente
if [ -f ".env" ]; then
    echo "📄 Carregando variáveis de ambiente do arquivo .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️  AVISO: Arquivo .env não encontrado. Certifique-se de configurar as variáveis de ambiente necessárias."
fi

# Inicia o servidor com Gunicorn
echo "🚀 Iniciando o servidor Gunicorn..."
echo "📡 Acesse: http://localhost:${PORT:-5000}"

exec gunicorn app:app -c gunicorn_config.py
