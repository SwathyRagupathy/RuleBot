import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS

# === CONFIG ===
PDF_FILE = "crossroads.pdf"         
INDEX_DIR = "faiss_index"                

# === 1. Load PDF ===
print(f"📄 Loading PDF: {PDF_FILE}")
loader = PyPDFLoader(PDF_FILE)
documents = loader.load()

# === 2. Split into Chunks ===
print("✂️ Splitting into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# === 3. Embed using HuggingFace ===
print("🔗 Creating embeddings...")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embedding_model)

# === 4. Save Index ===
os.makedirs(INDEX_DIR, exist_ok=True)
vectorstore.save_local(INDEX_DIR)
print(f"✅ FAISS index saved to: {INDEX_DIR}")
