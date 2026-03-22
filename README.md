# Online Payslip Portal

A full-stack web application for securely managing and retrieving employee payslips with PDF processing capabilities.

## Features

✅ **User Portal**: Search and view payslips by employee ID, month, and year  
✅ **Admin Panel**: Upload PDF files containing payslip data  
✅ **PDF Processing**: Automatic extraction of salary data from PDFs  
✅ **Database**: SQLite integration for persistent data storage  
✅ **PDF Download**: Generate and download payslips as PDF files  
✅ **Responsive Design**: Mobile-friendly UI with modern gradient design  
✅ **Security**: Input validation and SQL injection prevention  
✅ **API Endpoints**: RESTful API for all operations  

## Project Structure

```
payslip-portal/
│
├── frontend/                      # Frontend files
│   ├── index.html                # Main portal page
│   ├── admin.html                # Admin upload page
│   ├── style.css                 # CSS styling
│   └── script.js                 # Frontend JavaScript
│
├── backend/                       # Backend Flask application
│   ├── app.py                    # Main Flask application
│   ├── init_db.py                # Database initialization script
│   ├── create_sample_pdf.py      # Sample PDF generator
│   ├── requirements.txt          # Python dependencies
│   ├── uploads/                  # Uploaded PDF files
│   └── database/                 # SQLite database
│       └── payslip.db
│
└── README.md                      # This file
```

## Tech Stack

### Frontend
- HTML5
- CSS3 with gradients and animations
- Vanilla JavaScript (ES6+)

### Backend
- Python Flask 2.3.2
- Flask-CORS for cross-origin requests
- SQLite3 database
- PyMuPDF/pdfplumber for PDF processing
- ReportLab for PDF generation

### Database
- SQLite (lightweight, no server needed)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python init_db.py
   ```

5. **Create sample PDF (optional):**
   ```bash
   python create_sample_pdf.py
   ```

### Frontend Setup

No installation needed! The frontend runs directly in the browser.

## Running the Application

### Start Backend Server

From the `backend` folder:

```bash
python app.py
```

The backend will start at: `http://localhost:5000`

### Open Frontend

Open `frontend/index.html` in your web browser or serve it with a simple HTTP server:

```bash
# Python 3
cd frontend
python -m http.server 8000

# Then open: http://localhost:8000
```

## Usage

### User Portal (index.html)

1. **Select Contract**: Choose from available contracts (e.g., SMSE-JASMINE)
2. **Select Month**: Choose the month for the payslip
3. **Select Year**: Choose the year
4. **Enter Employee ID**: Input your employee ID
5. **Search**: Click "Search Payslip" to retrieve your payslip
6. **View & Download**: View salary breakdown and download as PDF

Sample Employee IDs to test:
- `EMP001` - John Doe
- `EMP002` - Jane Smith
- `EMP003` - Michael Johnson

### Admin Panel (admin.html)

1. **Navigate to Admin Panel**: Click "Admin Panel" link on main page
2. **Upload PDF**: 
   - Click the upload area or drag-drop a PDF file
   - The system will auto-extract payslip data
   - Data is stored in the database
3. **View Results**: Success message confirms data storage

## API Endpoints

### 1. Upload PDF
**POST** `/upload-pdf`

Upload a PDF containing payslip data. The system extracts employee information and salary details.

**Request:**
```
Content-Type: multipart/form-data
- file: PDF file
- contract: (optional) Contract name
```

**Response:**
```json
{
  "success": true,
  "message": "PDF processed and data stored successfully",
  "extracted_data": {
    "employee_id": "EMP001",
    "employee_name": "John Doe",
    "basic_salary": 50000,
    "hra": 10000,
    "allowances": 5000,
    "deductions": 5000,
    "net_salary": 60000,
    "month": "March",
    "year": "2026"
  }
}
```

### 2. Search Payslip
**GET** `/search-payslip`

Search for a payslip by employee ID, month, and year.

**Query Parameters:**
- `employee_id` (required): Employee ID
- `month` (required): Month name (e.g., "March")
- `year` (required): Year (e.g., "2026")
- `contract` (optional): Contract name

**Example:**
```
GET /search-payslip?employee_id=EMP001&month=March&year=2026
```

**Response:**
```json
{
  "success": true,
  "payslip": {
    "employee_id": "EMP001",
    "employee_name": "John Doe",
    "month": "March",
    "year": "2026",
    "basic_salary": 50000,
    "hra": 10000,
    "allowances": 5000,
    "deductions": 5000,
    "net_salary": 60000
  }
}
```

### 3. Generate Payslip PDF
**POST** `/generate-payslip-pdf`

