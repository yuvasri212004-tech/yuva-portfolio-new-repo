# 🎓 AI-Enhanced E-Learning Analytics System

A machine learning-powered e-learning web platform that analyzes student interaction data and predicts learning performance using advanced ML algorithms.

## 📋 Features

- 🧠 **ML-Powered Performance Prediction** - Random Forest and Decision Tree models
- 📊 **Interactive Analytics Dashboard** - Real-time charts and visualizations
- 👥 **Multi-Role Access Control** - Admin, Teacher, and Student roles
- 🔒 **Secure Authentication** - Unique credential validation (email, mobile, password)
- 📝 **PDF Report Generation** - Comprehensive performance reports with ReportLab
- 📈 **Data Visualization** - Chart.js powered analytics
- 💾 **Dataset Management** - Built-in CSV with 200+ student records
- 🎨 **Modern UI/UX** - Gradient design with glassmorphism effects

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **ML Libraries:** scikit-learn, pandas, NumPy, XGBoost
- **Visualization:** Chart.js, Matplotlib
- **Reporting:** ReportLab
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

## 📁 Project Structure

```
e_learning_ml_system/
│
├── backend/
│   ├── app.py                      # Flask application factory
│   ├── models.py                   # Database models
│   ├── ml/
│   │   ├── student_data.csv        # Built-in dataset (200+ records)
│   │   ├── preprocessing.py        # Data preprocessing
│   │   ├── train_model.py          # Model training
│   │   ├── predict.py              # Prediction engine
│   │   └── model.pkl               # Trained ML model
│   ├── routes/
│   │   ├── auth_routes.py          # Authentication endpoints
│   │   ├── admin_routes.py         # Admin panel endpoints
│   │   ├── student_routes.py       # Student dashboard endpoints
│   │   ├── analytics_routes.py     # Analytics & prediction endpoints
│   │   └── report_routes.py        # Report generation endpoints
│   ├── utils/
│   │   ├── validators.py           # Credential validation
│   │   └── report_generator.py     # PDF report generation
│   ├── templates/                  # HTML templates
│   ├── static/                     # CSS, JS, images
│   └── database/                   # SQLite database
│
├── run.py                          # Application entry point
├── train_model_standalone.py       # Standalone ML training script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

## 🚀 Installation & Deployment in VS Code

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd path/to/your/project
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-CORS==4.0.0
- Werkzeug==3.0.1
- scikit-learn==1.3.2
- pandas==2.1.4
- numpy==1.26.2
- xgboost==2.0.3
- reportlab==4.0.7
- matplotlib==3.8.2

### Step 4: Train the ML Model (First Time Only)

```bash
python train_model_standalone.py
```

This creates the `model.pkl` file with trained Random Forest/Decision Tree models (100% accuracy on the built-in dataset).

### Step 5: Run the Application

```bash
python run.py
```

The application will start on: **http://127.0.0.1:5000**

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 🔑 Default Admin Credentials

**Email:** admin@elearning.com  
**Password:** Admin@123  
**Mobile:** 9999999999

Use these credentials to log in as an administrator.

## 👥 User Roles

### Admin
- Manage users (create, view, delete)
- Upload datasets (CSV files)
- View system statistics
- Full access to all features

### Teacher
- Make student performance predictions
- View analytics and charts
- Access feature importance data
- Generate PDF reports

### Student
- View personal predictions
- Access dashboard with statistics
- See prediction history
- Download performance reports

## 📊 Making Predictions

1. **Login** as Admin or Teacher
2. Navigate to **Analytics** page
3. Fill in the prediction form:
   - Student Name
   - Attendance (%)
   - Quiz Score (0-100)
   - Assignment Score (0-100)
   - Study Hours (per week)
   - Internet Connectivity (Yes/No)
   - Participation Level (Active/Moderate/Low)
4. Click **Predict Performance**
5. View results with confidence percentage

## 📝 Generating Reports

1. Go to **Analytics** page
2. Click **Download PDF Report**
3. PDF will be generated with:
   - Recent predictions
   - Performance distribution
   - Recommendations

## 📤 Uploading Custom Datasets

**Admin Only:**

1. Login as Admin
2. Go to **Admin Panel**
3. Use **Upload Dataset** section
4. Select CSV file with required columns:
   - Student_ID
   - Attendance
   - Quiz_Score
   - Assignment_Score
   - Study_Hours
   - Internet_Connectivity
   - Participation
   - Final_Score
   - Performance_Level

## 🔧 Troubleshooting

### Issue: Module Not Found Error
**Solution:** Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database Not Found
**Solution:** The database is created automatically on first run. If you see errors:
```bash
rm -rf backend/database/e_learning.db
python backend/app.py
```

### Issue: Model Not Found
**Solution:** Train the model:
```bash
cd backend/ml
python train_model.py
cd ../..
```

### Issue: Port Already in Use
**Solution:** Change the port in `backend/app.py`:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

### Issue: Import Errors
**Solution:** Make sure you're running from the project root directory:
```bash
python backend/app.py
```

## 🎨 UI Color Scheme

- **Primary Color:** #4E73DF (Royal Blue)
- **Accent Color:** #F6C23E (Amber Yellow)
- **Background:** #F0F4F8 (Soft Cool Gray)
- **Highlight:** #1CC88A (Mint Green)

## 📈 Dataset Information

The built-in dataset contains 200 student records with:
- Attendance percentages
- Quiz and assignment scores
- Study hours per week
- Internet connectivity status
- Participation levels
- Final scores and performance classifications

**Performance Levels:**
- Excellent (90-100%)
- Good (70-89%)
- Average (50-69%)
- Poor (0-49%)

## 🔐 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Unique credential validation
- Role-based access control
- CORS protection

## 🧪 Testing the Application

1. **Register a new user:**
   - Go to http://127.0.0.1:5000/register
   - Fill in all required fields
   - Select role (Student/Teacher)

2. **Login:**
   - Use your credentials or default admin
   - You'll be redirected to the dashboard

3. **Make a prediction:**
   - Go to Analytics page
   - Enter student data
   - View ML prediction results

4. **Generate report:**
   - Click "Download PDF Report"
   - Check the reports/ folder

## 📞 Support

For issues or questions:
- Check the Troubleshooting section above
- Review error logs in the console
- Ensure all dependencies are correctly installed

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ using Flask, Machine Learning, and Modern Web Technologies**
