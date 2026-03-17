from fastapi.testclient import TestClient
from main import app

# Initialize the TestClient with our FastAPI app instance
client = TestClient(app)

# ==========================================
# Automated Testing Suite for Gaming Laptops API
# ==========================================

def test_read_laptops():
    """
    Test 1: Verify that the public GET endpoint works without authentication.
    It should return a 200 OK status and a list of laptop objects.
    """
    response = client.get("/laptops?limit=5")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_laptop_unauthorized():
    """
    Test 2: Verify that a POST request without authentication is blocked.
    It should return a 401 Unauthorized status.
    """
    new_laptop = {
        "title": "Hacker Laptop",
        "brand": "HackerBrand",
        "price": 0.0
    }
    response = client.post("/laptops", json=new_laptop)
    
    # Assert that the server rejects the request due to missing credentials
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_and_delete_laptop_authorized():
    """
    Test 3: Verify the full authorized CRUD lifecycle.
    Successfully create (POST) a record, then immediately delete (DELETE) it
    using valid Basic Auth credentials to ensure the database remains clean.
    """
    # Step 1: Prepare valid payload for creation
    new_laptop = {
        "title": "Test Gaming Pro",
        "brand": "TestBrand",
        "price": 1999.99,
        "discount_pct": 5.0,
        "price_currency": "$",
        "stars": 4.8,
        "reviews_count": 10
    }
    
    # Send POST request with valid Basic Auth credentials
    response = client.post("/laptops", json=new_laptop, auth=("admin", "secret123"))
    
    # Assert successful creation (201 Created)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Gaming Pro"
    
    # Extract the auto-generated ID of the newly created laptop
    laptop_id = data["id"]

    # Step 2: Immediately delete the created record to maintain testing hygiene
    delete_response = client.delete(f"/laptops/{laptop_id}", auth=("admin", "secret123"))
    
    # Assert successful deletion with no content returned (204 No Content)
    assert delete_response.status_code == 204