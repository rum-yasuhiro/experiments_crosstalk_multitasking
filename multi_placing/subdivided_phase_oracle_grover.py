import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def spo_grover(num_data: int, measure=False):
    qr = QuantumRegister(num_data)
    ar = QuantumRegister(num_data-3)
    qc = QuantumCircuit(qr, ar)

    data = [qr[0], qr[1], qr[2], qr[3]]
    anc = [ar[0]]

    # initialize
    initialize(qc, data)

    # subdivided phase oracle
    subdivided_phase_oracle(qc, data)

    # difussion operator
    for d in data:
        qc.h(d)
        qc.x(d)
    RTof_m(qc, data[0], data[1], anc[0])
    qc.h(data[2])  # target before swaped
    Tof_swap(qc, anc[0], data[3], data[2])
    qc.h(data[3])  # target after swaped
    RTof_m(qc, data[0], data[1], anc[0])
    for d in data:
        qc.h(d)
        qc.x(d)

    if measure:
        cr = ClassicalRegister(num_data)
        qc.add_creg(cr)
        qc.measure(qr, cr)
    return qc


def initialize(circuit, data: list, replace=False):
    for qubit in data:
        circuit.h(qubit)
    if replace:
        return circuit


def subdivided_phase_oracle(circuit, data: list, replace=False):
    num_data = len(data)
    for qubit in data:
        circuit.rz(np.pi/num_data, qubit)
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
