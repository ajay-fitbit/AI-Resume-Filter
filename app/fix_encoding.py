import mysql.connector
from mysql.connector import Error
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def fix_database_encoding():
    """Fix database encoding to support UTF8MB4"""
    try:
        # Connect to database
        connection = mysql.connector.connect(**Config.DB_CONFIG)
        cursor = connection.cursor()
        
        print("Converting database to UTF8MB4...")
        
        # Convert database
        cursor.execute("ALTER DATABASE resume_filter_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        # Convert tables
        tables = ['job_descriptions', 'candidates', 'resume_data', 'analysis_results', 'red_flags']
        
        for table in tables:
            print(f"Converting table: {table}")
            cursor.execute(f"ALTER TABLE {table} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        connection.commit()
        print("✓ Database encoding updated successfully!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error fixing database encoding: {e}")

if __name__ == "__main__":
    fix_database_encoding()
