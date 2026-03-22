# Quick Start Guide - Online Payslip Portal

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.7+ installed
- Modern web browser
- Terminal/Command Prompt access

### Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py
```

**Expected Output:**
```
Database initialized successfully!
Database location: /path/to/database/payslip.db
```

### Step 2: Start Backend Server

```bash
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
```

Leave this running and open a new terminal for frontend.

### Step 3: Start Frontend

```bash
cd frontend
python -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Step 4: Access Application

Open your browser and go to:
```
http://localhost:8000
```

### ✅ Test It Out

**Test Search:**
1. Contract: Select "SMSE-JASMINE"
2. Month: Select "March"
3. Year: Select "2026"
4. Employee ID: Enter `EMP001`
5. Click "Search Payslip"

**Expected Result:**
```
Employee Name: John Doe
Basic Salary: ₹ 50,000.00
HRA: ₹ 10,000.00
Allowances: ₹ 5,000.00
Deductions: ₹ 5,000.00
Net Salary: ₹ 60,000.00
```

### 📄 Test PDF Upload (Admin Panel)

1. Click "Admin Panel" link
2. Create a sample PDF:
   ```bash
   cd backend
   python create_sample_pdf.py
   ```
3. Upload `sample_payslip.pdf` from admin panel
4. Confirm success message

---

## 📋 API Health Check

```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

## 🗄️ Database

Sample data already loaded:
- **EMP001** - John Doe
- **EMP002** - Jane Smith
- **EMP003** - Michael Johnson

All for March 2026, SMSE-JASMINE contract.

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Main Flask application |
| `backend/init_db.py` | Database setup script |
| `frontend/index.html` | Main portal page |
| `frontend/admin.html` | Admin upload page |
| `frontend/script.js` | Frontend logic |

---

## 🔧 Troubleshooting

### "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### "Module not found" error
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### "PDF library not installed"
```bash
pip install PyMuPDF reportlab pdfplumber
```

### CORS error in browser console
- Ensure backend is running on http://localhost:5000
- Check `API_BASE_URL` in `frontend/script.js` is correct

---

## 📚 Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production deployment

---

## 💡 Quick Tips

- Use sample data to test before uploading your own PDFs
- Admin panel is at `/admin.html`
- All data is stored in `backend/database/payslip.db`
- PDFs are saved in `backend/uploads/`
- To reset database, delete `backend/database/payslip.db` and run `python init_db.py`

---

**Powered by PAVI TECH** ✨
