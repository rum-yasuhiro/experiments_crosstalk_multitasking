from typing import List

from qiskit.circuit import QuantumCircuit


def prepare_zerostateBench(label) -> QuantumCircuit: 
    qc_name = "plus state_"+ str(label)
    benchmark_qc = QuantumCircuit(1, name=qc_name)
    benchmark_qc.i(0)
    return benchmark_qc

