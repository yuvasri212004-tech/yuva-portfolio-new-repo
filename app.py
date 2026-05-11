from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secret_student_hub_key'

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yuva123',
    'database': 'student_academic_hub'
}

def get_db_connection():
    try:
        # Try to connect with the database
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"DATABASE ERROR: {err}")
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database 'student_hub' not found. Attempting to create it...")
            try:
                temp_config = db_config.copy()
                temp_config.pop('database')
                temp_conn = mysql.connector.connect(**temp_config)
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
                temp_cursor.close()
                temp_conn.close()
                
                # Now connect to the new database
                conn = mysql.connector.connect(**db_config)
                return conn
            except mysql.connector.Error as create_err:
                print(f"CRITICAL: Failed to create database: {create_err}")
                return None
        elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("CRITICAL: Access denied. Check your username and password.")
        elif err.errno == 2003:
            print("CRITICAL: Can't connect to MySQL server. IS YOUR MYSQL SERVER RUNNING?")
        return None

# --- AUTH ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed.', 'danger')
            return render_template('login.html')
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and (user['password'] == password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                
                cursor.close()
                conn.close()
                flash('Login successful!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                cursor.close()
                conn.close()
                flash('Invalid email or password', 'danger')
        except Exception as e:
            if conn: conn.close()
            flash(f'An error occurred: {str(e)}', 'danger')
            
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed.', 'danger')
            return render_template('admin_login.html')
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND role = 'admin'", (username,))
            user = cursor.fetchone()
            
            if user and (user['password'] == password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                
                cursor.close()
                conn.close()
                flash('Admin Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                cursor.close()
                conn.close()
                flash('Invalid admin credentials', 'danger')
        except Exception as e:
            if conn: conn.close()
            flash(f'An error occurred: {str(e)}', 'danger')
            
    return render_template('admin_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        
        # Backend Validation
        if not email.endswith('@gmail.com'):
            flash('Only Gmail addresses are allowed', 'danger')
            return render_template('register.html')
        
        if not (mobile.isdigit() and len(mobile) == 10):
            flash('Enter valid 10-digit mobile number', 'danger')
            return render_template('register.html')

        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed.', 'danger')
            return render_template('register.html')
            
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, mobile, password) VALUES (%s, %s, %s, %s)", (username, email, mobile, password))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration was successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            if conn: conn.close()
            flash('Username, Email, or Mobile already exists', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- STUDENT PIPELINE ---

def get_progress(user_id):
    conn = get_db_connection()
    if conn is None:
        return {'current_module': 1} # Fallback
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_progress WHERE user_id = %s", (user_id,))
        progress = cursor.fetchone()
        if not progress:
            cursor.execute("INSERT INTO user_progress (user_id, current_module) VALUES (%s, 1)", (user_id,))
            conn.commit()
            cursor.execute("SELECT * FROM user_progress WHERE user_id = %s", (user_id,))
            progress = cursor.fetchone()
        cursor.close()
        conn.close()
        return progress
    except Exception as e:
        if conn: conn.close()
        return {'current_module': 1}

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    progress = get_progress(session['user_id'])
    return render_template('student/dashboard.html', progress=progress)

@app.route('/student/module/<int:mod_id>', methods=['GET', 'POST'])
def module_handler(mod_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    user_id = session['user_id']
    progress = get_progress(user_id)
    
    if mod_id > progress['current_module']:
        flash("Please complete previous modules first!", "warning")
        return redirect(url_for('module_handler', mod_id=progress['current_module']))

    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('student_dashboard'))
        
    try:
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            print(f"[DEBUG] Processing POST for Module {mod_id} (User: {user_id})")
            
            if mod_id == 1:
                name = request.form['name']
                age = request.form['age']
                country = request.form['country']
                interest = request.form['interest']
                budget = request.form['budget']
                cursor.execute("REPLACE INTO student_profiles (user_id, name, age, country_pref, field_interest, budget) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (user_id, name, age, country, interest, budget))
            elif mod_id == 2:
                m10 = request.form['m10']
                m12 = request.form['m12']
                degree = request.form['degree']
                cgpa = request.form['cgpa']
                subjects = request.form['subjects']
                cursor.execute("REPLACE INTO academic_details (user_id, marks_10th, marks_12th, degree, cgpa, subjects) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (user_id, m10, m12, degree, cgpa, subjects))
            elif mod_id == 3:
                tech = request.form['tech']
                soft = request.form['soft']
                cursor.execute("REPLACE INTO skills (user_id, technical_skills, soft_skills) VALUES (%s, %s, %s)", 
                               (user_id, tech, soft))
            elif mod_id == 4:
                uni_id = request.form['uni_id']
                cursor.execute("UPDATE user_progress SET selected_uni_id = %s WHERE user_id = %s", (uni_id, user_id))
            elif mod_id == 5:
                course_id = request.form['course_id']
                cursor.execute("UPDATE user_progress SET selected_course_id = %s WHERE user_id = %s", (course_id, user_id))
            elif mod_id == 7:
                acc_id = request.form.get('acc_id')
                if acc_id:
                    cursor.execute("UPDATE user_progress SET selected_acc_id = %s WHERE user_id = %s", (acc_id, user_id))
            elif mod_id == 8:
                job_id = request.form.get('job_id')
                if job_id:
                    cursor.execute("UPDATE user_progress SET selected_job_id = %s WHERE user_id = %s", (job_id, user_id))
                
            next_mod = mod_id + 1 if mod_id < 10 else 10
            print(f"[DEBUG] Module {mod_id} completed. Updating current_module to {next_mod}")
            
            cursor.execute("UPDATE user_progress SET current_module = GREATEST(current_module, %s) WHERE user_id = %s", (next_mod, user_id))
            conn.commit()
            
            print(f"[DEBUG] Redirecting to Module {next_mod}")
            cursor.close()
            conn.close()
            return redirect(url_for('module_handler', mod_id=next_mod))

        data = {}
        if mod_id == 4:
            cursor.execute("SELECT cgpa FROM academic_details WHERE user_id = %s", (user_id,))
            acad = cursor.fetchone()
            student_cgpa = acad['cgpa'] if acad else 0
            cursor.execute("SELECT country_pref, budget FROM student_profiles WHERE user_id = %s", (user_id,))
            prof = cursor.fetchone()
            country = prof['country_pref'] if prof else ''
            budget = prof['budget'] if prof else 0
            
            cursor.execute("""
                SELECT *, 
                (CASE WHEN country = %s THEN 40 ELSE 0 END + 
                 CASE WHEN min_cgpa <= %s THEN 30 ELSE 0 END +
                 CASE WHEN fees_per_year <= %s THEN 30 ELSE 0 END) as relevance
                FROM universities
                ORDER BY relevance DESC
            """, (country, student_cgpa, budget))
            unis = cursor.fetchall()
            
            # AI Logic: Add reasons and best match flag
            for i, uni in enumerate(unis):
                uni['best_match'] = (i == 0)
                reasons = []
                if uni['country'] == country: reasons.append(f"Located in your preferred country ({country}).")
                if uni['min_cgpa'] <= student_cgpa: reasons.append(f"Your CGPA ({student_cgpa}) exceeds requirement.")
                if uni['fees_per_year'] <= budget: reasons.append(f"Well within your annual budget (${budget}).")
                uni['reason'] = " ".join(reasons) if reasons else "Good general match based on reputation."
                
            data['universities'] = unis[:3] # Show 1 Best + 2 Alternatives
            
        elif mod_id == 5:
            uni_id = progress['selected_uni_id']
            cursor.execute("SELECT * FROM courses WHERE university_id = %s", (uni_id,))
            data['courses'] = cursor.fetchall()

        elif mod_id == 7:
            uni_id = progress['selected_uni_id']
            cursor.execute("SELECT * FROM accommodations WHERE university_id = %s", (uni_id,))
            data['accommodations'] = cursor.fetchall()

        elif mod_id == 8:
            uni_id = progress['selected_uni_id']
            cursor.execute("SELECT * FROM part_time_jobs WHERE university_id = %s", (uni_id,))
            data['jobs'] = cursor.fetchall()

        elif mod_id == 10:
            cursor.execute("""
                SELECT p.*, a.*, s.*, 
                       u.name as uni_name, u.location as uni_loc, u.fees_per_year as uni_fees,
                       c.course_name, c.duration as course_dur, c.fees as course_total_fees,
                       acc.name as acc_name, acc.type as acc_type, acc.address as acc_addr, acc.contact_info as acc_contact, acc.maps_link as acc_maps,
                       j.job_role, j.job_type, j.salary_range, j.location as job_loc, j.website_link as comp_site, j.careers_page as comp_careers, j.contact_email as comp_email
                FROM users usr
                LEFT JOIN student_profiles p ON usr.id = p.user_id
                LEFT JOIN academic_details a ON usr.id = a.user_id
                LEFT JOIN skills s ON usr.id = s.user_id
                LEFT JOIN user_progress up ON usr.id = up.user_id
                LEFT JOIN universities u ON up.selected_uni_id = u.id
                LEFT JOIN courses c ON up.selected_course_id = c.id
                LEFT JOIN accommodations acc ON up.selected_acc_id = acc.id
                LEFT JOIN part_time_jobs j ON up.selected_job_id = j.id
                WHERE usr.id = %s
            """, (user_id,))
            report = cursor.fetchone()
            
            # AI Logic: Structural Suggestions for Future
            suggestions = []
            if 'Python' in (report['technical_skills'] or ''):
                suggestions.append("Given your Python skills, focus on Data Science or Backend roles in your target country.")
            if len(report['soft_skills'] or '') < 10:
                suggestions.append("Consider improving soft skills (Communication, Leadership) to boost your visa/interview success.")
            else:
                suggestions.append("Your strong soft skills will be a major asset for networking in international markets.")
            
            report['future_suggestions'] = suggestions
            data['report'] = report

        cursor.close()
        conn.close()
        return render_template(f'student/module{mod_id}.html', progress=progress, data=data)
    except Exception as e:
        if conn: conn.close()
        print(f"[ERROR] Module {mod_id} failed: {e}")
        flash(f"System Error: {e}", "danger")
        # Try to recover by staying on current module if possible
        return redirect(url_for('module_handler', mod_id=mod_id))

# --- ADMIN ROUTES ---

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('student_dashboard'))
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT u.username, u.email, p.name, p.country_pref, up.current_module FROM users u JOIN user_progress up ON u.id = up.user_id LEFT JOIN student_profiles p ON u.id = p.user_id WHERE u.role = 'student'")
        students = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) as count FROM universities")
        uni_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM courses")
        course_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM accommodations")
        acc_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM part_time_jobs")
        job_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT * FROM universities")
        unis = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin/dashboard.html', 
                               students=students, 
                               universities=unis,
                               stats={
                                   'users': len(students),
                                   'unis': uni_count,
                                   'courses': course_count,
                                   'acc': acc_count,
                                   'jobs': job_count
                               })
    except Exception as e:
        if conn: conn.close()
        flash(f"Admin DB Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/admin/add_uni', methods=['POST'])
def add_uni():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    name = request.form['name']
    location = request.form['location']
    country = request.form['country']
    fees = request.form['fees']
    cgpa = request.form['cgpa']
    desc = request.form['desc']
    
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO universities (name, location, country, fees_per_year, min_cgpa, description) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (name, location, country, fees, cgpa, desc))
        conn.commit()
        cursor.close()
        conn.close()
        flash('University added successfully!', 'success')
    except Exception as e:
        if conn: conn.close()
        flash(f"Error adding university: {e}", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_course', methods=['POST'])
def add_course():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    uni_id = request.form['uni_id']
    name = request.form['name']
    duration = request.form['duration']
    fees = request.form['fees']
    
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (university_id, course_name, duration, fees) VALUES (%s, %s, %s, %s)", (uni_id, name, duration, fees))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Course added successfully!', 'success')
    except Exception as e:
        if conn: conn.close()
        flash(f"Error adding course: {e}", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_acc', methods=['POST'])
def add_acc():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    uni_id = request.form['uni_id']
    name = request.form['name']
    acc_type = request.form['type']
    dist = request.form['dist']
    addr = request.form['addr']
    contact = request.form['contact']
    maps = request.form['maps']
    fees = request.form.get('fees', 0)
    transport = request.form.get('transport', 'Not specified')
    facilities = request.form.get('facilities', 'Standard facilities')
    needs = request.form.get('needs', 'Shops nearby')
    
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accommodations (university_id, name, type, distance_from_uni, address, contact_info, maps_link, fees_per_month, transport_availability, facilities, daily_needs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (uni_id, name, acc_type, dist, addr, contact, maps, fees, transport, facilities, needs))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Accommodation added successfully!', 'success')
    except Exception as e:
        if conn: conn.close()
        flash(f"Error adding accommodation: {e}", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_job', methods=['POST'])
def add_job():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    uni_id = request.form['uni_id']
    role = request.form['role']
    site = request.form.get('site')
    careers = request.form.get('careers')
    email = request.form.get('email')
    job_type = request.form.get('type', 'Part-time')
    salary = request.form.get('salary', 'Competitive')
    loc = request.form.get('location', 'Nearby')
    
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed.", "danger")
        return redirect(url_for('admin_dashboard'))
        
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO part_time_jobs (university_id, job_role, website_link, careers_page, contact_email, job_type, salary_range, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (uni_id, role, site, careers, email, job_type, salary, loc))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Career recommendation added!', 'success')
    except Exception as e:
        if conn: conn.close()
        flash(f"Error adding career: {e}", "danger")
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
