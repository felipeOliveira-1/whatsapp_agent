import os
import multiprocessing

# Configuração básica - Render espera que a aplicação use a porta 10000 por padrão
bind = "0.0.0.0:" + os.environ.get("PORT", "10000")

# Número de workers baseado no número de CPUs disponíveis
try:
    workers = multiprocessing.cpu_count() * 2 + 1
except:
    workers = 3  # Fallback para 3 workers se não for possível detectar CPUs

# Configuração de threads por worker
threads = 2

# Timeout aumentado para evitar timeouts em operações longas
timeout = 300  # 5 minutos

# Worker class
worker_class = "gthread"

# Logging
loglevel = "info"
accesslog = "-"  # Log para stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Manter o worker vivo por um tempo razoável
max_requests = 1000
max_requests_jitter = 50

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
