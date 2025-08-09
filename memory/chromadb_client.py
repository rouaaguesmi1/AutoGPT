# memory/chromadb_client.py
import chromadb
from langchain_chroma import Chroma # <-- NEW
from langchain_ollama import OllamaEmbeddings # <-- NEW
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Initialize a persistent ChromaDB client
client = chromadb.PersistentClient(path="./chromadb_data")

# Use local embeddings from Ollama (this line is now correct)
embeddings = OllamaEmbeddings(model="llama3")

# Create or get the vector store collection (this line is now correct)
vector_store = Chroma(
    client=client,
    collection_name="autogpt_memory",
    embedding_function=embeddings,
)

def add_text_to_memory(text: str, metadata: dict = None):
    """Splits text and adds it to the persistent vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = [Document(page_content=chunk, metadata=metadata or {}) for chunk in text_splitter.split_text(text)]
    vector_store.add_documents(docs)
    print(f"Added {len(docs)} document chunks to memory.")

def get_retriever(k_value: int = 5):
    """Returns a retriever for the vector store."""
    return vector_store.as_retriever(search_kwargs={'k': k_value})

# Example of how to add initial data
# add_text_to_memory("Initial data point: The project started on a Tuesday.", {"source": "initial_setup"})