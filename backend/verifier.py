from llm import ask_llm

def verify_answer(provider, question, context, draft_answer):

    prompt = f"""
You are Veritas AI Verification Agent.

Your ONLY source of truth is the Retrieved Context below.

Question:
{question}

Retrieved Context:
{context}

Draft Answer:
{draft_answer}

Your job is to improve the answer, NOT simply reject it.

Follow these rules carefully.

1. Compare the user's question against the retrieved evidence.

2. Evaluate every factual statement in the draft answer.

3. Keep every statement that is directly supported by the retrieved context.

4. Rewrite supported statements to improve clarity if necessary.

5. Remove statements that are contradicted by the retrieved context.

6. Never invent facts.

7. Never use outside knowledge.

8. If the user's question contains multiple parts:
   - Answer every part that is supported.
   - Ignore unsupported parts.
   - At the end briefly mention which parts could not be answered because the retrieved evidence does not contain enough information.

9. If the user refers to a person, event, medicine, organization, law or technology that does not appear anywhere in the retrieved context:
   explain that the retrieved evidence does not indicate that such an entity exists or contains no information about it.
   Do NOT assume the spelling is correct.
   Do NOT hallucinate.

10. Never mention "verification process", "draft answer", or "retrieved context".

11. Never say:
"I cannot verify..."

Instead naturally explain what the evidence does and does not show.

12. Produce one polished final answer exactly as if answering the user directly.

13. The final answer should:
- be well structured
- use markdown headings
- use bullet points when appropriate
- remain concise
- include historical context if available
- include dates if present
- conclude with a short summary

Return ONLY the final corrected answer.
"""

    return ask_llm(provider, prompt, "")