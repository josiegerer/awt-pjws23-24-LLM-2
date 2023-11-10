# Set env var OPENAI_API_KEY or load from a .env file:
#import dotenv
#dotenv.load_dotenv()
import os
import langchain
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

os.environ

chat = ChatOpenAI()
chat(
    [
        HumanMessage(
            content="Translate this sentence from English to French: I love programming."
        )
    ]
)

messages = [
    SystemMessage(
        content="You are a helpful assistant that translates English to French."
    ),
    HumanMessage(content="I love programming."),
]
chat(messages)