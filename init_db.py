import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yuva123'
}

def run_sql_file(filename):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        with open(filename, 'r') as f:
            sql_script = f.read()
            
        # Split script into individual commands
        commands = sql_script.split(';')
        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error executing command: {e}")
                    
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize database: {e}")

if __name__ == "__main__":
    run_sql_file('database.sql')
