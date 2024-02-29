# awt-pjws23-24-LLM-2
AWT Project WS23/24 Group: Large Language Models for Education: Generative Agents [2]

## Project Overview
This project, conducted as part of the AWT course for WS23/24, focuses on utilize Large Language Models (LLMs) for educational purposes. Specifically, our objective is to develop Generative Agents capable of facilitating interactive and educational conversations. 
Two specific use-cases are utilized:
1. Conversation Agent: <br>This agent is designed to engage in conversations with users in a natural and interactive manner, similar to everyday discussions. It supports language style variations, allowing users to switch between formal and informal communication.


2. Grammar Correction Agent: <br>The Grammar Correction Agent aims to provide users with valuable feedback on their written sentences, addressing both syntactical and semantical aspects.

In addition to the primary use-cases, two other agents have been implemented:
- Analysis and Evaluation Agent:<br>
This agent analyzes and evaluates the language used by the user, providing constructive feedback.
- Endless Conversation Agent:<br>
This agent facilitates an endless conversation between two agents, simulating an ongoing discussion/conversation on a specific topic.


To achieve our objectives, we leveraged the Langchain framework combined with the Llama2-7b model.

<!-- Key Features:
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
- LlaMA2 Model: llama-2-7b-chat.Q4_K_M.gguf -->

<!-- to run:
1. download MySQL Workbench (https://dev.mysql.com/downloads/workbench/) create a new server in MySQL Database
2. Navigate to app/backend and change PW and database name and then run app.py
3. Navigate to app/frontend and "npm run serve"
4. open browser and go to localhost:8080 (and close the error message if it occurs)
5. backend can be reached via localhost:5000/get_users/ -->

# Setup and Requirements
## Database
1. Download MySQL and preferably MySQL Workbench (https://dev.mysql.com/downloads/workbench/)
2. Create / Open Database Connection and Create a new Schema
3. Change the database credentials `DB_PATH` (`mysql+pymysql://<username>:<password>@localhost/<schemaname>`) in the file `constants.py` at location `/app/backend`. Example: mysql+pymysql://root:LLMsAreGreat@localhost/test_llm_app
4. Run the script `init_database.py` at location `/app/backend`

## Frontend
Install the following packages:
- Node: v16.17.0 (https://nodejs.org/en/blog/release/v16.17.0)
- npm: 8.15.0 (https://www.npmjs.com/package/npm/v/8.15.0)
- Vue Version: @vue/cli 5.0.8 (https://www.npmjs.com/package/@vue/cli/v/5.0.8)

## Backend
1. Python version 3.10.11 should be used. Python 3.11 should also be possible to use, but using version 3.12.x might break the code due to compatibility reason for certain libraries (faiss-cpu)
2. Change the `MODEL_PATH` in `constants.py` at `/app/backend` to the correct location of the quantized LLM.
3. <i>Optional:</i> If a custom vector-store is used also change the location stored in the variable `DB_FAISS_PATH` according to Step 2 above.
4. <i>Optional:</i> If a User has more than 12GB RAM, using a higher `max_token` count (default=1024) can be utilized in `constants.py` for a better conversation experience.<br>
<b>NOTE:</b> The `max_token` count will be highly effected for the Conversation Use-Case and much less for the Grammar Correction/Analysis Use-Case.

# Usage
## Backend
1. Run the following command in the root of the project: `pip install -r requirements.txt` 
2. To start the backend run the file `app.py` at location `/app/backend` using the command: `python app.py` 

## Frontend
1. Navigate to `/app/frontend` and run:`npm install`
2. After successful installation run: `npm run serve`
3. Now `localhost:8080` should be reachable


# TODO
- Create `init_database.py` file
- Create tunnel via ngrok utilizing API directly on top of Google Colab 
- Utilize Constants in backend
- Write requirements.txt