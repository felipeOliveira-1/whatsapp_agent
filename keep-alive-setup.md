# Configuração de Keep-Alive para WhatsApp Agent

Este guia mostra como evitar que seu bot adormeça no plano gratuito do Render.

## Por que usar Keep-Alive?

No plano gratuito do Render, seu serviço "adormece" após 15 minutos de inatividade. Isso causa:
- Delays de 50+ segundos na primeira mensagem
- Possíveis timeouts do Twilio
- Experiência ruim para usuários

## Opção 1: UptimeRobot (Gratuito)

1. Acesse [uptimerobot.com](https://uptimerobot.com/) e crie uma conta gratuita

2. Crie um novo monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: WhatsApp Agent Keep-Alive
   - **URL**: `https://whatsapp-agent-hqfj.onrender.com/ping`
   - **Monitoring Interval**: 5 minutes

3. Clique em "Create Monitor"

## Opção 2: Cron-job.org (Gratuito)

1. Acesse [cron-job.org](https://cron-job.org/) e crie uma conta

2. Crie um novo cron job:
   - **URL**: `https://whatsapp-agent-hqfj.onrender.com/ping`
   - **Execution schedule**: Every 5 minutes
   - **Request method**: GET

3. Ative o cron job

## Opção 3: GitHub Actions (Gratuito)

Crie `.github/workflows/keep-alive.yml` no seu repositório:

```yaml
name: Keep Alive

on:
  schedule:
    - cron: '*/5 * * * *'  # A cada 5 minutos
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Service
        run: |
          curl https://whatsapp-agent-hqfj.onrender.com/ping
          echo "Keep-alive ping sent"
```

## Verificando se Funciona

1. Configure o keep-alive usando uma das opções acima
2. Aguarde alguns minutos
3. Verifique os logs no Render - você deve ver requisições periódicas para `/ping`
4. Teste enviando uma mensagem após período de inatividade - resposta deve ser rápida

## Observações

- O endpoint `/ping` retorna apenas "pong" para ser o mais leve possível
- Intervalo de 5 minutos é suficiente (Render adormece após 15 minutos)
- Monitoramento gratuito tem limites, mas suficiente para este uso
- Se precisar de 100% uptime, considere o plano pago do Render