from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_report(itinerary: str, budget_summary: str, risk_summary: str, emergency_contacts: str) -> BytesIO:
    output = BytesIO(); document = canvas.Canvas(output, pagesize=A4); text = document.beginText(48, 800); text.setFont('Helvetica', 11)
    for heading, content in [('AI Travel Itinerary', itinerary), ('Budget Summary', budget_summary), ('Risk Summary', risk_summary), ('Emergency Contacts', emergency_contacts)]:
        text.textLine(heading); text.textLines(content); text.textLine('')
        if text.getY() < 70: document.drawText(text); document.showPage(); text = document.beginText(48, 800); text.setFont('Helvetica', 11)
    document.drawText(text); document.save(); output.seek(0); return output