Generate a formatted payslip PDF from payslip data.

**Request Body:**
```json
{
  "employee_id": "EMP001",
  "employee_name": "John Doe",
  "month": "March",
  "year": "2026",
  "basic_salary": 50000,
  "hra": 10000,
  "allowances": 5000,
  "deductions": 5000,
  "net_salary": 60000
}
```

**Response:** PDF file download

### 4. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## Database Schema

### payslips table

```sql
CREATE TABLE payslips (
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
);
```

**Indexes:**
- `idx_employee_month_year`: On (employee_id, month, year)
- `idx_employee_id`: On (employee_id)

## PDF Extraction Logic

The system uses regex patterns to extract the following fields from PDFs:

- **Employee ID**: Patterns like "Employee ID:", "EMP ID:", "ID:"
- **Employee Name**: Extracted after "Employee Name:" or "Name:"
- **Basic Salary**: Numeric value after "Basic Salary:" or "Basic"
- **HRA**: Numeric value after "HRA"
- **Allowances**: Numeric value after "Allowances" or "Other Allowances"
- **Deductions**: Numeric value after "Deductions" or "Total Deductions"
- **Net Salary**: Numeric value after "Net Salary" or "Take Home"
- **Month & Year**: Extracted from patterns like "Month: March, 2026"

The system handles currency symbols (₹, $) and comma-separated numbers.

## Deployment Guide

### Option 1: Vercel (Recommended for Frontend)

**Frontend:**
```bash
cd frontend
# Upload to Vercel directly from GitHub repo
```

**Backend:**
```bash
cd backend
# Deploy to Vercel with vercel.json configuration
```

### Option 2: Render.com

1. Push code to GitHub
2. Connect repository to Render
3. Create Web Service for backend
4. Set environment variables
5. Deploy

### Option 3: Railway

1. Create account at railway.app
2. Connect GitHub repository
3. Add environment variables
4. Deploy automatically

### Option 4: Docker

**Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["python", "app.py"]
```

**Build and run:**
```bash
docker build -t payslip-portal .
docker run -p 5000:5000 payslip-portal
```

## Environment Configuration

Create a `.env` file in the backend folder:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/payslip.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800
```

## Security Features

1. **Input Validation**: All inputs are validated before database operations
2. **CORS Protection**: Cross-Origin Resource Sharing configured
3. **File Type Validation**: Only PDF files allowed
4. **SQL Injection Prevention**: Parameterized SQL queries
5. **SQL Alchemy Not Needed**: Direct SQLite with parameterized queries
6. **Safe File Handling**: Secure filename generation and path handling

## Error Handling

The application handles various error scenarios:

- **Missing required fields**: Returns 400 error with clear message
- **File upload errors**: Validates file type and size
- **PDF processing errors**: Handles corrupted or unreadable PDFs
- **Database errors**: Graceful error messages
- **Network errors**: Frontend displays user-friendly error messages

## Troubleshooting

### Issue: "PDF library not installed"

**Solution:**
```bash
pip install PyMuPDF reportlab
# OR
pip install pdfplumber reportlab
```

### Issue: "Database locked"

**Solution:**
- Close other connections to the database
- Restart the Flask application

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Kill the process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: CORS errors in browser console

**Solution:**
- Ensure backend is running on `http://localhost:5000`
- Check that `API_BASE_URL` in `script.js` is correct
- Verify CORS is enabled in `app.py`

## Sample Test Data

The database includes pre-loaded sample payslips:

| Employee ID | Name | Month | Year | Basic | HRA | Allowances | Deductions | Net |
|---|---|---|---|---|---|---|---|---|
| EMP001 | John Doe | March | 2026 | 50,000 | 10,000 | 5,000 | 5,000 | 60,000 |
| EMP002 | Jane Smith | March | 2026 | 55,000 | 11,000 | 5,500 | 6,000 | 65,500 |
| EMP003 | Michael Johnson | March | 2026 | 60,000 | 12,000 | 6,000 | 7,000 | 71,000 |

## Performance Optimization

- **Database Indexes**: Fast queries on frequently searched fields
- **Caching**: Can be added using Redis
- **Lazy Loading**: PDF data extracted only on upload
- **Async Processing**: Can be implemented with Celery

## Future Enhancements

- [ ] Multi-language support
- [ ] User authentication and authorization
- [ ] Email notification for payslips
- [ ] Bulk PDF processing
- [ ] Advanced reporting dashboard
- [ ] Export to Excel/CSV
- [ ] Email integration
- [ ] Dark mode
- [ ] Mobile app

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, please check the troubleshooting section or contact the development team.

---

**Powered by PAVI TECH**
