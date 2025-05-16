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

## Deploy no Render

Siga estes passos para fazer o deploy no Render:

1. **Crie uma nova conta no Render** (se ainda não tiver) em [https://render.com/](https://render.com/)

2. **Conecte seu repositório**
   - Vá para o [Dashboard do Render](https://dashboard.render.com/)
   - Clique em "New" e selecione "Web Service"
   - Conecte sua conta do GitHub/GitLab
   - Selecione o repositório do projeto

3. **Configure as variáveis de ambiente**
   - No painel de configuração do serviço, vá para a seção "Environment"
   - Adicione as seguintes variáveis:
     - `TWILIO_ACCOUNT_SID`: Seu SID da conta Twilio
     - `TWILIO_AUTH_TOKEN`: Seu token de autenticação Twilio
     - `OPENAI_API_KEY`: Sua chave da API da OpenAI
     - `OPENAI_ASSISTANT_ID`: ID do seu Assistante na OpenAI
     - `PORT`: 10000 (o Render definirá isso automaticamente, mas é bom ter como fallback)
     - `PYTHON_VERSION`: 3.10.8

4. **Configurações de build**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app -c gunicorn_config.py`

5. **Plano e região**
   - Selecione o plano gratuito (Free) para começar
   - Escolha a região mais próxima dos seus usuários

6. **Clique em "Create Web Service"**
   - O Render irá fazer o build e implantar sua aplicação
   - O processo pode levar alguns minutos na primeira vez

7. **Configure o webhook do Twilio**
   - Acesse o [Console do Twilio](https://www.twilio.com/console)
   - Vá para "Messaging" > "Settings" > "WhatsApp Sandbox Settings"
   - No campo "WHEN A MESSAGE COMES IN", insira a URL do seu webhook no Render:
     `https://seu-servico.onrender.com/webhook`
   - Certifique-se de que o método HTTP está definido como `HTTP POST`

8. **Teste a aplicação**
   - Envie uma mensagem para o número do WhatsApp Sandbox
   - Verifique os logs no painel do Render para depuração, se necessário

## Solução de Problemas Comuns

- **Erro de porta**: Certifique-se de que sua aplicação está configurada para usar a porta da variável de ambiente `PORT`
- **Timeout no deploy**: Verifique se o comando de inicialização está correto e se a aplicação está vinculada a `0.0.0.0`
- **Erros de dependência**: Verifique se todas as dependências estão listadas no `requirements.txt`
- **Logs**: Sempre verifique os logs no painel do Render para identificar problemas

## Alternativas de Deploy

Se preferir, você também pode implantar em:
- Railway
- Heroku
- Google Cloud Run
- AWS Elastic Beanstalk

## Licença

MIT
