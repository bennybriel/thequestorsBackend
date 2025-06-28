from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import Dict, Any
from ..interfaces import IPdfGenerator

class PdfGenerator(IPdfGenerator):
    def generate_pdf(self, plan_data: Dict[str, Any]) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        elements.append(Paragraph("Career Development Plan", styles['Title']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Career Section
        elements.append(Paragraph("Career Path", styles['Heading1']))
        career_table = Table([
            ["Title", plan_data['career']['title']],
            ["Description", plan_data['career']['description']],
            ["Salary Range", plan_data['career']['salary_range']]
        ], colWidths=[100, 400])
        career_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(career_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # Education Section
        elements.append(Paragraph("Education Path", styles['Heading1']))
        edu_data = [["University", "Country", "Ranking", "Avg Salary"]]
        for uni in plan_data['education']['universities']:
            edu_data.append([
                uni['name'],
                uni['country'],
                str(uni['ranking']),
                f"${uni['salary']:,.0f}"
            ])
        
        edu_table = Table(edu_data)
        edu_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(edu_table)
        
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf