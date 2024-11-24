import pennylane as qml
import torch

# Define the quantum device
dev = qml.device("default.qubit", wires=2)

# Define a quantum circuit
@qml.qnode(dev)
def circuit(weights):
    qml.Hadamard(wires=0)  # Apply Hadamard gate on qubit 0
    qml.RX(weights[0], wires=0)  # Apply rotation gate RX on qubit 0
    qml.RY(weights[1], wires=1)  # Apply rotation gate RY on qubit 1
    return qml.expval(qml.PauliZ(0))  # Measure the Pauli-Z expectation value of qubit 0

# Function to use Torch for optimization
def quantum_model(weights):
    return torch.tensor(circuit(weights), dtype=torch.float32)
