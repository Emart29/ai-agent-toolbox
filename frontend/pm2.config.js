module.exports = {
  apps: [
    {
      name: 'ai-agent-frontend',
      script: 'npx',
      args: 'serve -s dist -p 4173',
      cwd: '/path/to/frontend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
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
