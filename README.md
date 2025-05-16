# WhatsApp OpenAI Assistant

Integração direta entre WhatsApp (via Twilio) e OpenAI Assistant v2 usando Python e Flask.

## Visão Geral

Este projeto implementa um Assistant da OpenAI que opera dentro do WhatsApp, utilizando:
- **Twilio API** para receber e enviar mensagens via WhatsApp
- **OpenAI Assistants API v2** para processamento e geração de respostas inteligentes
- **Flask** como framework web para gerenciar webhooks e requisições

## Funcionalidades

- Recebe mensagens do WhatsApp via webhook do Twilio
- Mantém contexto de conversas usando Threads da OpenAI
- Processa mensagens com o Assistant API v2 da OpenAI 
- Envia respostas de volta para o WhatsApp

## Requisitos

- Python 3.8+
- Conta Twilio com configuração para WhatsApp
- Conta OpenAI com acesso ao Assistants API
- Flask e outras dependências listadas em `requirements.txt`

## Configuração

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente em um arquivo `.env`:
   ```
   TWILIO_ACCOUNT_SID=seu_sid_aqui
   TWILIO_AUTH_TOKEN=seu_token_aqui
   OPENAI_API_KEY=sua_chave_api_aqui
   OPENAI_ASSISTANT_ID=id_do_seu_assistant
   PORT=5000
   DEBUG=True
   ```
4. Execute a aplicação: `python app.py`
5. Use Ngrok para expor seu servidor local: `ngrok http 5000`
6. Configure o webhook no console do Twilio

## Deploy

Para deploy em produção, recomendamos:
- Render
- Railway
- Heroku
- Google Cloud Run

## Licença

MIT
