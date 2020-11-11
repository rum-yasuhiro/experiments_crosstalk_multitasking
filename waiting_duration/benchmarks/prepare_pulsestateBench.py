from typing import List

from qiskit.circuit import QuantumCircuit


def prepare_pulsestateBench() -> QuantumCircuit: 
    benchmark_qc = QuantumCircuit(1, name="pulse state")
    benchmark_qc.h(1)
    return benchmark_qc

