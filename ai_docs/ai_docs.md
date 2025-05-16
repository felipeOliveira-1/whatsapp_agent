# AI_Docs.md

## 🧠 Visão Geral do Projeto

Este projeto tem como objetivo criar um **Assistant da OpenAI operando dentro do WhatsApp**, com uma conexão direta via API ao WhatsApp provida pelo **Twilio**. A integração é realizada através de código Python, sem a necessidade de uma ferramenta de orquestração externa.

> **NOTA IMPORTANTE**: Este projeto utiliza a **API v2 de Assistants** da OpenAI, que substituiu a versão anterior. A documentação abaixo reflete esta versão atualizada da API.

## 🌐 Integrações Externas

### **Twilio API for WhatsApp**
- **Função**: Permite enviar e receber mensagens do WhatsApp via API.
- **Implementação**: 
  - Requer conta Twilio e configuração de um número de telefone para WhatsApp Business.
  - Utiliza autenticação via Account SID e Auth Token da Twilio.
  - A URL base para API é `https://api.twilio.com`.
  - Exemplo de envio de mensagem:
    ```python
    from twilio.rest import Client

    account_sid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = '[AuthToken]'  # Substituir pelo seu Auth Token real
    client = Client(account_sid, auth_token)

    # Envio de mensagem simples
    message = client.messages.create(
      from_='whatsapp:+14155238886',
      body='Sua mensagem aqui',
      to='whatsapp:+1234567890'
    )
    
    # Ou envio usando template
    message = client.messages.create(
      from_='whatsapp:+14155238886',
      content_sid='HXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  # ID do template
      content_variables='{"1":"12/1","2":"3pm"}',  # Variáveis do template
      to='whatsapp:+1234567890'
    )
    ```
  - Suporta envio de mídia (imagens, áudio, documentos) além de texto.
  - Requisitos de formato: Mensagens em texto puro ou formatação específica do WhatsApp, ou uso de templates pré-aprovados.

### **OpenAI API (Assistants v2)**
- **Função**: Processamento e geração de respostas usando Large Language Models.
- **Implementação**:
  - Utiliza o novo modelo **GPT-4o** para melhor desempenho com custo-benefício otimizado.
  - Forma de implementação: **Assistants API v2** da OpenAI.
  - **Importante**: É necessário adicionar o cabeçalho `OpenAI-Beta: assistants=v2` para usar a v2 da API.
  - Fluxo básico de integração:
    1. Criar um Assistant com instruções específicas
    2. Criar um Thread para cada conversa do WhatsApp
    3. Adicionar mensagens ao Thread
    4. Executar o Assistant no Thread
    5. Recuperar a resposta
  - Exemplo básico de código com a API v2:
    ```python
    from openai import OpenAI
    import os
    
    # Inicializar cliente com suporte à API v2
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        default_headers={"OpenAI-Beta": "assistants=v2"}
    )
    
    # Criar um assistant (uma vez)
    assistant = client.beta.assistants.create(
        name="WhatsApp Assistant",
        instructions="Você é um assistente no WhatsApp. Responda de forma concisa e útil.",
        model="gpt-4o"
    )
    
    # Para cada conversa
    thread = client.beta.threads.create()
    
    # Adicionar mensagem do usuário
    client.beta.threads.messages.create(
        thread_id=thread.id, 
        role="user", 
        content="Olá, como você pode me ajudar?"
    )
    
    # Executar o assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    # Aguardar e verificar status do run
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break
        time.sleep(1)
    
    # Recuperar resposta após completar
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    ```
  - Capacidade de manter contexto entre mensagens usando o sistema de Threads.

