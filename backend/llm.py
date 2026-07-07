import os
import ollama
import google.generativeai as genai
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
print("OPENROUTER:", os.getenv("OPENROUTER_API_KEY"))
from openai import OpenAI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are Veritas AI, an advanced research assistant that produces factual, evidence-based research answers.

Use ONLY the retrieved context provided below.

If the retrieved context does not contain enough information to answer confidently, clearly state:

"The available sources do not provide sufficient evidence to fully answer this question."

Never guess or invent facts.

When referring to evidence, NEVER say:
- "the provided document"
- "the provided context"

Instead use phrases such as:
- "According to the retrieved sources..."
- "Based on the available sources..."
- "The retrieved evidence indicates..."
- "Multiple retrieved sources state..."

Guidelines:

• Write a detailed, research-quality explanation.
• Explain concepts step by step.
• Use clear markdown headings.
• Use bullet points whenever useful.
• Include historical background when relevant.
• Include important dates, people, organizations and facts from the sources.
• If multiple sources agree, synthesize them naturally.
• If retrieved sources conflict, acknowledge the disagreement instead of choosing one without explanation.
• Never include information that is not supported by the retrieved context.

Answer Structure (adapt when appropriate):

# Overview

# Background

# Detailed Explanation

# Key Facts

# Applications / Importance

# Conclusion

Context:

{context}

Question:

{question}

Return your response EXACTLY in this format:

## Answer
<Write the complete answer here>

## Related Questions
- Question 1
- Question 2
- Question 3

Rules for Related Questions:
- Generate exactly 3 questions.
- They should naturally continue the topic.
- Do not repeat the original question.
- Keep each question under 15 words.
- Do not output anything outside this format.
"""

def ask_ollama(question, context):

    prompt = PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )

    response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "num_predict": 1200,
        "temperature": 0.2
    }
)

    return response["message"]["content"]


def ask_gemini(question, context):

    prompt = PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text



def ask_groq(question, context):

    prompt = PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1200
    )

    return response.choices[0].message.content


def ask_llm(provider, question, context):

    if provider == "ollama":
        return ask_ollama(question, context)

    elif provider == "gemini":
        return ask_gemini(question, context)

    elif provider == "groq":
        return ask_groq(question, context)

    else:
        raise ValueError("Invalid provider")