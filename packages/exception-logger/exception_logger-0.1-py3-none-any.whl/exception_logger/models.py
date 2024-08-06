import mysql.connector
from config import db_config

# Establish database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the ExceptionLog table
query = """
CREATE TABLE IF NOT EXISTS ExceptionLog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    stack_trace TEXT NOT NULL,
    timestamp DATETIME NOT NULL
)
"""
cursor.execute(query)

cursor.close()
conn.close()
