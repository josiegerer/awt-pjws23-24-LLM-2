from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

DB_FAISS_PATH = 'vector_store/faiss_store'


prompt_template = """Use the following information to answer the user's question.
If you don't know the answer, just say that you don't know, don't make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


def qa_prompt():
    prompt = PromptTemplate(template=prompt_template,
                            input_variables=['context', 'question'])
    return prompt


def retrieval_qa(llm, prompt, vector_store):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=vector_store.as_retriever(search_kwargs={'k': 3}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt})
    return qa_chain


def load_llm():
    model_path ="/Users/Admin/Documents/llm/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0.75,
    max_tokens=2048,
    top_p=1,
    verbose=True  

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2",
                                       model_kwargs={'device': 'cpu'})
    vector_store = FAISS.load_local('vector_store/faiss_store', embeddings)
    llm = load_llm() 
    qa_prompt = qa_prompt()
    qa = retrieval_qa(llm, qa_prompt, vector_store)

    return qa


def retriever_bot_answer(query):
    qa_bot_instance = qa_bot()
    bot_response = qa_bot_instance({"query": query})
    return bot_response

result = retriever_bot_answer("Wie viele Use Cases gibt es?")
print(result)

# def result(query):
#     qa_result = qa_bot()
#     response = qa_result({'query': query})
#     return response