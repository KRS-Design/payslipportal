"""
Sample PDF Creation Script
This script creates a sample PDF with payslip data for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_sample_pdf():
    """Create a sample payslip PDF"""
    
    filename = "sample_payslip.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#9c27b0'),
        spaceAfter=20,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("PAYSLIP", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Employee Information - With fields the extraction script will recognize
    employee_info = [
        ['Employee ID:', 'EMP001'],
        ['Employee Name:', 'John Doe'],
        ['Month & Year:', 'March, 2026'],
    ]
    
    emp_table = Table(employee_info, colWidths=[2*inch, 4*inch])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e5f5')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(emp_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Salary Breakdown - With recognizable field names
    salary_data = [
        ['Description', 'Amount'],
        ['Basic Salary', '₹ 50,000.00'],
        ['HRA', '₹ 10,000.00'],
        ['Allowances', '₹ 5,000.00'],
        ['Deductions', '₹ 5,000.00'],
        ['', ''],
        ['Net Salary', '₹ 60,000.00'],
    ]
    
    salary_table = Table(salary_data, colWidths=[3*inch, 3*inch])
    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9c27b0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3e5f5')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(salary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Powered by PAVI TECH", footer_style))
    
    # Build PDF
    doc.build(elements)
    print(f"Sample PDF created: {filename}")

if __name__ == '__main__':
    create_sample_pdf()
