import chromadb
import uuid

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection(
    name="research_documents"
)


def clear_database():

    data = collection.get()

    if data["ids"]:
        collection.delete(ids=data["ids"])


def store_chunks(chunks, embeddings, metadata_list):

    ids = [str(uuid.uuid4()) for _ in chunks]

    metadatas = []

    for metadata, chunk in zip(metadata_list, chunks):

        metadatas.append({

            **metadata,

            "chunk_length": len(chunk)

        })

    collection.add(

        ids=ids,

        documents=chunks,

        embeddings=embeddings.tolist(),

        metadatas=metadatas

    )


def search_chunks(query_embedding, top_k=10):

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=[
            "documents",
            "distances",
            "metadatas"
        ]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    scores = [1 - d for d in distances]   # convert distance to similarity

    return {
        "documents": documents,
        "distances": distances,
        "metadatas": metadatas,
        "scores": scores
    }