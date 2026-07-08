<div align="center">

# VERITAS AI

### Truth. Backed by Evidence.

An AI-powered research assistant that reduces hallucinations using **Retrieval-Augmented Generation (RAG)**, **semantic search**, and **live web retrieval**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# Overview

VERITAS AI is a research-focused AI assistant designed to produce **fact-based, evidence-backed answers** rather than relying solely on an LLM's internal knowledge.

Instead of answering questions directly, the system first performs a **live web search**, extracts relevant information, converts the extracted text into semantic embeddings, stores them inside a vector database, retrieves the most relevant evidence, and finally generates a response grounded in that retrieved context.

This Retrieval-Augmented Generation (RAG) pipeline significantly reduces hallucinations and improves answer reliability.

---

# Key Features

- 🔍 Live web search
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic search using Sentence Transformers
- 🗄️ ChromaDB vector database
- 🤖 Multiple AI providers
  - Gemini
  - Groq
  - Ollama
- 📖 Source-backed responses
- 📊 Retrieval confidence score
- ✅ Automatic answer verification
- 💡 AI-generated follow-up questions
- ⚡ FastAPI backend
- 🎨 React frontend

---

# Architecture

```
                    User Question
                          │
                          ▼
                 React Frontend
                          │
                          ▼
                  FastAPI Backend
                          │
                          ▼
                  Live Web Search
                          │
                          ▼
               Content Extraction
                          │
                          ▼
                 Document Chunking
                          │
                          ▼
             Sentence Embeddings
                          │
                          ▼
             ChromaDB Vector Store
                          │
                          ▼
              Semantic Retrieval
                          │
                          ▼
              Context Construction
                          │
                          ▼
          Gemini / Groq / Ollama
                          │
                          ▼
              Verification Layer
                          │
                          ▼
                  Final Response
```

---

# How It Works

## 1. User Query

The user submits a research question through the React frontend.

Example:

> How is Artificial Intelligence transforming healthcare?

---

## 2. Live Web Search

The backend performs a real-time search using DDGS to gather recent and relevant web pages.

---

## 3. Content Extraction

Each webpage is processed using **Trafilatura**, which removes unnecessary HTML, advertisements, menus, and page clutter while preserving meaningful content.

---

## 4. Text Chunking

Long articles are divided into smaller chunks for efficient embedding and retrieval.

---

## 5. Semantic Embeddings

Each chunk is converted into a dense vector using:

```
all-MiniLM-L6-v2
```

This enables semantic similarity instead of keyword matching.

---

## 6. Vector Database

Embeddings are stored inside **ChromaDB** together with metadata such as

- Title
- URL
- Source

---

## 7. Semantic Retrieval

The user's query is embedded using the same model.

The vector database retrieves the most relevant chunks based on semantic similarity.

---

## 8. Context Generation

The retrieved evidence is combined into a single research context.

Only this retrieved information is sent to the language model.

---

## 9. AI Answer Generation

The selected language model receives

- User Question
- Retrieved Context

Supported providers

- Gemini
- Groq
- Ollama

The model generates a structured answer using only the supplied evidence.

---

## 10. Verification

If retrieval confidence is low, a verification stage compares the generated answer against the retrieved evidence and removes unsupported statements.

---

## 11. Final Output

The frontend displays

- Research Answer
- Supporting Sources
- Confidence Score
- Related Questions
- Search Summary

---

# Tech Stack

## Frontend

- React
- JavaScript
- HTML5
- CSS3

## Backend

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Trafilatura
- DDGS Search
- Gemini API
- Groq API
- Ollama

---

# Project Structure

```
Agentic-AI/

│
├── backend/
│   ├── chunker.py
│   ├── embedding.py
│   ├── extractor.py
│   ├── llm.py
│   ├── main.py
│   ├── rag.py
│   ├── reranker.py
│   ├── search.py
│   ├── vectordb.py
│   ├── verifier.py
│   └── database/
│
├── frontend/
│
├── requirements.txt
│
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Agentic-AI.git

cd Agentic-AI
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

### Required Packages

- fastapi
- uvicorn
- python-dotenv
- chromadb
- sentence-transformers
- transformers
- torch
- numpy
- trafilatura
- ddgs
- google-generativeai
- groq
- ollama
- pydantic

---

# Environment Variables

Create a `.env` file inside the **backend** directory.

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

GROQ_API_KEY=YOUR_GROQ_API_KEY

OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

---

# Running the Backend

```bash
cd backend

uvicorn main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

---

# Running the Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# API

### POST `/ask`

Request

```json
{
    "question":"What is Artificial Intelligence?",
    "provider":"gemini"
}
```

Supported providers

- gemini
- groq
- ollama

---

# Current Limitations

- Depends on publicly available websites.
- Some websites may block automated extraction.
- Free AI APIs may enforce rate limits.
- Response quality depends on retrieved evidence.
- Ollama requires a locally installed model.

---

# Running the Backend

The backend is intended to be run locally.

It uses several machine learning libraries including **Torch**, **Sentence Transformers**, **ChromaDB**, and optionally **Ollama**, all of which have platform-specific dependencies and may require additional configuration when deployed to cloud services.

For the best experience:

1. Clone the repository.
2. Install the dependencies listed above.
3. Add your API keys.
4. Run the FastAPI backend locally.

The frontend can then communicate with the local backend without any additional modifications.

---

# Future Improvements

- PDF Research Reports
- APA / MLA Citation Generator
- Chat History
- Source Credibility Ranking
- Research Session Saving
- Multi-document Comparison
- Academic Paper Search
- User Authentication
- Streaming Responses
- Multi-language Support

---


# Running with Ollama (Unlimited Local Inference)

VERITAS AI supports **Ollama** as a local Large Language Model provider.

Using Ollama allows you to run the application without relying on paid cloud APIs, making it suitable for unlimited local experimentation (subject to your computer's hardware resources).

## 1. Install Ollama

Download and install Ollama from:

https://ollama.com/download

Verify the installation:

```bash
ollama --version
```

---

## 2. Pull the Required Model

VERITAS AI is configured to use:

```bash
ollama pull qwen2.5:3b
```

If you wish to use another model, update the model name inside `backend/llm.py`.

Examples:

```bash
ollama pull llama3.2:3b
```

```bash
ollama pull gemma3:4b
```

```bash
ollama pull mistral:7b
```

---

## 3. Start the Ollama Server

Before running the backend, start the Ollama service.

On most systems:

```bash
ollama serve
```

Leave this terminal running.

---

## 4. Select Ollama in VERITAS AI

When sending requests to the backend, set the provider to:

```json
{
    "question": "Explain Quantum Computing",
    "provider": "ollama"
}
```

---

## Why Use Ollama?

- ✅ No API usage charges
- ✅ No daily request limits
- ✅ Unlimited local inference
- ✅ Better privacy since data stays on your machine
- ✅ Works offline after the model has been downloaded

> **Note:** Performance depends on your system specifications. Larger models require more RAM and CPU/GPU resources.


# Author

## Sai Harshith

VERITAS AI was developed as a project demonstrating how Retrieval-Augmented Generation, semantic search, vector databases, and modern language models can be combined to produce more reliable, transparent, and evidence-grounded AI research assistants.

---

## If you found this project useful, consider giving it a ⭐ on GitHub!
