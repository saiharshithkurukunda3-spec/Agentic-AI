from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse
import time

from rag import build_rag, retrieve
from llm import ask_llm
from verifier import verify_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    provider: str


@app.get("/")
def health():
    return {"status": "online"}


@app.post("/ask")
def ask(request: QuestionRequest):

    start_time = time.time()

    print("Step 1 : Building Knowledge Base")

    stats = build_rag(request.question)

    print("Step 2 : Retrieving Relevant Chunks")

    results = retrieve(request.question)

    docs = results["documents"]
    distances = results["distances"]
    metadata = results["metadatas"]
    scores = results["scores"]

    # Nothing retrieved
    if not docs:
        return {
            "answer": "No relevant information found.",
            "confidence": 0,
            "sources": [],
            "summary": {
                "sources_searched": stats["sources"],
                "documents_extracted": stats["documents"],
                "chunks_retrieved": 0,
                "engine": "Ollama" if request.provider == "ollama" else "Gemini 2.5 Flash",
                "verification": "Skipped",
                "time_taken": round(time.time() - start_time, 2)
            }
        }

    # ---------- Sources ----------

    sources = []
    seen = set()

    for m in metadata:

        url = m.get("url")

        if url not in seen:

            seen.add(url)

            sources.append({
                "title": m.get("title"),
                "url": url,
                "source": m.get("source"),
                "domain": urlparse(url).netloc.lower()
            })

    # ---------- Confidence ----------
    import math

    if scores:
       top_scores = scores[:3]
       avg_score = sum(top_scores) / len(top_scores)
 
       confidence = round(
        100 / (1 + math.exp(-avg_score)),
        2
    )
    else:
       confidence = 0

    # ---------- Context ----------

    context = "\n\n".join(docs)

    print("Generating draft...")
    t=time.time()
    response = ask_llm(
    request.provider,
    request.question,
    context
)
    print(f"LLM Generation: {time.time()-t:.2f}s")
    answer = response
    related_questions = []

    try:

        if "## Related Questions" in response:

           answer_part, related_part = response.split(
            "## Related Questions",
            1
           )

           answer = answer_part.replace(
            "## Answer",
            ""
           ).strip()

           related_questions = [

              line.strip("-•1234567890. ").strip()

              for line in related_part.split("\n")

              if line.strip()

           ][:3]

    except Exception:

      answer = response
      related_questions = []

    print(f"Retrieval Confidence: {confidence:.2f}%")

# Only verify when retrieval confidence is low
    if confidence >= 80:

        print("High confidence retrieval. Skipping verification.")

        final_answer = answer
        verification_status = "Skipped (High Confidence)"

    else:

        print("Low confidence retrieval. Running verification...")

        final_answer = verify_answer(
        request.provider,
        request.question,
        context,
        answer
    )

        verification_status = "Applied"

    

    
    

    elapsed = round(time.time() - start_time, 2)

    engine = (
        "Ollama"
        if request.provider == "ollama"
        else "Gemini 2.5 Flash"
    )
    print(f"TOTAL: {time.time()-start_time:.2f}s")
    return {

        "answer": final_answer,

        "confidence": confidence,

        "sources": sources,
         
        "related_questions": related_questions,
 
        "summary": {

            "sources_searched": stats["sources"],

            "documents_extracted": stats["documents"],

            "chunks_retrieved": len(docs),

            "engine": engine,

            "verification": verification_status,

            "time_taken": elapsed

        }

    }