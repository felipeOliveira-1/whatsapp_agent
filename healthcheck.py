#!/usr/bin/env python
"""
Script de verificação de saúde para o serviço WhatsApp OpenAI Assistant.
Este script verifica se todos os componentes necessários estão funcionando corretamente.
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def check_env_vars():
    """Verifica se todas as variáveis de ambiente necessárias estão definidas."""
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'OPENAI_API_KEY',
        'OPENAI_ASSISTANT_ID'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        return False
    
    print("✅ Todas as variáveis de ambiente necessárias estão definidas")
    return True

def check_web_server():
    """Verifica se o servidor web está respondendo."""
    try:
        port = os.getenv('PORT', '5000')
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Servidor web respondendo na porta {port}")
            return True
        else:
            print(f"❌ Servidor web retornou código de status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Não foi possível conectar ao servidor web: {e}")
        return False

def check_openai_api():
    """Verifica se a API da OpenAI está acessível."""
    from openai import OpenAI
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        
        if models:
            print("✅ API da OpenAI está acessível")
            return True
        else:
            print("❌ Não foi possível obter a lista de modelos da OpenAI")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar a API da OpenAI: {e}")
        return False

def check_twilio_api():
    """Verifica se a API do Twilio está acessível."""
    from twilio.rest import Client
    
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        client = Client(account_sid, auth_token)
        account = client.api.accounts(account_sid).fetch()
        
        if account.sid:
            print("✅ API do Twilio está acessível")
            return True
        else:
            print("❌ Não foi possível acessar a conta do Twilio")
            return False
    except Exception as e:
        print(f"❌ Erro ao acessar a API do Twilio: {e}")
        return False

def main():
    """Função principal que executa todas as verificações."""
    print("🔍 Iniciando verificação de saúde do sistema...")
    start_time = time.time()
    
    checks = [
        ("Variáveis de ambiente", check_env_vars),
        ("Servidor web", check_web_server),
        ("API da OpenAI", check_openai_api),
        ("API do Twilio", check_twilio_api)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n⏳ Verificando {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro ao executar verificação de {name}: {e}")
            results.append(False)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*50)
    print(f"📊 Resumo da verificação de saúde (duração: {duration:.2f}s):")
    
    all_passed = all(results)
    
    for i, (name, _) in enumerate(checks):
        status = "✅ PASSOU" if results[i] else "❌ FALHOU"
        print(f"{name}: {status}")
    
    print("\n📝 Resultado final:", "✅ SAUDÁVEL" if all_passed else "❌ INSALUBRE")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
