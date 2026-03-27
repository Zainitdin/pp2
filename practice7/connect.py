# Import the get_connection function from our connect.py file
# This function handles connecting to the PostgreSQL database using psycopg2
from connect import get_connection

# Step 1: Call the function to establish a connection
# It will return a connection object if successful, or None if it fails
conn = get_connection()

# Step 2: Check if the connection was successful
if conn:
    # ✅ If we reach here, the connection to the database was successful
    print("Connection test successful!")

    # Step 3: Close the connection
    # Closing the connection is important to free resources
    conn.close()
    # After closing, the database connection is properly terminated

else:
    # ❌ If we reach here, the connection failed
    # Could be due to wrong credentials, database not running, or server issues
    print("Connection test failed.")