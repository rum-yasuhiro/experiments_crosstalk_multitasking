import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalReigster


def spo_grover(num_data; int, measure=False):
    qr = QuantumRegister(num_data)
    anc_reg = QuantumRegister(num_data-3)
    qc = QuantumCircuit(qr, anc)

    d0, d1, d2, d3 = [qr[0], qr[1], qr[2], qr[3]]
    anc = anc_reg[0]

    # initialize
    initialize(qc)

    # subdivided phase oracle
    subdivided_phase_oracle(qc, qr.qubits)

    #  CCX_swap
    CCX_s(circuit, n2, anc, n3)
    circuit.barrier()

    if measure:
        cr = ClassicalReigster(num_data)
        qc.add_creg(cr)
        qc.measure(qr, )
    return qc


def initialize(circuit, data: list, replace=False):
    for qubit in data:
        circuit.h(qubit)
    if replace:
        return circuit


def subdivided_phase_oracle(circuit, data: list, replace=False):
    num_data = len(data)
    for qubit in data:
        circuit.rz(qubit, np.pi/num_data)
    if replace:
        return circuit


# define Relative phase Toffoli
def RTof_m(circuit, c1, c2, t, replace=False):
    circuit.ry(np.pi/4, t)
    circuit.cx(c2, t)
    circuit.ry(np.pi/4, t)
    circuit.cx(c1, t)
    circuit.ry(-np.pi/4, t)
    circuit.cx(c2, t)
    circuit.ry(-np.pi/4, t)
    if replace:
        return circuit


# Toffoli gate with one swap
def Tof_swap(circuit, c1, c2, targ, replace=False):  # Toffoli_swap
    circuit.cx(targ, c2)
    circuit.tdg(c2)
    circuit.cx(c1, c2)
    circuit.t(c2)
    circuit.cx(targ, c2)
    circuit.t(targ)
    circuit.tdg(c2)
    circuit.cx(c2, c1)
    circuit.cx(c1, c2)
    circuit.t(c1)
    circuit.cx(c2, targ)
    circuit.t(c2)
    circuit.tdg(targ)
    circuit.cx(c2, targ)
    if replace:
        return circuit
