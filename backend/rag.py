from search import search_web
from extractor import extract_text
from chunker import chunk_text
from embedding import embed_chunks, embed_text
from vectordb import store_chunks, search_chunks, clear_database
from reranker import rerank
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
def process_site(site):

    print("Reading:", site["title"])

    page = extract_text(site["url"])

    if page is None:
        return None

    text = page["text"]

    if len(text) < 300:
        return None

    chunks = chunk_text(text)

    if not chunks:
        return None

    

    metadata = {
        "title": site["title"],
        "url": site["url"],
        "source": site["source"]
    }

    return {
    "chunks": chunks,
    "metadata": metadata
}
def build_rag(query):

    print("Finding relevant knowledge...")

    clear_database()

    t = time.time()
    websites = search_web(query)
    print(f"Web Search: {time.time()-t:.2f}s")

    documents_extracted = 0
    all_chunks = []
    chunk_metadata = []
    t = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = [
            executor.submit(process_site, site)
            for site in websites
        ]

        for future in as_completed(futures):

            try:
               result = future.result()
            except Exception as e:
               print("Error processing site:", e)
               continue

            if result is None:
               continue

            documents_extracted += 1

            chunks = result["chunks"]
            metadata = result["metadata"]

            all_chunks.extend(chunks)

            chunk_metadata.extend([metadata] * len(chunks))
    print(f"Extraction + Chunking: {time.time()-t:.2f}s")
    print("Knowledge Base Ready")
    print("Embedding all chunks together...")
    if not all_chunks:
       return {
        "sources": len(websites),
        "documents": 0
    }
    t = time.time()
    embeddings = embed_chunks(all_chunks)
    print(f"Embedding: {time.time()-t:.2f}s")
    print("Storing all chunks...")
    t = time.time()
    store_chunks(
    all_chunks,
    embeddings,
    chunk_metadata
)
    print(f"Store: {time.time()-t:.2f}s")
    return {
        "sources": len(websites),
        "documents": documents_extracted
    }

def retrieve(query):

    query_embedding = embed_text(query)

    results = search_chunks(query_embedding)

    t = time.time()

    results = rerank(
    query,
    results,
    top_k=8
)

    print(f"Reranking: {time.time()-t:.2f}s")

    return results