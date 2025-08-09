import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import time

def build_galton_box_circuit(n_layers):
    """
    Creates a quantum circuit to simulate a Galton Box.
    """
    position_qubits = n_layers
    ancilla_qubit = n_layers
    qc = QuantumCircuit(position_qubits + 1, position_qubits)
    for i in range(n_layers):
        qc.h(ancilla_qubit)
        qc.cx(ancilla_qubit, i)
        qc.reset(ancilla_qubit)
    qc.measure(range(position_qubits), range(position_qubits))
    return qc

def process_counts_for_galton(counts_dict, n_layers):
    """
    Processes the raw counts from the simulator.
    """
    positions = {i: 0 for i in range(n_layers + 1)}
    for bitstring, count in counts_dict.items():
        pos = bitstring.count('1')
        if pos in positions:
            positions[pos] += count
    return positions

def run_ideal_binomial_simulation(n_layers=8, shots=8192):
    """
    Sets up and runs the ideal binomial simulation.
    """
    print("Starting ideal binomial simulation...")
    start_time = time.time()
    qc = build_galton_box_circuit(n_layers)
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Ideal binomial simulation completed in: {execution_time:.2f} seconds")
    return process_counts_for_galton(counts, n_layers)
