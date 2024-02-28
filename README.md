# awt-pjws23-24-LLM-2
AWT Project WS23/24 Group: Large Language Models for Education: Generative Agents [2]

This project, conducted as part of the AWT course for WS23/24, focuses on utilize Large Language Models (LLMs) for educational purposes. Specifically, our objective is to develop Generative Agents capable of facilitating interactive and educational conversations. The agents are designed to..

Key Features:
- Backend: llm_service.py
  - Conversation Agent
  - Grammar Agent
  - Self-Conversation Agent
 
- Frontend:
  - UserChats
  - 

Techologies:
- Python
- JavaScript
- Vue.js
- LlaMA2 Model: llama-2-7b-chat.Q4_K_M.gguf

to run:
1. download MySQL Workbench (https://dev.mysql.com/downloads/workbench/) create a new server in MySQL Database
2. Navigate to app/backend and change PW and database name and then run app.py
3. Navigate to app/frontend and "npm run serve"
4. open browser and go to localhost:8080 (and close the error message if it occurs)
5. backend can be reached via localhost:5000/get_users/
