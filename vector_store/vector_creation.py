from langchain.document_loaders import PyPDFLoader, DirectoryLoader, WebBaseLoader, UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

DB_FAISS_PATH = "./vector_store/faiss_store"
DATA_DIR = "./vector_store/data"

def vector_store_creation():
    html_loader = DirectoryLoader(DATA_DIR, glob="*.html", loader_cls=UnstructuredHTMLLoader)
    pdf_loader = DirectoryLoader(DATA_DIR, glob="*.pdf", loader_cls=PyPDFLoader)

    # web_loader = WebBaseLoader(["https://medium.com/@orangecollege/what-is-the-difference-between-general-and-academic-english-4890a698f578",
    #                            "https://speakenglishalfresco.com/blog/informal-vs-formal-language/",
    #                            "https://www.busuu.com/en/languages/informal-vs-formal",
    #                            "https://languagetool.org/insights/post/formal-vs-informal-style/",
    #                            "https://testmaximizer.com/formal-and-informal"])

    all_loaders = [pdf_loader, html_loader]

    documents = []
    for loader in all_loaders:
        documents.extend(loader.load())

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
    chunked_documents = text_splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2", 
        model_kwargs={"device": "cpu"},)

    vector_store = FAISS.from_documents(
    documents=chunked_documents,
    embedding=embedding_model)

    vector_store.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    vector_store_creation()