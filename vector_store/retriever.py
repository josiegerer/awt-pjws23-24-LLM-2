from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from datetime import datetime

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
    pass 


def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2",
                                       model_kwargs={'device': 'cpu'})
    vector_store = FAISS.load_local('vector_store/faiss_store', embeddings)
    # llm = load_llm() local llama 
    qa_prompt = qa_prompt()
    qa = retrieval_qa(llm, qa_prompt, vector_store)

    return qa


def retriever_bot_answer(query):
    qa_bot_instance = qa_bot()
    bot_response = qa_bot_instance({"query": query})
    return bot_response


def result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response


# def chat_history(query, answer):
#     chat_history_list = []
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     chat_history_list.append({
#         "timestamp": timestamp,
#         "query": query,
#         "answer": answer})
#     return chat_history_list
