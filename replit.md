# AI-Enhanced E-Learning Analytics System

## Overview

This is a machine learning-powered e-learning platform built with Flask that predicts student performance based on engagement metrics. The system analyzes attendance, quiz scores, assignment completion, study hours, internet connectivity, and participation levels to forecast academic outcomes using Random Forest and Decision Tree classifiers.

The platform serves three user roles (Admin, Teacher, Student) with role-based access control, providing interactive dashboards, real-time analytics, PDF report generation, and performance predictions with confidence scores.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework & Routing
- **Flask-based MVC architecture** with Blueprint-based route separation
- Modular route handlers for authentication, admin operations, student data, analytics, and reporting
- Session-based authentication with role-based access control (RBAC)
- CORS enabled for potential API consumption

### Database Layer
- **SQLite** for relational data storage with SQLAlchemy ORM
- Three primary models:
  - `User`: Stores user credentials with hashed passwords (Werkzeug), unique email/mobile constraints
  - `StudentData`: Contains student performance metrics and historical data
  - `PredictionHistory`: Tracks all ML predictions with timestamps and confidence scores
- Database migrations handled implicitly through SQLAlchemy's `create_all()`

### Machine Learning Pipeline
- **Preprocessing**: LabelEncoder for categorical features (Internet Connectivity, Participation), StandardScaler for numerical normalization, engineered "Engagement_Index" feature
- **Model Training**: Comparative training of Random Forest (100 trees, max_depth=10) vs Decision Tree (max_depth=8) with automatic best-model selection
- **Prediction**: Serialized model (pickle) with probability distribution for multi-class performance categories
- **Dataset**: Built-in CSV with 200+ synthetic student records for training

### Authentication & Validation
- Custom validators for email format (regex), mobile (10-digit numeric), password strength (8+ chars, uppercase, number)
- Unique credential enforcement at database and validation layers
- Default admin account seeded on first run (admin@elearning.com / Admin@123)

### Frontend Architecture
- Server-side rendered Jinja2 templates with Bootstrap 5 for responsive UI
- Chart.js for client-side data visualization (pie charts, bar graphs)
- Glassmorphism and gradient design patterns for modern aesthetics
- Client-side validation mirroring backend rules

### Reporting System
- **ReportLab** generates PDF performance reports with:
  - User prediction history (last 20 entries)
  - Performance distribution tables
  - Timestamp and metadata headers
- Reports stored in `/reports` directory with timestamped filenames

### Security Measures
- Password hashing with Werkzeug's PBKDF2-SHA256
- Session-based authentication with decorator-protected routes
- CSRF protection through Flask's session management
- Secret key configurable via environment variable

### Design Patterns
- **Decorator pattern**: `@login_required` and `@admin_required` for route protection
- **Factory pattern**: `create_app()` for application instantiation
- **Repository pattern**: SQLAlchemy models abstract database operations

## External Dependencies

### Python Libraries
- **Flask 3.0.0**: Web framework and routing
- **Flask-SQLAlchemy 3.1.1**: ORM for database operations
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **Werkzeug 3.0.1**: Password hashing and security utilities
- **scikit-learn 1.3.2**: ML algorithms (Random Forest, Decision Tree, preprocessing)
- **pandas 2.1.4**: Data manipulation and CSV processing
- **NumPy 1.26.2**: Numerical computations
- **XGBoost 2.0.3**: Advanced gradient boosting (currently unused, available for future enhancement)
- **ReportLab 4.0.7**: PDF generation
- **Matplotlib 3.8.2**: Data visualization backend

### Frontend Libraries (CDN)
- **Bootstrap 5.3.0**: UI components and responsive grid
- **Chart.js**: Interactive charts for analytics dashboard
- **Google Fonts (Poppins)**: Typography

### Database
- **SQLite**: File-based relational database (no external server required)
- Database file location: `backend/database/e_learning.db`

### File Storage
- **CSV Dataset**: `backend/ml/student_data.csv` (200+ records for training)
- **Model Persistence**: `backend/ml/model.pkl` (serialized trained model)
- **Generated Reports**: `reports/` directory (PDF outputs)

### Development & Deployment
- **Dual-environment compatibility**: Works in both Replit and VS Code
- **Entry points**: 
  - `run.py` for main application (runs on port 5000)
  - `train_model_standalone.py` for ML model training
- **Import strategy**: Relative imports for module files, absolute imports via sys.path for entry points
- Session secret configurable via `SESSION_SECRET` environment variable
- Static file serving through Flask's built-in development server

## Recent Changes (November 16, 2025)

### VS Code Compatibility Fix
- Fixed `ModuleNotFoundError: No module named 'backend'` error for VS Code deployment
- Changed all internal imports from absolute (`from backend.ml.preprocessing`) to relative (`from .preprocessing`)
- Created `run.py` as application entry point (replaces direct `python backend/app.py` execution)
- Created `train_model_standalone.py` for standalone ML model training
- Updated README.md with corrected VS Code deployment instructions
- Database path now uses absolute paths to work across different execution contexts