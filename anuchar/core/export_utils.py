import io
from datetime import datetime
from fpdf import FPDF


def _clean(text):
    """FPDF core fonts are latin-1 only; replace unsupported chars safely."""
    if not text:
        return ""
    return text.encode("latin-1", "replace").decode("latin-1")


def export_chat_txt(messages, title="Anuchar Chat Export"):
    """Chat history ko plain .txt bytes me export karta hai."""
    lines = [f"{title}", f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "-" * 40, ""]
    for m in messages:
        role = "You" if m.get("role") == "user" else "Anuchar"
        lines.append(f"{role}: {m.get('content', '')}")
        lines.append("")
    return "\n".join(lines).encode("utf-8")


def export_chat_pdf(messages, title="Anuchar Chat Export"):
    """Chat history ko PDF bytes me export karta hai."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _clean(title), ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 8, _clean(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
    pdf.ln(4)

    for m in messages:
        role = "You" if m.get("role") == "user" else "Anuchar"
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, _clean(f"{role}:"))
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _clean(m.get("content", "")))
        pdf.ln(2)

    out = pdf.output(dest="S")
    if isinstance(out, str):
        out = out.encode("latin-1", "replace")
    return bytes(out)


def export_document_txt(name, content):
    """Extracted document text ko .txt bytes me export karta hai."""
    header = f"{name}\nExported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'-'*40}\n\n"
    return (header + (content or "")).encode("utf-8")


def export_tasks_pdf(tasks, title="Anuchar - Tasks"):
    """Task list ko PDF me export karta hai. tasks = list of (id, title, done)."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _clean(title), ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 8, _clean(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    for _id, t_title, done in tasks:
        box = "[x]" if done else "[ ]"
        pdf.multi_cell(0, 8, _clean(f"{box} {t_title}"))

    out = pdf.output(dest="S")
    if isinstance(out, str):
        out = out.encode("latin-1", "replace")
    return bytes(out)
