from typing import List

from qiskit.circuit import QuantumCircuit


def prepare_pulsestateBench(label) -> QuantumCircuit: 
    qc_name = "pulse state_"+ str(label)
    benchmark_qc = QuantumCircuit(1, name=qc_name)
    benchmark_qc.h(0)
    return benchmark_qc

