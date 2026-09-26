import pypdf
import pdfplumber


def extract_text(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception:
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        except Exception:
            return ""
    return text.strip()


def find_relevant(text, query, top_k=4, chunk_size=800):
    if not text:
        return ""

    chunks = []
    for i in range(0, len(text), chunk_size - 100):
        chunks.append(text[i:i + chunk_size])

    query_words = set(w.lower() for w in query.split() if len(w) > 2)
    if not query_words:
        return "\n\n---\n\n".join(chunks[:top_k])

    scored = []
    for chunk in chunks:
        cl = chunk.lower()
        score = sum(1 for w in query_words if w in cl)
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [c for s, c in scored[:top_k] if s > 0]
    if not top:
        top = [c for s, c in scored[:top_k]]

    return "\n\n---\n\n".join(top)
