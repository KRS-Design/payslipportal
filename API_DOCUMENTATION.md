# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, the API does not require authentication. For production, implement:
- JWT tokens
- API keys
- OAuth 2.0

## Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint**: `GET /health`

**Response**: 
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Status Code**: 200

---

### 2. Upload PDF
Upload a PDF file containing payslip data.

**Endpoint**: `POST /upload-pdf`

**Headers**:
```
Content-Type: multipart/form-data
```

**Form Parameters**:
- `file` (required): PDF file (max 50MB)
- `contract` (optional): Contract name

**Example cURL**:
```bash
curl -X POST http://localhost:5000/upload-pdf \
  -F "file=@payslip.pdf" \
  -F "contract=SMSE-JASMINE"
```

**Response (Success - 200)**:
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

**Response (Error - 400)**:
```json
{
  "success": false,
  "message": "Only PDF files are allowed"
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad request (no file, wrong format)
- `500`: Server error

---

### 3. Search Payslip
Search for a payslip by employee ID, month, and year.

**Endpoint**: `GET /search-payslip`

**Query Parameters** (all required):
- `employee_id` (string): Employee ID (e.g., "EMP001")
- `month` (string): Month name (e.g., "March", "January")
- `year` (string): Year (e.g., "2026", "2025")
- `contract` (string, optional): Contract name

**Example Request**:
```
GET /search-payslip?employee_id=EMP001&month=March&year=2026&contract=SMSE-JASMINE
```

**Example cURL**:
```bash
curl "http://localhost:5000/search-payslip?employee_id=EMP001&month=March&year=2026"
```

**Response (Success - 200)**:
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

**Response (Not Found - 404)**:
```json
{
  "success": false,
  "message": "Payslip not found"
}
```

**Response (Error - 400)**:
```json
{
  "success": false,
  "message": "Missing required parameters: employee_id, month, year"
}
```

**Status Codes**:
- `200`: Success
- `400`: Missing or invalid parameters
- `404`: Payslip not found
- `500`: Server error

---

### 4. Generate Payslip PDF
Generate a formatted payslip PDF.

**Endpoint**: `POST /generate-payslip-pdf`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
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

**Example cURL**:
```bash
curl -X POST http://localhost:5000/generate-payslip-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "employee_name": "John Doe",
    "month": "March",
    "year": "2026",
    "basic_salary": 50000,
    "hra": 10000,
    "allowances": 5000,
    "deductions": 5000,
    "net_salary": 60000
  }' \
  --output payslip.pdf
```

**Response**: Binary PDF file

**Response Headers**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="Payslip_EMP001_March_2026.pdf"
```

**Status Codes**:
- `200`: PDF generated
- `400`: Missing or invalid data
- `500`: Server error

---

## Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "message": "Error description"
}
```

### Common Error Messages

| Message | Cause | Solution |
|---------|-------|----------|
| "No file provided" | Missing file in upload | Ensure file is included in request |
| "Only PDF files are allowed" | Wrong file type | Upload only PDF files |
| "Could not extract employee ID from PDF" | PDF doesn't contain employee ID | Ensure PDF has employee ID field |
| "Missing required parameters" | Missing query parameters | Include all required parameters |
| "Payslip not found" | No matching payslip in database | Check employee ID, month, year |
| "PDF processing library not installed" | Missing dependencies | Install PyMuPDF or pdfplumber |

---

## Request/Response Examples

### Example 1: Complete Workflow

**Step 1**: Upload PDF
```bash
curl -X POST http://localhost:5000/upload-pdf \
  -F "file=@payslip.pdf" \
  -F "contract=SMSE-JASMINE"
```

**Step 2**: Search for payslip
```bash
curl "http://localhost:5000/search-payslip?employee_id=EMP001&month=March&year=2026"
```

**Step 3**: Download as PDF
```bash
curl -X POST http://localhost:5000/generate-payslip-pdf \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"EMP001","employee_name":"John Doe","month":"March","year":"2026","basic_salary":50000,"hra":10000,"allowances":5000,"deductions":5000,"net_salary":60000}' \
  --output payslip_download.pdf
```

### Example 2: JavaScript Fetch

```javascript
// Upload PDF
const formData = new FormData();
formData.append('file', file);
formData.append('contract', 'SMSE-JASMINE');

fetch('http://localhost:5000/upload-pdf', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));

// Search payslip
fetch('http://localhost:5000/search-payslip?employee_id=EMP001&month=March&year=2026')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Example 3: Python Requests

```python
import requests

# Upload PDF
files = {'file': open('payslip.pdf', 'rb')}
data = {'contract': 'SMSE-JASMINE'}
response = requests.post('http://localhost:5000/upload-pdf', files=files, data=data)
print(response.json())

# Search payslip
params = {
    'employee_id': 'EMP001',
    'month': 'March',
    'year': '2026'
}
response = requests.get('http://localhost:5000/search-payslip', params=params)
print(response.json())
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- Rate limiting by IP address
- User-based rate limiting
- API key-based rate limiting

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:*`
- `http://127.0.0.1:*`
- Any origin (configurable in production)

---

## Data Validation

### Employee ID
- Format: Text, alphanumeric
- Min Length: 1
- Max Length: 50

### Month
Valid values: January, February, March, April, May, June, July, August, September, October, November, December

### Year
Format: YYYY (e.g., 2026)

### Salary Fields
- Type: Numeric (float)
- Min: 0
- Max: 999,999,999

---

## Changelog

### Version 1.0 (Current)
- Initial release
- Upload PDF functionality
- Search payslip
- Generate PDF
- SQLite database

### Planned Features
- User authentication (v2.0)
- Advanced filtering (v2.0)
- Bulk operations (v2.0)
- Export to Excel (v2.0)
- Email notifications (v2.0)

---

## Support

For API issues or questions, contact the development team or check the main README.md file.
