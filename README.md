# Student Academic Hub with Abroad Education and Career Recommendation System

A full-stack web application designed to guide students through a continuous 10-module pipeline for abroad education and career preparation.

## Features
- **10-Module Pipeline**: Profile -> Academics -> Skills -> University -> Course -> Visa -> Accommodation -> Jobs -> Career -> Final Report.
- **Strict Sequential Flow**: Progress is saved, and modules must be completed in order.
- **Smart Recommendations**: Universities filtered by CGPA/Budget; Courses, Accommodation, and Jobs filtered by selected university.
- **Modern UI**: Professional purple theme (#6C5CE7) with responsive design.
- **Admin Panel**: Manage students and university data.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python (Flask)
- **Database**: MySQL

## Setup Instructions

### 1. Database Setup
1. Open your MySQL client (e.g., XAMPP, MySQL Workbench).
2. Run the SQL commands in `database.sql` to create the schema and insert sample data.
   - Database name: `student_hub`
   - Default user: `root` (no password)

### 2. Python Environment
1. Install dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```

### 3. Run the Application
1. Execute the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`

### 4. Default Accounts
- **Admin**: `admin` / `admin123`
- **Student**: Register a new account on the landing page.

## Module Overview
1. **Student Profile**: Basic personal info.
2. **Academic Details**: Marks, CGPA, Degree.
3. **Skills**: Tech & Soft skills input.
4. **University Recommendation**: Filtered by CGPA and Budget.
5. **Course Recommendation**: Selection from courses at the chosen uni.
6. **Visa & Application**: Step-by-step guidance.
7. **Accommodation**: Hostel/PG details with distance & facilities.
8. **Part-Time Jobs**: Job types and salary info near the uni.
9. **Career Preparation**: ATS Resume tips, LinkedIn/GitHub setup.
10. **Final Report**: Aggregate summary with Print/PDF option.
