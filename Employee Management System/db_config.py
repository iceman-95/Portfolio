import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Force load the environment variables
load_dotenv(override=True)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': 'Mysql!995',  # Direct password for testing
    'database': os.getenv('DB_NAME', 'employee_management'),
    'auth_plugin': 'mysql_native_password'
}

def initialize_database():
    """Initialize the database using the SQL file"""
    try:
        # First, create connection without database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password='Mysql!995',  # Direct password for testing
            auth_plugin='mysql_native_password'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute the SQL file
            with open('employee_management.sql', 'r') as sql_file:
                # Split the file into individual statements
                sql_commands = sql_file.read().split(';')
                
                # Execute each statement
                for command in sql_commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                            connection.commit()
                        except Error as e:
                            print(f"Error executing command: {e}")
                            print(f"Command was: {command}")
            
            print("Database initialized successfully!")
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Error initializing database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def create_connection():
    """Create a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password='Mysql!995',  # Direct password for testing
            database=os.getenv('DB_NAME', 'employee_management'),
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a query and return the results"""
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()
            return cursor.rowcount
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def call_stored_procedure(connection, procedure_name, params=None):
    """Call a stored procedure and return the results"""
    try:
        cursor = connection.cursor()
        if params:
            cursor.callproc(procedure_name, params)
        else:
            cursor.callproc(procedure_name)
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        
        return results
    except Error as e:
        print(f"Error calling stored procedure: {e}")
        return None
    finally:
        cursor.close()

def get_employee_summary():
    """Get employee summary using the view"""
    connection = create_connection()
    if connection:
        try:
            results = execute_query(connection, "SELECT * FROM employee_summary")
            return results
        finally:
            connection.close()
    return None

def promote_employee_db(employee_id, new_position, new_salary):
    """Promote an employee using the stored procedure"""
    connection = create_connection()
    if connection:
        try:
            call_stored_procedure(connection, 'promote_employee', 
                                [employee_id, new_position, new_salary])
            return True
        finally:
            connection.close()
    return False

def search_employees_db(search_term):
    """Search employees using the stored procedure"""
    connection = create_connection()
    if connection:
        try:
            results = call_stored_procedure(connection, 'search_employees', [search_term])
            return results
        finally:
            connection.close()
    return None

# Initialize the database when the module is imported
if __name__ == "__main__":
    initialize_database() 