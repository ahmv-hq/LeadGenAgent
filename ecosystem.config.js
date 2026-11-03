module.exports = {
  apps: [
    {
      name: "tamimah-whatsapp-gateway",
      cwd: "./gateway",
      script: "server.js",
      watch: false,
      restart_delay: 3000,
      env: {
        NODE_ENV: "production",
        PORT: 3001
      }
    },
    {
      name: "tamimah-dashboard-agent",
      cwd: "./",
      script: "app.py",
      interpreter: "python",
      watch: false,
      restart_delay: 3000,
      env: {
        PYTHONIOENCODING: "utf-8",
        PORT: 8000
      }
    }
  ]
};
