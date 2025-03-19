from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_report(output_path, summary_text):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawString(100, 750, "⚡ Power Fault Analysis Report ⚡")
    c.drawString(100, 730, summary_text)
    c.save()
