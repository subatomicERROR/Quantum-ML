import torch
import pennylane as qml
from fastapi import FastAPI
from pydantic import BaseModel  # For data validation

# Initialize FastAPI app instance
app = FastAPI()

# Define quantum device (extended to 3 wires for better flexibility)
dev = qml.device("default.qubit", wires=3)

# Define the quantum circuit (increased complexity)
@qml.qnode(dev)
def quantum_circuit(x):
    # Quantum gates applied on different wires
    qml.Hadamard(wires=0)  # Hadamard gate on qubit 0
    qml.RX(x, wires=0)      # Rotation on qubit 0
    qml.RY(x, wires=1)      # Rotation on qubit 1
    qml.CNOT(wires=[0, 1])  # CNOT gate between qubits 0 and 1
    qml.CNOT(wires=[1, 2])  # CNOT gate between qubits 1 and 2
    return qml.expval(qml.PauliZ(0))  # Measure Pauli-Z on qubit 0

# Classical Machine Learning Model (Hybrid model for better results)
class QuantumModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(3, 1)  # Simple linear model with 3 input features

    def forward(self, x):
        return self.linear(x)  # Pass input through the linear layer

# Pydantic model for the POST request (to handle input data)
class InputValue(BaseModel):
    input_value: float  # Input value for prediction (will be used in the quantum circuit)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quantum AI Project API"}

@app.get("/quantum-ai/status")
def get_status():
    return {"status": "Quantum AI is up and running!"}

# Hybrid endpoint for predictions (quantum + classical)
@app.post("/quantum-ai/predict")
def predict(input_value: InputValue):
    # Get quantum result using the quantum circuit
    quantum_result = quantum_circuit(input_value.input_value)
    
    # Classical result using the hybrid model (taking quantum result as input)
    classical_model = QuantumModel()
    
    # Adjust the quantum_result shape to (1, 3) for the linear layer to accept
    input_tensor = torch.tensor([[quantum_result, quantum_result, quantum_result]], dtype=torch.float32)
    
    classical_result = classical_model(input_tensor)  # Pass through the model
    
    return {"quantum_result": quantum_result, "classical_result": classical_result.item()}

# Placeholder for the API subscription endpoint (simulate freemium model)
@app.post("/quantum-ai/subscribe")
def subscribe_to_api(user_email: str):
    # Simulate API subscription logic
    return {"status": "Subscription successful", "email": user_email}
