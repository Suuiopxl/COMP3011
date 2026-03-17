import pandas as pd
import sqlite3

def setup_database():
    print("Loading and cleaning data from CSV...")
    df = pd.read_csv("gaming_laptops_2026_q1.csv")
    df.fillna(value={
        "list_price": 0.0, 
        "stars": 0.0, 
        "breadCrumbs": "Unknown", 
        "description": "No description available"
    }, inplace=True)

    print("Connecting to SQLite database 'laptops.db'...")
    conn = sqlite3.connect("laptops.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS laptops")

    cursor.execute('''
        CREATE TABLE laptops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            brand TEXT,
            price REAL,
            list_price REAL,
            discount_pct REAL,
            price_currency TEXT,
            stars REAL,
            reviews_count INTEGER,
            breadCrumbs TEXT,
            description TEXT
        )
    ''')

    print("Writing data to the 'laptops' table...")
    df.to_sql("laptops", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print("Database initialization completed successfully!")

if __name__ == "__main__":
    setup_database()