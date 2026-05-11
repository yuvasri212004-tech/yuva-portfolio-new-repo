-- Clean up existing tables to ensure new schema works
DROP DATABASE IF EXISTS student_academic_hub;
CREATE DATABASE student_academic_hub;
USE student_academic_hub;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile VARCHAR(15),
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student Profiles (Module 1)
CREATE TABLE student_profiles (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    country_pref VARCHAR(100),
    field_interest VARCHAR(100),
    budget DECIMAL(12, 2),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Academic Details (Module 2)
CREATE TABLE academic_details (
    user_id INT PRIMARY KEY,
    marks_10th FLOAT,
    marks_12th FLOAT,
    degree VARCHAR(100),
    cgpa FLOAT,
    subjects TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Skills (Module 3)
CREATE TABLE skills (
    user_id INT PRIMARY KEY,
    technical_skills TEXT,
    soft_skills TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Universities Data
CREATE TABLE universities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    country VARCHAR(100),
    fees_per_year DECIMAL(12, 2),
    min_cgpa FLOAT,
    description TEXT
);

-- Courses Data
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT,
    course_name VARCHAR(255),
    duration VARCHAR(50),
    fees DECIMAL(12, 2),
    FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
);

-- Accommodations Data
CREATE TABLE accommodations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT,
    name VARCHAR(255),
    type ENUM('Hostel', 'PG'),
    distance_from_uni VARCHAR(50),
    transport_availability VARCHAR(100),
    facilities TEXT,
    daily_needs TEXT,
    address TEXT,
    contact_info VARCHAR(100),
    maps_link TEXT,
    fees_per_month DECIMAL(12, 2),
    FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
);

-- Part-Time Jobs
CREATE TABLE part_time_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT,
    job_role VARCHAR(255),
    job_type VARCHAR(100),
    salary_range VARCHAR(100),
    location VARCHAR(255),
    website_link TEXT,
    careers_page TEXT,
    contact_email VARCHAR(100),
    FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
);

-- Progress & Selection Tracking
CREATE TABLE user_progress (
    user_id INT PRIMARY KEY,
    current_module INT DEFAULT 1,
    selected_uni_id INT,
    selected_course_id INT,
    selected_acc_id INT,
    selected_job_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (selected_uni_id) REFERENCES universities(id),
    FOREIGN KEY (selected_course_id) REFERENCES courses(id),
    FOREIGN KEY (selected_acc_id) REFERENCES accommodations(id),
    FOREIGN KEY (selected_job_id) REFERENCES part_time_jobs(id)
);

-- Insert Sample Admin
INSERT INTO users (username, email, password, role) VALUES ('admin', 'admin@studenthub.com', 'admin123', 'admin');

-- Insert Sample Data for Universities
INSERT INTO universities (name, location, country, fees_per_year, min_cgpa, description) VALUES
('Oxford University', 'Oxford', 'UK', 30000, 8.5, 'One of the oldest and most prestigious universities.'),
('Stanford University', 'California', 'USA', 50000, 9.0, 'Leading research university in the heart of Silicon Valley.'),
('University of Toronto', 'Toronto', 'Canada', 25000, 7.5, 'Top-ranked public university in Canada.'),
('Technical University of Munich', 'Munich', 'Germany', 1500, 8.0, 'Leading technical university in Europe with low tuition fees.'),
('Melbourne University', 'Melbourne', 'Australia', 35000, 7.0, 'Prestigious research institution in Australia.');

-- Insert Sample Courses
INSERT INTO courses (university_id, course_name, duration, fees) VALUES
(1, 'Computer Science', '3 Years', 30000),
(1, 'Data Science', '1 Year', 32000),
(2, 'Software Engineering', '2 Years', 50000),
(3, 'Artificial Intelligence', '2 Years', 25000),
(4, 'Automotive Engineering', '2 Years', 1500),
(5, 'Business Analytics', '1.5 Years', 35000);

