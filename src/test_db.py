import sqlite3
import os

print(f"Current directory: {os.getcwd()}")
print(f"Can write to current directory: {os.access('.', os.W_OK)}")

try:
    conn = sqlite3.connect('test.db')
    print("Successfully created test database!")
    conn.close()
    os.remove('test.db')  # Clean up
except Exception as e:
    print(f"Error: {str(e)}")