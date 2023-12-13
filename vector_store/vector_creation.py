from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

DB_FAISS_PATH = "./vector_store/faiss_store"
DATA_DIR = "./vector_store/data"

def vector_store_creation():
    loader = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader) # add pdf file and change line
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
    chunked_documents = text_splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", 
        model_kwargs={"device": "cpu"},)

    vector_store = FAISS.from_documents(
    documents=chunked_documents,
    embedding=embedding_model)

    vector_store.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    vector_store_creation()