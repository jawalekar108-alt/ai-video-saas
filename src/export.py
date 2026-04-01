from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def export_pdf(summary, transcript):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(summary, styles["BodyText"]))

    content.append(Spacer(1, 20))
    content.append(Paragraph("<b>Transcript</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(transcript[:3000], styles["BodyText"]))

    doc.build(content)

    buffer.seek(0)
    return buffer
