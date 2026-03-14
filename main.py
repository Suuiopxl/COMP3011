from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
from typing import List

# Initialize the FastAPI application with metadata for the auto-generated documentation
app = FastAPI(
    title="2026 Q1 Gaming Laptops Market API",
    description="A RESTful API for querying and managing gaming laptop market data. Built with FastAPI and SQLite.",
    version="1.0.0"
)

# Define Pydantic models for data validation and parsing
# This ensures that any data sent to our API strictly follows this structure
class LaptopBase(BaseModel):
    title: str
    brand: str
    price: float
    discount_pct: float = 0.0
    price_currency: str = "$"
    stars: float = 0.0
    reviews_count: int = 0

class LaptopResponse(LaptopBase):
    id: int # The response will always include the database-generated ID

# Helper function to establish a database connection
def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect('laptops.db')
    # This allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row 
    return conn

# ==========================================
# CRUD Endpoints [cite: 69, 72]
# ==========================================

# 1. READ (Get Multiple Items)
@app.get("/laptops", response_model=List[LaptopResponse], status_code=status.HTTP_200_OK, tags=["Laptops"])
def get_laptops(limit: int = 10, skip: int = 0):
    """
    Retrieve a list of laptops. 
    Supports pagination via 'limit' and 'skip' query parameters.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laptops LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# 2. READ (Get Single Item)
@app.get("/laptops/{laptop_id}", response_model=LaptopResponse, status_code=status.HTTP_200_OK, tags=["Laptops"])
def get_laptop(laptop_id: int):
    """
    Retrieve a specific laptop by its unique ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laptops WHERE id = ?", (laptop_id,))
    row = cursor.fetchone()
    conn.close()
    
    # Error Handling: Return 404 if the item doesn't exist 
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found")
    return dict(row)

# 3. CREATE (Add a New Item)
@app.post("/laptops", response_model=LaptopResponse, status_code=status.HTTP_201_CREATED, tags=["Laptops"])
def create_laptop(laptop: LaptopBase):
    """
    Create a new gaming laptop entry in the database.
    Returns the created object along with its newly generated ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO laptops (title, brand, price, discount_pct, price_currency, stars, reviews_count) 
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (laptop.title, laptop.brand, laptop.price, laptop.discount_pct, laptop.price_currency, laptop.stars, laptop.reviews_count)
    )
    conn.commit()
    new_id = cursor.lastrowid # Retrieve the auto-incremented ID
    conn.close()
    
    # Merge the generated ID with the input data for the response
    return {**laptop.model_dump(), "id": new_id}

# 4. UPDATE (Modify an Existing Item)
@app.put("/laptops/{laptop_id}", response_model=LaptopResponse, status_code=status.HTTP_200_OK, tags=["Laptops"])
def update_laptop(laptop_id: int, laptop: LaptopBase):
    """
    Update all fields of an existing laptop by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE laptops 
           SET title=?, brand=?, price=?, discount_pct=?, price_currency=?, stars=?, reviews_count=? 
           WHERE id=?''',
        (laptop.title, laptop.brand, laptop.price, laptop.discount_pct, laptop.price_currency, laptop.stars, laptop.reviews_count, laptop_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found. Cannot update.")
    return {**laptop.model_dump(), "id": laptop_id}

# 5. DELETE (Remove an Item)
@app.delete("/laptops/{laptop_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Laptops"])
def delete_laptop(laptop_id: int):
    """
    Delete a laptop from the database by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM laptops WHERE id=?", (laptop_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found. Cannot delete.")
    return # 204 No Content doesn't require a JSON body