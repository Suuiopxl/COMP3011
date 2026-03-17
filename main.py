from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import sqlite3
import secrets
from typing import List

# FastAPI initialization
app = FastAPI(
    title="2026 Q1 Gaming Laptops Market API",
    description="A RESTful API for querying and managing gaming laptop market data. Built with FastAPI and SQLite. Features Basic Authentication for modifying data.",
    version="1.0.0"
)

# Authentication
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):

    """
    For demonstration, using userID 'admin'
    and password 'secret123'.
    """
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

class LaptopBase(BaseModel):
    title: str
    brand: str
    price: float
    discount_pct: float = 0.0
    price_currency: str = "$"
    stars: float = 0.0
    reviews_count: int = 0

class LaptopResponse(LaptopBase):
    id: int

def get_db_connection():
    conn = sqlite3.connect('laptops.db')
    conn.row_factory = sqlite3.Row 
    return conn

# CRUD Endpoints

# 1. READ (public access, no verification)
@app.get("/laptops", response_model=List[LaptopResponse], status_code=status.HTTP_200_OK, tags=["Laptops"])
def get_laptops(limit: int = 10, skip: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laptops LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# 2. READ (public access)
@app.get("/laptops/{laptop_id}", response_model=LaptopResponse, status_code=status.HTTP_200_OK, tags=["Laptops"])
def get_laptop(laptop_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laptops WHERE id = ?", (laptop_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found")
    return dict(row)

# 3. CREATE (Requires identity verification)
@app.post("/laptops", response_model=LaptopResponse, status_code=status.HTTP_201_CREATED, tags=["Laptops"])
def create_laptop(laptop: LaptopBase, username: str = Depends(get_current_username)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO laptops (title, brand, price, discount_pct, price_currency, stars, reviews_count) 
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (laptop.title, laptop.brand, laptop.price, laptop.discount_pct, laptop.price_currency, laptop.stars, laptop.reviews_count)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**laptop.model_dump(), "id": new_id}

# 4. UPDATE (Requires identity verification)
@app.put("/laptops/{laptop_id}", response_model=LaptopResponse, status_code=status.HTTP_200_OK, tags=["Laptops"])
def update_laptop(laptop_id: int, laptop: LaptopBase, username: str = Depends(get_current_username)):
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found.")
    return {**laptop.model_dump(), "id": laptop_id}

# 5. DELETE (Requires identity verification)
@app.delete("/laptops/{laptop_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Laptops"])
def delete_laptop(laptop_id: int, username: str = Depends(get_current_username)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM laptops WHERE id=?", (laptop_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laptop not found.")
    return