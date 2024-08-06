module.exports = {
    apps : [{
      name: 'main_process',  
      script: 'main_process.py',        
      interpreter: 'python3',    
      autorestart: true,         
      watch: true,               
      ignore_watch: ["node_modules", "logs"],  
      max_restarts: 10,          
      restart_delay: 5000,       
      max_memory_restart: '200M', 
      log_date_format: 'YYYY-MM-DD HH:mm:ss', 
      env: {
        NODE_ENV: 'production',
         
      },
      output: './logs/out.log',  
      error: './logs/error.log', 
    }]
  };
  
