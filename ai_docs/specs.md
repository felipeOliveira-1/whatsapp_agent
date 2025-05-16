# Specs.md

## ❓ Problema

Usuários desejam interagir com um assistente baseado em IA via WhatsApp, utilizando uma arquitetura leve e eficiente.

## 💡 Solução Implementada

Desenvolvimento de uma aplicação Python com Flask para conectar diretamente o Twilio (WhatsApp) à API de Assistants v2 da OpenAI, eliminando a necessidade de ferramentas de orquestração externas.

## 📝️ Arquitetura Final

- **Usuário (WhatsApp)** → 
- **Twilio Webhook** → 
- **Flask App (Endpoint /webhook)** → 
- **OpenAI Assistants API v2** → 
- **Flask App (Resposta via Twilio)** →
- **Usuário (Resposta no WhatsApp)**

## 🔧 Divisão de Módulos/Fases

1. **Recepção de Mensagens**
   - Endpoint Flask configurado para receber webhooks do Twilio
   - Ngrok para expor o servidor local durante desenvolvimento

2. **Processamento com OpenAI**
   - Gerenciamento de threads por usuário (número WhatsApp)
   - Uso da API de Assistants v2 com o cabeçalho adequado
   - Criação e gerenciamento de threads e runs

3. **Envio de Resposta**
   - Resposta formatada usando TwiML para o Twilio
   - Rastreamento de execução via logs

4. **Persistência de Contexto**
   - Armazenamento de IDs de threads em dicionário (em produção: banco de dados)

## ✅ Critérios de Aceitação

- Mensagens enviadas no WhatsApp são respondidas automaticamente pelo Assistant da OpenAI
- O código Python é modular e bem documentado
- As integrações com Twilio e OpenAI são autenticadas via variáveis de ambiente
- As respostas são relevantes e coerentes com o contexto da conversa mantido via threads
- A solução é escalonável e pode ser implantada em ambientes de produção

## 🤖 Validação

- Testes manuais com mensagens reais no WhatsApp
- Logs detalhados em cada fase do processamento
- Tratamento de erros para responder apropriadamente em casos de falha
- Monitoramento das chamadas à API da OpenAI para controle de custos
