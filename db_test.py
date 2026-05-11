import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yuva123',
    'database': 'student_academic_hub'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("SUCCESS: Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"TABLES FOUND: {tables}")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
