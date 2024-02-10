#!pip install langchain llama-cpp-python 

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "You are a helpful, respectful and honest assistant. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. \
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. \
    Always answer in a simple manner without any exaggerations."

SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS

def get_prompt(instruction):
    return B_INST + SYSTEM_PROMPT + instruction + E_INST

# chat_history = []

import os
os.listdir("/Users/josi/Llama2_weights")

llm = LlamaCpp(
    model_path = "/Users/josi/Llama2_weights/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0.3,
    max_tokens=1024,
    top_p=1,
    # callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

prompt = get_prompt("Correct the following sentence: Hau is the wether today?")
llm(prompt)