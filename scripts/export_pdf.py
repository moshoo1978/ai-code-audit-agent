import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet


def generate_pdf_report(
    markdown_path, output_pdf_path='output_data/PA_UCC_Compliance_Report.pdf'
):
  """Converts the generated markdown audit report into a professional PDF document."""
  os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

  doc = SimpleDocTemplate(
      output_pdf_path,
      pagesize=letter,
      rightMargin=54,
      leftMargin=54,
      topMargin=54,
      bottomMargin=54,
  )

  styles = getSampleStyleSheet()
  title_style = ParagraphStyle(
      'DocTitle',
      parent=styles['Heading1'],
      fontSize=20,
      leading=24,
      textColor=colors.HexColor('#1A365D'),
      spaceAfter=12,
  )

  body_style = ParagraphStyle(
      'DocBody',
      parent=styles['BodyText'],
      fontSize=10,
      leading=14,
      spaceAfter=8,
  )

  story = []
  story.append(
      Paragraph('🏛️ PA UCC Architectural Code Audit Report', title_style)
  )
  story.append(
      HRFlowable(
          width='100%',
          thickness=1.5,
          color=colors.HexColor('#1A365D'),
          spaceAfter=15,
      )
  )

  if os.path.exists(markdown_path):
    with open(markdown_path, 'r') as f:
      lines = f.readlines()

    for line in lines:
      clean_line = line.strip()
      if not clean_line:
        continue
      if clean_line.startswith('#'):
        story.append(
            Paragraph(
                f"<b>{clean_line.replace('#', '').strip()}</b>",
                styles['Heading2'],
            )
        )
      else:
        story.append(Paragraph(clean_line, body_style))
  else:
    story.append(Paragraph('No audit report content found.', body_style))

  doc.build(story)
  return output_pdf_path