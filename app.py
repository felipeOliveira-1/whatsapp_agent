import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import json
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')  # Carregar do .env
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')  # Manter seguro
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Manter seguro
ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID')  # ID do seu Assistant

# Inicializar cliente OpenAI com a versão v2 da API de Assistants
client = OpenAI(
    api_key=OPENAI_API_KEY,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

# Dicionário para armazenar threads por número de telefone
# Em produção, usar um banco de dados
user_threads = {}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Página inicial para verificar se o serviço está funcionando"""
    return {"status": "online", "service": "WhatsApp OpenAI Assistant"}

@app.route('/', methods=['POST'])
def root_webhook():
    """Rota alternativa para capturar requisições enviadas para a raiz"""
    return webhook()

@app.route('/webhook', methods=['POST'])
def webhook():
    # Extrair informações da mensagem
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')  # formato: whatsapp:+numero
    
    print(f"Mensagem recebida de {sender}: {incoming_msg}")
    
    # Gerenciar thread do usuário
    thread_id = get_or_create_thread(sender)
    
    # Adicionar mensagem ao thread
    add_message_to_thread(thread_id, incoming_msg)
    
    # Executar o assistant
    run_id = run_assistant(thread_id)
    
    # Aguardar a conclusão e obter a resposta
    response_text = get_assistant_response(thread_id, run_id)
    
    # Preparar resposta para o WhatsApp
    resp = MessagingResponse()
    resp.message(response_text)
    
    return Response(str(resp), mimetype="application/xml")

def get_or_create_thread(user_id):
    """Obtém thread existente ou cria um novo"""
    if user_id in user_threads:
        return user_threads[user_id]
    
    # Criar um novo thread
    thread = client.beta.threads.create()
    user_threads[user_id] = thread.id
    print(f"Novo thread criado para {user_id}: {thread.id}")
    return thread.id

def add_message_to_thread(thread_id, message_content):
    """Adiciona uma mensagem ao thread"""
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content
    )
    print(f"Mensagem adicionada ao thread {thread_id}")

def run_assistant(thread_id):
    """Executa o assistant no thread"""
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    print(f"Assistant executado no thread {thread_id}, run_id: {run.id}")
    return run.id

def get_assistant_response(thread_id, run_id):
    """Aguarda a conclusão do run e obtém a resposta"""
    # Aguardar conclusão
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            return "Desculpe, houve um problema ao processar sua mensagem."
        # Verificar outros estados possíveis
        elif run_status.status in ['expired', 'cancelled']:
            return "A operação foi cancelada ou expirou. Por favor, tente novamente."
        
        time.sleep(1)  # Aguardar 1 segundo antes de verificar novamente
    
    # Obter mensagens
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    # Extrair a resposta mais recente do assistente
    for message in messages.data:
        if message.role == 'assistant':
            return message.content[0].text.value
    
    return "Desculpe, não consegui processar sua mensagem."

# Função para enviar mensagem diretamente (fora do webhook)
def send_whatsapp_message(to_number, message_body):
    from twilio.rest import Client
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número do Twilio Sandbox
        body=message_body,
        to=f'whatsapp:{to_number}'
    )
    
    return message.sid

# Função para enviar mensagem usando template (para iniciar conversa)
def send_template_message(to_number, template_id, variables):
    from twilio.rest import Client
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número do Twilio Sandbox
        content_sid=template_id,
        content_variables=json.dumps(variables),
        to=f'whatsapp:{to_number}'
    )
    
    return message.sid

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint simples para verificar se a aplicação está funcionando"""
    return {"status": "ok", "timestamp": time.time()}

@app.route('/ping', methods=['GET'])
def ping():
    """Endpoint ultra-leve para keep-alive"""
    return "pong", 200

if __name__ == '__main__':
    # Configura a porta a partir da variável de ambiente ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    print(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=(os.environ.get('DEBUG', 'False').lower() == 'true'))
