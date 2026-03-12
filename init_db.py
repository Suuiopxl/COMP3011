import pandas as pd
import sqlite3
import os

def setup_database():
    """
    Reads data from a CSV file, performs basic cleaning, 
    and imports it into an SQLite database.
    """
    csv_file_path = "gaming_laptops_2026_q1.csv"
    db_file_path = "laptops.db"

    print(f"Loading data from {csv_file_path}...")
    
    # Load the CSV file into a pandas DataFrame
    # Using pandas simplifies the process of handling CSV to SQL conversion
    df = pd.read_csv(csv_file_path)

    # Data Cleaning: Handle missing values (NaN) to prevent database constraints errors
    # We fill numeric columns with 0 and text columns with a placeholder string
    print("Cleaning missing values...")
    df.fillna(value={
        "list_price": 0.0, 
        "stars": 0.0, 
        "breadCrumbs": "Unknown", 
        "description": "No description available"
    }, inplace=True)

    print(f"Connecting to SQLite database '{db_file_path}'...")
    # Connect to the SQLite database. It will create the file if it does not exist.
    conn = sqlite3.connect(db_file_path)

    # Write the records stored in the DataFrame to a SQL database
    # 'if_exists="replace"' will drop the table if it already exists and recreate it
    # 'index_label="id"' automatically generates an auto-incrementing primary key column named 'id'
    print("Writing data to the 'laptops' table...")
    df.to_sql("laptops", conn, if_exists="replace", index_label="id")

    # Commit the transaction and close the database connection
    conn.commit()
    conn.close()

    print("Database initialization completed successfully! The 'laptops.db' file is ready.")

if __name__ == "__main__":
    setup_database()