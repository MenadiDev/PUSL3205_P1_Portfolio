import hashlib
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Define folder paths
DOCUMENTS_FOLDER = Path("documents")
CHROMA_FOLDER = "chroma_db"


# 2. Load all PDF documents
documents = []

pdf_files = list(DOCUMENTS_FOLDER.glob("*.pdf"))

if not pdf_files:
    print("No PDF files found in the documents folder.")
    exit()

for pdf_file in pdf_files:
    print(f"Loading: {pdf_file.name}")

    loader = PyMuPDFLoader(str(pdf_file))
    pdf_documents = loader.load()

    # Same metadata as app.py: file name as source, plus a fingerprint of the
    # PDF content used to build stable chunk IDs.
    file_hash = hashlib.sha256(pdf_file.read_bytes()).hexdigest()
    for doc in pdf_documents:
        doc.metadata["source"] = pdf_file.name
        doc.metadata["file_hash"] = file_hash

    documents.extend(pdf_documents)


# 3. Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Total PDF files: {len(pdf_files)}")
print(f"Total document chunks: {len(chunks)}")


# 4. Load the embedding model
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:0.6b"
)


# 5. Store embeddings in ChromaDB
# Uses the same de-duplicated collection and stable chunk IDs as app.py, so
# running this script again updates existing chunks instead of duplicating them.
def chunk_id(chunk):
    """Stable ID built exactly like app.py: file hash + page + chunk text hash."""
    chunk_hash = hashlib.sha256(chunk.page_content.encode("utf-8")).hexdigest()
    page = chunk.metadata.get("page", 0)
    return hashlib.sha256(
        f"{chunk.metadata['file_hash']}_{page}_{chunk_hash}".encode("utf-8")
    ).hexdigest()


ids = [chunk_id(chunk) for chunk in chunks]

# Drop chunks that are identical within this run (same source, page and text)
unique = dict(zip(ids, chunks))

vector_store = Chroma(
    collection_name="university_docs_clean",
    persist_directory=CHROMA_FOLDER,
    embedding_function=embeddings,
)
vector_store.add_documents(documents=list(unique.values()), ids=list(unique.keys()))

print(f"Unique chunks stored: {len(unique)}")

print("Documents successfully stored in ChromaDB!")