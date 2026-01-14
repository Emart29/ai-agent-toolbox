"""
Gunicorn configuration file for production deployment
"""
import os
import multiprocessing

# Server socket
bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'ai-agent-toolbox'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Preload app for better performance
preload_app = True

# Restart workers after this many requests (helps prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

def on_starting(server):
    """Called just before the master process is initialized."""
    print("=" * 60)
    print("🚀 Starting AI Agent Toolbox API (Production)")
    print("=" * 60)

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("🔄 Reloading workers...")

def when_ready(server):
    """Called just after the server is started."""
    print("=" * 60)
    print("✅ Server is ready to accept connections")
    print(f"   Workers: {workers}")
    print(f"   Bind: {bind}")
    print("=" * 60)

def on_exit(server):
    """Called just before exiting Gunicorn."""
    print("=" * 60)
    print("🛑 Shutting down AI Agent Toolbox API")
    print("=" * 60)
