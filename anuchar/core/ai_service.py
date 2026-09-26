import json
import requests
from . import config


def _groq_chat(messages, model, temperature=0.7):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": temperature,
        },
        timeout=45,
    )
    if r.status_code != 200:
        raise Exception(f"Groq error {r.status_code}: {r.text[:200]}")
    return r.json()["choices"][0]["message"]["content"]


def _ollama_chat(messages, model, temperature=0.7):
    import ollama
    r = ollama.chat(
        model=model,
        messages=messages,
        format="json",
        options={"temperature": temperature},
    )
    return r["message"]["content"]


def chat(query, history, model, provider="groq", system_prompt=None):
    system = system_prompt or _default_system()
    messages = [{"role": "system", "content": system}]
    messages += history[-10:]
    messages.append({"role": "user", "content": query})

    try:
        if provider == "groq":
            raw = _groq_chat(messages, model)
        else:
            raw = _ollama_chat(messages, model)

        data = json.loads(raw)
        return {
            "answer": data.get("answer", raw),
            "details": data.get("details", []),
            "options": data.get("options", []),
        }
    except json.JSONDecodeError:
        return {"answer": raw, "details": [], "options": []}
    except Exception as e:
        return {"answer": f"Error: {e}", "details": [], "options": []}


def _default_system():
    return """
You are Anuchar, a friendly and intelligent personal AI assistant.

STRICT RULES:
1. Reply in the SAME language as the user (Hindi/Hinglish/English).
2. Return ONLY valid JSON (no markdown, no code fences):
{
  "answer": "main answer (2-5 lines, clear & helpful)",
  "details": ["related point 1", "related point 2", "related point 3"],
  "options": ["short follow-up 1", "short follow-up 2", "short follow-up 3"]
}
3. "details" = 2 to 5 important related points.
4. "options" = 3 to 4 short follow-up questions.
5. If DOCUMENT CONTEXT provided, use it for accuracy.
6. If WEB RESULTS provided, cite them naturally.
"""


def chat_with_context(query, history, model, provider,
                       doc_context=None, web_context=None):
    system = _default_system()
    if doc_context:
        system += f"\n\n=== DOCUMENT CONTEXT ===\n{doc_context}\n=== END ==="
    if web_context:
        system += f"\n\n=== WEB RESULTS ===\n{web_context}\n=== END ==="

    messages = [{"role": "system", "content": system}]
    messages += history[-10:]
    messages.append({"role": "user", "content": query})

    try:
        if provider == "groq":
            raw = _groq_chat(messages, model)
        else:
            raw = _ollama_chat(messages, model)
        data = json.loads(raw)
        return {
            "answer": data.get("answer", raw),
            "details": data.get("details", []),
            "options": data.get("options", []),
        }
    except json.JSONDecodeError:
        return {"answer": raw, "details": [], "options": []}
    except Exception as e:
        return {"answer": f"Error: {e}", "details": [], "options": []}
