module.exports = {
  apps: [
    {
      name: 'ai-agent-backend',
      script: 'venv/bin/gunicorn',
      args: 'app.main:app -c gunicorn.conf.py',
      cwd: '/path/to/backend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
      },
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_file: './logs/combined.log',
      time: true,
    },
  ],
};
