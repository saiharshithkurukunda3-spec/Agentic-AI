from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text):
    return model.encode(
        text,
        normalize_embeddings=True
    )


def embed_chunks(chunks):
    return model.encode(
        chunks,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False
    )