### **Integração Direta via Python**
- **Função**: Script Python para conexão direta entre Twilio e OpenAI.
- **Implementação**:
  - **Recepção de Mensagens**: Utilização de um servidor web (Flask) para receber webhooks do Twilio.
  - **Exposição do webhook**: Uso do Ngrok para criar um túnel para o servidor local durante o desenvolvimento.
  - **Fluxo de trabalho implementado**:
    1. **Recepção**: Endpoint HTTP recebe mensagens do Twilio via POST.
    2. **Processamento**: Código Python extrai conteúdo e identifica o remetente da mensagem.
    3. **Contexto**: Armazenamento de threads por número de telefone em um dicionário (em produção, seria um banco de dados).
    4. **Integração OpenAI**: Chamada à API de Assistants v2 da OpenAI.
    5. **Resposta**: Envio da resposta de volta para o WhatsApp via Twilio.
  - **Segurança**: Variáveis de ambiente para armazenar tokens de autenticação.
  - **Exemplo de configuração do webhook com integração completa**:
    ```python
    from flask import Flask, request, Response
    from twilio.twiml.messaging_response import MessagingResponse
    from openai import OpenAI
    import time
    import os
    
    app = Flask(__name__)
    
    # Inicializar cliente OpenAI com a versão v2
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        default_headers={"OpenAI-Beta": "assistants=v2"}
    )
    
    # Dicionário para armazenar threads por número de telefone
    user_threads = {}
    
    @app.route('/webhook', methods=['POST'])
    def webhook():
        incoming_msg = request.values.get('Body', '')
        sender = request.values.get('From')
        print(f"Mensagem recebida de {sender}: {incoming_msg}")
        
        # Obter ou criar um thread para este usuário
        thread_id = get_or_create_thread(sender)
        
        # Adicionar mensagem ao thread
        add_message_to_thread(thread_id, incoming_msg)
        
        # Executar o assistant e obter resposta
        run_id = run_assistant(thread_id)
        response_text = get_assistant_response(thread_id, run_id)
        
        # Enviar resposta
        resp = MessagingResponse()
        resp.message(response_text)
        return Response(str(resp), mimetype="application/xml")
    ```

## 🧩 Padrões e Convenções

- Uso de **webhooks do Twilio** para entrada de mensagens no servidor Python.
- Código Python organizado em funções específicas para cada operação:
  - `get_or_create_thread`: Gerencia threads por usuário
  - `add_message_to_thread`: Adiciona mensagens ao thread da OpenAI
  - `run_assistant`: Executa o Assistant no thread
  - `get_assistant_response`: Processa e obtém a resposta
- Estrutura de ambiente usando Flask para o servidor web.
- Comunicação com o Twilio usando TwiML para respostas formalmente estruturadas.
- API v2 de Assistants para maior eficiência e funcionalidades atualizadas.
- Separação clara entre recepção de mensagens, processamento e envio de resposta.

## 📚 Glossário

- **Twilio**: Plataforma de comunicação para envio de mensagens via API.
- **Webhook**: Endpoint HTTP para receber eventos externos do Twilio.
- **Assistant v2 da OpenAI**: API atualizada que utiliza GPT-4o da OpenAI para gerar respostas contextualizadas.
- **Thread**: Conceito da OpenAI para manter contexto de conversas entre mensagens.
- **Run**: Execução de um Assistant em um Thread específico para processar e responder a mensagens.
- **Flask**: Framework Python para criar aplicações web e APIs.
- **Ngrok**: Ferramenta para expor servidores locais à internet, útil para desenvolvimento.
- **TwiML**: Linguagem de markup do Twilio para formatar respostas de SMS e mensagens.

## ⚙️ Notas de Implementação

- **Uso da API v2 de Assistants**: É obrigatório adicionar o cabeçalho `OpenAI-Beta: assistants=v2` para utilizar a versão atual da API.
- **Armazenamento de contexto**: O código atual usa um dicionário em memória para testes. Em produção, use um banco de dados ou Redis para persistência.
- **Variáveis de ambiente**: As credenciais estão configuradas no arquivo `.env` com as seguintes variáveis:
  ```
  TWILIO_ACCOUNT_SID=seu_sid_aqui
  TWILIO_AUTH_TOKEN=seu_token_aqui
  OPENAI_API_KEY=sua_chave_api_aqui
  OPENAI_ASSISTANT_ID=id_do_seu_assistant
  PORT=5000
  DEBUG=True
  ```
- **Ngrok para desenvolvimento**: Para expor o servidor local para os webhooks do Twilio durante o desenvolvimento, usamos Ngrok: `ngrok http 5000`
- **Configuração do Webhook no Twilio**: Configure a URL do webhook no formato `https://seu-dominio-ngrok.app/webhook` no console do Twilio.
- **Modelo recomendado**: GPT-4o é recomendado para melhor performance e qualidade de respostas.
- **Tratamento de erros**: Implementamos verificações básicas de status dos runs, mas em produção amplie para mais casos de erro.
- **Rate limiting**: Considere implementar limitação de taxa para controlar custos e prevenir abusos em produção.

