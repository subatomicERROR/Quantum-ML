import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

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
    assert response.json() == {"status": "Quantum AI is running!"}

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
