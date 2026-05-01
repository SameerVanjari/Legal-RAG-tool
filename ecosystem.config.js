module.exports = {
  apps: [
    {
      name: 'legal-rag-backend',
      cwd: './',
      command: './venv/bin/fastapi run src/main.py --port 5000 --host 0.0.0.0',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        PYTHONPATH: './src',
        // Add any environment variables needed for the backend here
      }
    },
    {
      name: 'legal-rag-ui',
      cwd: './',
      command: './venv/bin/streamlit run src/ui.py --server.port 8501 --server.address 0.0.0.0',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        // Streamlit will use the API_BASE_URL from the environment or default to http://localhost:8000
        // We can set it explicitly if needed, but the ui.py already defaults to localhost:8000
        API_BASE_URL: 'http://localhost:5000',
        // Optional: Streamlit specific settings
        STREAMLIT_SERVER_HEADLESS: 'true',
        STREAMLIT_SERVER_ENABLE_CORS: 'false',
        STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION: 'false'
      }
    }
  ]
};