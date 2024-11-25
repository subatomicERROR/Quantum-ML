import pennylane as qml
import torch
import numpy as np

# Define the quantum device (increased wires and improved configuration)
dev = qml.device("default.qubit", wires=3)

# Quantum Node with added features (e.g., entanglement, Hadamard)
@qml.qnode(dev)
def quantum_circuit(weights):
    # Apply a Hadamard gate and other rotations
    qml.Hadamard(wires=0)
    qml.RX(weights[0], wires=1)
    qml.RY(weights[1], wires=2)
    
    # Add entanglement
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    
    # Measurement
    return qml.expval(qml.PauliZ(0))

# Define hybrid classical-quantum model
class QuantumMLModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(3, 1)  # Increased dimensionality for more complex data

    def forward(self, x):
        return self.linear(x)

# Function to use quantum output as part of the optimization process
def hybrid_model(weights):
    quantum_output = quantum_circuit(weights)
    classical_input = torch.tensor([[quantum_output]], dtype=torch.float32)
    return classical_input

# Optimization using Torch's optimization libraries
def optimize_model():
    model = QuantumMLModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(100):
        weights = np.random.rand(3)  # Generate random weights for the quantum circuit
        optimizer.zero_grad()
        loss = model(hybrid_model(weights))  # Hybrid quantum-classical loss
        loss.backward()
        optimizer.step()
    return model
