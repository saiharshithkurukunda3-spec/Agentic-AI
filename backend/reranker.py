from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, results, top_k=8):

    documents = results["documents"]
    distances = results["distances"]
    metadatas = results["metadatas"]

    if not documents:
        return {
            "documents": [],
            "distances": [],
            "metadatas": [],
            "scores": []
        }

    pairs = [
        [query, doc]
        for doc in documents
    ]

    scores = reranker.predict(pairs)
    print(scores)
    ranked = sorted(
        zip(
            scores,
            documents,
            distances,
            metadatas
        ),
        key=lambda x: x[0],
        reverse=True
    )

    ranked = ranked[:top_k]

    return {
        "documents": [x[1] for x in ranked],
        "distances": [x[2] for x in ranked],
        "metadatas": [x[3] for x in ranked],
        "scores": [float(x[0]) for x in ranked]
    }
