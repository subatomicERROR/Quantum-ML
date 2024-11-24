import torch
import pennylane as qml
from fastapi import FastAPI
from pydantic import BaseModel  # For data validation

# Create FastAPI app instance
app = FastAPI()

# Define a quantum device using PennyLane
dev = qml.device("default.qubit", wires=1)

# Define a simple quantum circuit using PennyLane
@qml.qnode(dev)
def quantum_circuit(x):
    qml.Hadamard(wires=0)
    qml.RX(x, wires=0)
    return qml.expval(qml.PauliZ(0))

# Classical Machine Learning Model (PyTorch)
class QuantumModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(1, 1)  # Simple linear model

    def forward(self, x):
        return self.linear(x)

# Initialize the model
model = QuantumModel()

# Pydantic model for the POST request
class InputValue(BaseModel):
    value: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quantum AI Project API"}

@app.get("/quantum-ai/status")
def get_status():
    return {"status": "Quantum AI is running!"}

# Endpoint for making predictions using both Quantum and Classical models
@app.post("/quantum-ai/predict")
def predict(input_value: InputValue):
    # Get quantum result
    quantum_result = quantum_circuit(input_value.value)
    
    # Get classical result
    classical_result = model(torch.tensor([[input_value.value]]))
    
    # Return both results
    return {"quantum_result": quantum_result, "classical_result": classical_result.item()}
