"""
Database Initialize Script
Run this script to create and populate the database with sample data
"""

import sqlite3
import os

DATABASE_FOLDER = 'database'
DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'payslip.db')

# Create database folder if it doesn't exist
os.makedirs(DATABASE_FOLDER, exist_ok=True)

def init_database():
    """Initialize database with tables"""
    conn = sqlite3.connect(DATABASE_PATH)
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

    # Insert sample data
    sample_data = [
        ('EMP001', 'John Doe', 'SMSE-JASMINE', 'March', '2026', 50000, 10000, 5000, 5000, 60000),
        ('EMP002', 'Jane Smith', 'SMSE-JASMINE', 'March', '2026', 55000, 11000, 5500, 6000, 65500),
        ('EMP003', 'Michael Johnson', 'SMSE-ROSE', 'March', '2026', 60000, 12000, 6000, 7000, 71000),
        ('EMP001', 'John Doe', 'SMSE-JASMINE', 'February', '2026', 50000, 10000, 5000, 5000, 60000),
        ('EMP002', 'Jane Smith', 'SMSE-JASMINE', 'February', '2026', 55000, 11000, 5500, 6000, 65500),
        ('EMP001', 'John Doe', 'SMSE-JASMINE', 'January', '2026', 50000, 10000, 5000, 5000, 60000),
    ]

    for data in sample_data:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO payslips 
                (employee_id, employee_name, contract, month, year, basic_salary, hra, allowances, deductions, net_salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    print("Database initialized successfully!")
    print(f"Database location: {os.path.abspath(DATABASE_PATH)}")

if __name__ == '__main__':
    init_database()
