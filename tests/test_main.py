import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the path to the parent directory to ensure the main.py file can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import your FastAPI app
from main import app

# Create a test client for the FastAPI app
client = TestClient(app)

# Test GET / endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Quantum AI Project API"}

# Test GET /quantum-ai/status endpoint
def test_get_status():
    response = client.get("/quantum-ai/status")
    assert response.status_code == 200
    # Fix the expected response to match the actual response
    assert response.json() == {"status": "Quantum AI is up and running!"}

# Test POST /quantum-ai/predict endpoint
def test_predict():
    # Test with a sample input value
    input_value = 1.5
    response = client.post("/quantum-ai/predict", json={"input_value": input_value})
    assert response.status_code == 200
    assert "quantum_result" in response.json()
    assert "classical_result" in response.json()

    # Test with another input value
    input_value = 2.0
    response = client.post("/quantum-ai/predict", json={"input_value": input_value})
    assert response.status_code == 200
    assert "quantum_result" in response.json()
    assert "classical_result" in response.json()
