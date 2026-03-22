"""
Configuration file for the Flask application
"""

import os
from datetime import timedelta

# Flask Configuration
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Database Configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'payslip.db')
DATABASE_FOLDER = os.path.join(os.path.dirname(__file__), 'database')

# Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf'}

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost:*',
    'http://127.0.0.1:*',
    'http://localhost:3000',
    'http://localhost:5000',
    'http://localhost:8000',
]

# Security Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'salt')

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'logs/payslip_portal.log'

# PDF Processing Configuration
PDF_EXTRACTION_TIMEOUT = 30  # seconds
PDF_PROCESSING_BATCH_SIZE = 10

# API Configuration
API_TIMEOUT = 60  # seconds
API_VERSION = 'v1'

# Pagination
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500

# Feature Flags
ENABLE_PDF_UPLOAD = True
ENABLE_PDF_DOWNLOAD = True
ENABLE_SEARCH = True
ENABLE_ADMIN_PANEL = True