-- Insert Sample Accommodations with FIXED LINKS
INSERT INTO accommodations (university_id, name, type, distance_from_uni, transport_availability, facilities, daily_needs, address, contact_info, maps_link, fees_per_month) VALUES
(1, 'Oxford Student Hall', 'Hostel', '0.5 km', 'Walking/Bicycle', 'WiFi, Laundry, Mess, Gym', 'Supermarket: 200m, Pharmacy: 100m, ATM: On-site', 'High St, Oxford OX1 4BG, UK', '+44 1865 270000', 'https://www.google.com/maps?q=Oxford+Student+Hall+UK', 800),
(1, 'City View PG', 'PG', '2.0 km', 'Bus/Train', 'Kitchen, WiFi, Security', 'Convenience Store: 50m, Bus Stop: 100m', 'Cowley Rd, Oxford OX4 1HP, UK', '+44 1865 123456', 'https://www.google.com/maps?q=City+View+PG+Oxford', 600),
(2, 'Stanford Graduate Housing', 'Hostel', '0.2 km', 'Bicycle/Marguerite Shuttle', 'Fully furnished, high-speed internet, study lounges', 'Campus Store: 100m, Dining Hall: 50m', '450 Serra Mall, Stanford, CA 94305, USA', '+1 650-723-2300', 'https://www.google.com/maps?q=Stanford+Graduate+Housing', 1200),
(2, 'Palo Alto Student Suites', 'PG', '1.5 km', 'CalTrain/Bike', 'Private room, Shared kitchen, Laundry', 'Whole Foods: 400m, Coffee Shop: 100m', 'University Ave, Palo Alto, CA, USA', '+1 650-555-0199', 'https://www.google.com/maps?q=Palo+Alto+Student+Suites', 1500),
(3, 'Toronto University Residence', 'Hostel', '0.3 km', 'Subway/TTC', 'Meal plans, 24/7 security, Gym access', 'Subway Station: 200m, Eaton Centre: 1km', '27 King\'s College Cir, Toronto, ON M5S, Canada', '+1 416-978-2011', 'https://www.google.com/maps?q=University+of+Toronto+Residence', 900),
(4, 'Munich Tech Dorm', 'Hostel', '1.0 km', 'Tram/U-Bahn', 'High-speed internet, Common kitchen', 'Grocery: 300m, Transport Hub: 400m', 'Arcisstr. 21, 80333 Munich, Germany', '+49 89 2890', 'https://www.google.com/maps?q=Technical+University+of+Munich+Dorm', 400),
(5, 'Melbourne Village', 'Hostel', '0.6 km', 'Tram Zone', 'Pool, Rooftop lounge, Study rooms', 'Queen Vic Market: 300m, Tram Stop: 50m', 'Grattan St, Parkville VIC 3010, Australia', '+61 3 9035 5511', 'https://www.google.com/maps?q=Melbourne+University+Village', 1100);

-- Insert Sample Jobs with FIXED LINKS
INSERT INTO part_time_jobs (university_id, job_role, job_type, salary_range, location, website_link, careers_page, contact_email) VALUES
(1, 'Library Assistant', 'Campus Job', '£10-15/hr', 'University Library', 'https://www.ox.ac.uk/library', 'https://www.ox.ac.uk/about/jobs', 'library-jobs@ox.ac.uk'),
(1, 'Delivery Rider', 'Off-Campus', '£12-18/hr', 'Oxford City Center', 'https://www.deliveroo.co.uk', 'https://deliveroo.co.uk/apply', 'support@deliveroo.com'),
(2, 'Lab Assistant', 'Research', '$18-25/hr', 'Stanford Science Park', 'https://www.stanford.edu', 'https://careersearch.stanford.edu/', 'lab-jobs@stanford.edu'),
(2, 'Campus Tour Guide', 'Student Life', '$16-20/hr', 'Visitor Center', 'https://visit.stanford.edu', 'https://visit.stanford.edu/tours/', 'tours@stanford.edu'),
(3, 'Tutor', 'Academic', '$20-30/hr', 'Student Success Centre', 'https://www.utoronto.ca', 'https://jobs.utoronto.ca/', 'tutor@utoronto.ca'),
(4, 'Research Assistant', 'Academic', '€12-16/hr', 'Campus Labs', 'https://www.tum.de/en/', 'https://www.tum.de/en/about-tum/working-at-tum/job-opportunities', 'hr@tum.de'),
(5, 'Cafe Staff', 'Service', '$22-28/hr', 'Lygon Street', 'https://www.unimelb.edu.au', 'https://about.unimelb.edu.au/careers', 'jobs@unimelb.edu.au');
