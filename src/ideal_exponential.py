import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

def build_custom_walk_circuit(n_layers, theta):
    """
    Builds a quantum walk circuit with a custom, constant rotation angle.
    """
    position_qubits = n_layers
    ancilla_qubit = n_layers
    qc = QuantumCircuit(position_qubits + 1, position_qubits)
    for i in range(n_layers):
        qc.ry(theta, ancilla_qubit)
        qc.cx(ancilla_qubit, i)
        qc.reset(ancilla_qubit)
    qc.measure(range(position_qubits), range(position_qubits))
    return qc

def process_counts_exp(counts_dict, n_layers):
    """
    Processes raw counts and converts them into a probability distribution.
    """
    positions = {i: 0 for i in range(n_layers + 1)}
    for bitstring, count in counts_dict.items():
        pos = bitstring.count('1')
        if pos in positions:
            positions[pos] += count
    return positions


def run_ideal_exponential_simulation(n_layers=8, shots=16384, p_right=0.2):
    """
    Sets up and runs the ideal exponential-like simulation.
    """
    print("Starting ideal exponential simulation...")
    start_time = time.time()
    theta = 2 * np.arcsin(np.sqrt(p_right))
    ideal_sim = AerSimulator()
    exp_circuit = build_custom_walk_circuit(n_layers, theta)
    result = ideal_sim.run(exp_circuit, shots=shots).result()
    counts = result.get_counts()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Ideal exponential simulation completed in: {execution_time:.2f} seconds")
    return process_counts_exp(counts, n_layers)
