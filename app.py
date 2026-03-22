"""
Online Payslip Portal - Backend
Flask Application with SQLite Database
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sqlite3
import os
import io
from datetime import datetime
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

try:
    import fitz  # PyMuPDF
    PDF_LIBRARY = 'fitz'
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = 'pdfplumber'
    except ImportError:
        PDF_LIBRARY = None
        print("Warning: No PDF library found. Install PyMuPDF or pdfplumber")

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DATABASE_FOLDER = os.path.join(os.path.dirname(__file__), 'database')
DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'payslip.db')
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Flask App Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS
CORS(app)

# ========================
# DATABASE FUNCTIONS
# ========================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()

    # Create payslips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payslips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            contract TEXT,
            month TEXT NOT NULL,
            year TEXT NOT NULL,
            basic_salary REAL,
            hra REAL,
            allowances REAL,
            deductions REAL,
            net_salary REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(employee_id, month, year)
        )
    ''')

    # Create index for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee_month_year ON payslips(employee_id, month, year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee_id ON payslips(employee_id)')

    conn.commit()
    conn.close()

def insert_payslip(employee_id, employee_name, contract, month, year, 
                   basic_salary, hra, allowances, deductions, net_salary):
    """Insert payslip data into database"""
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR REPLACE INTO payslips 
            (employee_id, employee_name, contract, month, year, basic_salary, hra, allowances, deductions, net_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, employee_name, contract, month, year, basic_salary, hra, allowances, deductions, net_salary))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting payslip: {e}")
        return False
    finally:
        conn.close()

def search_payslip(employee_id, month, year, contract=None):
    """Search payslip from database"""
    conn = get_db()
    cursor = conn.cursor()

    try:
        if contract:
            cursor.execute('''
                SELECT * FROM payslips 
                WHERE employee_id = ? AND month = ? AND year = ? AND contract = ?
            ''', (employee_id, month, year, contract))
        else:
            cursor.execute('''
                SELECT * FROM payslips 
                WHERE employee_id = ? AND month = ? AND year = ?
            ''', (employee_id, month, year))

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        print(f"Error searching payslip: {e}")
        return None
    finally:
        conn.close()

# ========================
# PDF PROCESSING FUNCTIONS
# ========================

def extract_salary_fields(text):
    """Extract salary fields from PDF text using regex"""
    salary_data = {}

    # Extract Employee ID
    emp_id_pattern = r'(?:Employee\s+ID|EMP\s+ID|ID)[\s:]*([A-Z0-9]+)'
    emp_id_match = re.search(emp_id_pattern, text, re.IGNORECASE)
    if emp_id_match:
        salary_data['employee_id'] = emp_id_match.group(1).strip()

    # Extract Employee Name
    name_pattern = r'(?:Employee\s+Name|Name)[\s:]*([A-Za-z\s]+?)(?:\n|$|Employee)'
    name_match = re.search(name_pattern, text, re.IGNORECASE)
    if name_match:
        salary_data['employee_name'] = name_match.group(1).strip()

    # Extract Basic Salary
    basic_pattern = r'(?:Basic\s+Salary|Basic)[\s:]*[\$₹\s]*([0-9]+(?:[,.][0-9]{2})?)'
    basic_match = re.search(basic_pattern, text, re.IGNORECASE)
    if basic_match:
        salary_data['basic_salary'] = float(basic_match.group(1).replace(',', ''))

    # Extract HRA
    hra_pattern = r'(?:HRA)[\s:]*[\$₹\s]*([0-9]+(?:[,.][0-9]{2})?)'
    hra_match = re.search(hra_pattern, text, re.IGNORECASE)
    if hra_match:
        salary_data['hra'] = float(hra_match.group(1).replace(',', ''))

    # Extract Allowances
    allow_pattern = r'(?:Allowances|Other\s+Allowances)[\s:]*[\$₹\s]*([0-9]+(?:[,.][0-9]{2})?)'
    allow_match = re.search(allow_pattern, text, re.IGNORECASE)
    if allow_match:
        salary_data['allowances'] = float(allow_match.group(1).replace(',', ''))

    # Extract Deductions
    ded_pattern = r'(?:Deductions|Total\s+Deductions)[\s:]*[\$₹\s]*([0-9]+(?:[,.][0-9]{2})?)'
    ded_match = re.search(ded_pattern, text, re.IGNORECASE)
    if ded_match:
        salary_data['deductions'] = float(ded_match.group(1).replace(',', ''))

    # Extract Net Salary
    net_pattern = r'(?:Net\s+Salary|Take\s+Home)[\s:]*[\$₹\s]*([0-9]+(?:[,.][0-9]{2})?)'
    net_match = re.search(net_pattern, text, re.IGNORECASE)
    if net_match:
        salary_data['net_salary'] = float(net_match.group(1).replace(',', ''))

    # Extract Month and Year
    date_pattern = r'(?:Month|Period)[\s:]*([A-Za-z]+)\s*,?\s*([0-9]{4})'
    date_match = re.search(date_pattern, text, re.IGNORECASE)
    if date_match:
        salary_data['month'] = date_match.group(1).capitalize()
        salary_data['year'] = date_match.group(2)

    return salary_data

def extract_pdf_text(file_path):
    """Extract text from PDF using available library"""
    try:
        if PDF_LIBRARY == 'fitz':
            import fitz
            pdf_document = fitz.open(file_path)
            text = ''
            for page in pdf_document:
                text += page.get_text()
            pdf_document.close()
            return text
        elif PDF_LIBRARY == 'pdfplumber':
            import pdfplumber
            text = ''
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''
            return text
        else:
            return None
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========================
# ROUTES
# ========================

@app.route('/')
def index():
    """Serve main page"""
    return "Payslip Portal Backend - API Running"

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF upload for admin"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Only PDF files are allowed'}), 400

        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract PDF text
        if not PDF_LIBRARY:
            return jsonify({'success': False, 'message': 'PDF processing library not installed'}), 500

        pdf_text = extract_pdf_text(file_path)
        if not pdf_text:
            return jsonify({'success': False, 'message': 'Failed to read PDF'}), 400

        # Extract salary data
        salary_data = extract_salary_fields(pdf_text)

        if not salary_data.get('employee_id'):
            return jsonify({'success': False, 'message': 'Could not extract employee ID from PDF'}), 400

        # Insert into database
        success = insert_payslip(
            employee_id=salary_data.get('employee_id', ''),
            employee_name=salary_data.get('employee_name', 'Unknown'),
            contract=request.form.get('contract', 'UNKNOWN'),
            month=salary_data.get('month', 'Unknown'),
            year=salary_data.get('year', '2026'),
            basic_salary=salary_data.get('basic_salary', 0),
            hra=salary_data.get('hra', 0),
            allowances=salary_data.get('allowances', 0),
            deductions=salary_data.get('deductions', 0),
            net_salary=salary_data.get('net_salary', 0)
        )

        if success:
            return jsonify({
                'success': True,
                'message': 'PDF processed and data stored successfully',
                'extracted_data': salary_data
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Error storing payslip data'}), 500

    except Exception as e:
        print(f"Error in upload_pdf: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/search-payslip', methods=['GET'])
def search_payslip_route():
    """Search payslip by employee ID, month, year"""
    try:
        employee_id = request.args.get('employee_id', '').strip()
        month = request.args.get('month', '').strip()
        year = request.args.get('year', '').strip()
        contract = request.args.get('contract', '').strip()

        # Validation
        if not all([employee_id, month, year]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters: employee_id, month, year'
            }), 400

        # Search database
        payslip = search_payslip(employee_id, month, year, contract)

        if payslip:
            return jsonify({
                'success': True,
                'payslip': {
                    'employee_id': payslip['employee_id'],
                    'employee_name': payslip['employee_name'],
                    'month': payslip['month'],
                    'year': payslip['year'],
                    'basic_salary': payslip['basic_salary'],
                    'hra': payslip['hra'],
                    'allowances': payslip['allowances'],
                    'deductions': payslip['deductions'],
                    'net_salary': payslip['net_salary']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Payslip not found'
            }), 404

    except Exception as e:
        print(f"Error in search_payslip_route: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/generate-payslip-pdf', methods=['POST'])
def generate_payslip_pdf():
    """Generate payslip as PDF"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#9c27b0'),
            spaceAfter=30,
            alignment=1
        )

        # Title
        elements.append(Paragraph("PAYSLIP", title_style))
        elements.append(Spacer(1, 0.3*inch))

        # Employee Information
        emp_info = [
            ['Employee Name', data.get('employee_name', '-')],
            ['Employee ID', data.get('employee_id', '-')],
            ['Month & Year', f"{data.get('month', '-')}, {data.get('year', '-')}"],
        ]

        emp_table = Table(emp_info, colWidths=[2*inch, 4*inch])
        emp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))

        elements.append(emp_table)
        elements.append(Spacer(1, 0.3*inch))

        # Salary Breakdown
        salary_data = [
            ['Description', 'Amount'],
            ['Basic Salary', f"₹ {data.get('basic_salary', 0):,.2f}"],
            ['HRA', f"₹ {data.get('hra', 0):,.2f}"],
            ['Allowances', f"₹ {data.get('allowances', 0):,.2f}"],
            ['Deductions', f"₹ {data.get('deductions', 0):,.2f}"],
            ['', ''],
            ['Net Salary', f"₹ {data.get('net_salary', 0):,.2f}"],
        ]

        salary_table = Table(salary_data, colWidths=[3*inch, 3*inch])
        salary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9c27b0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3e5f5')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINESTYLE', (0, -2), (-1, -2), 0),
        ]))

        elements.append(salary_table)
        elements.append(Spacer(1, 0.5*inch))

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

        # Prepare response
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Payslip_{data.get('employee_id')}_{data.get('month')}_{data.get('year')}.pdf"
        )

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

# ========================
# MAIN
# ========================

if __name__ == '__main__':
    # Initialize database
    init_database()

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
