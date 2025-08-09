
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.fake_provider import FakeVigo
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
import time

def build_binomial_circuit(n_layers):
    """Creates the quantum circuit for the binomial walk."""
    position_qubits = n_layers
    ancilla_qubit = n_layers
    qc = QuantumCircuit(position_qubits + 1, position_qubits)
    for i in range(n_layers):
        qc.h(ancilla_qubit)
        qc.cx(ancilla_qubit, i)
        qc.reset(ancilla_qubit)
    qc.measure(range(position_qubits), range(position_qubits))
    return qc

def process_counts(counts_dict, n_layers):
    """Processes raw bitstring counts into a dictionary of final positions."""
    positions = {i: 0 for i in range(n_layers + 1)}
    for bitstring, count in counts_dict.items():
        pos = bitstring.count('1')
        if pos in positions:
            positions[pos] += count
    return positions

def run_noisy_baseline(n_layers=8, shots=8192):
    """
    Sets up and runs the baseline noisy simulation.
    This function is now self-contained.
    """
    print("Running baseline noisy simulation...")
    start_time = time.time()
    
    backend = FakeVigo()
    noise_model = NoiseModel.from_backend(backend)
    noisy_sim = AerSimulator(noise_model=noise_model)
    
    circuit = build_binomial_circuit(n_layers)
    result = noisy_sim.run(circuit, shots=shots).result()
    counts = result.get_counts()
    
    execution_time = time.time() - start_time
    print(f"Baseline simulation executed in: {execution_time:.2f} seconds")
    
    return process_counts(counts, n_layers)

def run_optimized_simulation(n_layers=8, shots=8192):
    """
    Sets up and runs the optimized noisy simulation.
    This function is also self-contained.
    """
    print("Running optimized noisy simulation...")
    start_time = time.time()

    backend = FakeVigo()
    noise_model = NoiseModel.from_backend(backend)
    basis_gates = noise_model.basis_gates
    noisy_sim = AerSimulator(noise_model=noise_model)
    
    circuit = build_binomial_circuit(n_layers)
    
    optimized_circuit = transpile(circuit, basis_gates=basis_gates, optimization_level=3)
    
    result = noisy_sim.run(optimized_circuit, shots=shots).result()
    counts = result.get_counts()
    
    execution_time = time.time() - start_time
    print(f"Optimized simulation executed in: {execution_time:.2f} seconds")
    
    return process_counts(counts, n_layers)
