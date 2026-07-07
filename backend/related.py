from llm import ask_llm


def generate_related(provider, question, answer):

    prompt = f"""
You are an AI research assistant.

Based on the user's question and the answer provided,
generate exactly 3 related follow-up research questions.

Rules:
- Questions should naturally continue the conversation.
- Do not repeat the original question.
- Keep each question under 15 words.
- Return ONLY the questions.
- One question per line.

User Question:
{question}

Answer:
{answer}
"""

    response = ask_llm(provider, prompt, "")

    questions = [
        q.strip("-•1234567890. ").strip()
        for q in response.split("\n")
        if q.strip()
    ]

    return questions[:3]