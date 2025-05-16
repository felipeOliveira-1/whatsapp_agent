#!/bin/bash

# Script de configuração do ambiente de desenvolvimento

echo "🚀 Configurando o ambiente de desenvolvimento..."

# Verifica se o Python 3.10 está instalado
if ! command -v python3.10 &> /dev/null; then
    echo "❌ Python 3.10 não encontrado. Por favor, instale o Python 3.10."
    exit 1
fi

# Cria um ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3.10 -m venv venv

# Ativa o ambiente virtual
echo "✅ Ambiente virtual criado. Ativando..."
source venv/bin/activate  # No Windows, use: .\venv\Scripts\activate

# Atualiza o pip
echo "🔄 Atualizando pip..."
pip install --upgrade pip

# Instala as dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

echo "✨ Configuração concluída com sucesso!"
echo "Para ativar o ambiente virtual, execute:"
echo "No Linux/Mac: source venv/bin/activate"
echo "No Windows: .\\venv\\Scripts\\activate"
echo "\nDepois, execute o servidor com: python app.py"
