import os
import sys
import glob
import json
import shutil
import argparse
import requests
import pypdf
import chromadb
from chromadb.utils import embedding_functions

# Configuration
PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "pdf_rag_docs"
OLLAMA_URL = "https://aud-thomas-citizen-inspector.trycloudflare.com/api/generate"
MODEL_NAME = "gemma3:12b"

def extract_chunks_from_pdfs(pdf_folder, chunk_size=800, chunk_overlap=150):
    """
    Reads all PDF files in pdf_folder, extracts text page by page,
    and splits into overlapping text chunks with source metadata.
    """
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))
    if not pdf_files:
        print(f"Warning: No PDF files found in {pdf_folder}")
        return []

    chunks = []
    chunk_id = 0

    for pdf_path in pdf_files:
        file_name = os.path.basename(pdf_path)
        print(f"Processing PDF: {file_name}...")
        try:
            reader = pypdf.PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text or not text.strip():
                    continue
                
                start = 0
                text_len = len(text)
                while start < text_len:
                    end = min(start + chunk_size, text_len)
                    chunk_text = text[start:end].strip()
                    
                    if chunk_text:
                        chunks.append({
                            "id": f"chunk_{chunk_id}",
                            "text": chunk_text,
                            "metadata": {
                                "source": file_name,
                                "page": page_num
                            }
                        })
                        chunk_id += 1
                    
                    start += chunk_size - chunk_overlap
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    print(f"Extracted {len(chunks)} text chunks from {len(pdf_files)} PDF file(s).")
    return chunks

def setup_vector_database(chunks, reset_db=False):
    """
    Initializes ChromaDB persistent client and inserts text chunks into the collection.
    """
    if reset_db and os.path.exists(CHROMA_DB_DIR):
        print(f"Resetting existing database at {CHROMA_DB_DIR}...")
        shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)

    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    
    # Try SentenceTransformer embedding function first, fallback to DefaultEmbeddingFunction
    try:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    except Exception:
        ef = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    if chunks and collection.count() == 0:
        print(f"Populating ChromaDB collection '{COLLECTION_NAME}'...")
        ids = [c["id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        
        batch_size = 50
        for i in range(0, len(ids), batch_size):
            print(f"Indexing batch {i // batch_size + 1}/{(len(ids) + batch_size - 1) // batch_size}...")
            collection.add(
                ids=ids[i:i+batch_size],
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size]
            )
        print(f"Successfully indexed {len(ids)} document chunks into ChromaDB!")
    else:
        print(f"ChromaDB collection '{COLLECTION_NAME}' ready ({collection.count()} chunks indexed).")

    return collection

def query_ollama(prompt, system_context="", model=MODEL_NAME):
    """
    Sends the prompt + context to the Ollama endpoint.
    """
    full_prompt = f"""You are an intelligent assistant. Answer the user's question accurately using ONLY the provided context below.
If the context does not contain enough information to answer, state that clearly.

--- RETRIEVED PDF CONTEXT ---
{system_context}
-----------------------------

Question: {prompt}

Answer:"""

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError:
            lines = [line.strip() for line in response.text.strip().splitlines() if line.strip()]
            data = json.loads(lines[-1])

        if isinstance(data, dict) and "response" in data:
            return data["response"]
        return str(data)
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def ask_question(query, collection, n_results=4):
    """
    Retrieves relevant PDF chunks from ChromaDB and queries the LLM.
    """
    print(f"\nSearching ChromaDB for: '{query}'...")
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        print("No relevant context found in PDFs.")
        return

    print("\n--- RETRIEVED SOURCES ---")
    context_blocks = []
    for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        source_info = f"Source: {meta.get('source', 'Unknown')} (Page {meta.get('page', '?')})"
        print(f"[{idx}] {source_info}")
        print(f"    Excerpt: {doc[:140]}...\n")
        context_blocks.append(f"[{source_info}]\n{doc}")

    system_context = "\n\n".join(context_blocks)

    print("Querying Ollama LLM with retrieved context...")
    answer = query_ollama(query, system_context=system_context)
    print("\n--- RAG ANSWER ---")
    print(answer)
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="ChromaDB RAG for PDFs")
    parser.add_argument("--query", type=str, help="Single query to ask")
    parser.add_argument("--reset", action="store_true", help="Reset ChromaDB collection")
    args = parser.parse_args()

    print("=== ChromaDB PDF RAG System ===")
    
    # 1. Load and chunk PDFs
    chunks = extract_chunks_from_pdfs(PDF_DIR)
    
    # 2. Setup Vector DB
    collection = setup_vector_database(chunks, reset_db=args.reset)

    # 3. Query Execution
    query = args.query if args.query else "What is Arjuna's distress about on the battlefield?"
    ask_question(query, collection)

if __name__ == "__main__":
    main()
