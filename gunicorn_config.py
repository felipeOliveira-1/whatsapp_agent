import os

bind = "0.0.0.0:" + os.environ.get("PORT", "5000")
workers = 2
threads = 4
timeout = 120
worker_class = "sync"
loglevel = "info"
