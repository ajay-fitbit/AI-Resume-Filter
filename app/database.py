import mysql.connector
from mysql.connector import Error
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(**Config.DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a single query"""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

def fetch_query(connection, query, params=None):
    """Fetch results from a query"""
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()

def setup_database():
    """Setup database and tables"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=Config.DB_CONFIG['host'],
            user=Config.DB_CONFIG['user'],
            password=Config.DB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        
        # Read and execute schema file
        with open('database_schema.sql', 'r') as f:
            sql_script = f.read()
        
        # Execute each statement separately
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print("Database setup completed successfully!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
