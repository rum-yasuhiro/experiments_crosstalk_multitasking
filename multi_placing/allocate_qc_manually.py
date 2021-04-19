from typing import Dict
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.circuit import Qubit
from qiskit.compiler import transpile


def allocate_qc_manually(
    qc_map: Dict[QuantumCircuit, Dict[Qubit, int]]
):
    """allocate multipul circuit to hardware qubits and produce it as
    a single combined circuit

    Args:
        qc_map: Pairs of QuantumCircuit and its mapping (dict).
                Only one circuit should have a measurements
                * virtual to physical::

                    {qr[0]: 0,
                    qr[1]: 1,
                    qr[2]: 2}
    Return:
        QuantumCircuit
    """

    comp_qc, layout_d = _compose_qc(qc_map)

    transpiled = transpile(comp_qc, initial_layour=layout_d)

    return transpiled


def _compose_qc(qc_dict):
    """Compose each qc and return new multitask qc"""
    name_list = []
    qubit_counter = 0
    clbit_counter = 0
    layout_dict = {}
    composed_qc = QuantumCircuit()
    for qc, layout_i in enumerate(qc_dict):
        num_qubits = qc.num_qubits
        num_clbits = qc.num_clbits
        layout_dict.update(layout_i)

        reg_name_tmp = qc.qubits[0].register.name
        register_name = reg_name_tmp if (reg_name_tmp not in name_list) and (
            not reg_name_tmp == 'q') else None
        name_list.append(register_name)

        qr = qc.qregs[0]
        composed_qc.add_qreg(qr)
        qubits = composed_qc.qubits[qubit_counter: qubit_counter + num_qubits]

        if num_clbits > 0:
            cr = ClassicalRegister(size=num_clbits, name=None)
            composed_qc.add_creg(cr)
            clbits = composed_qc.clbits[clbit_counter: clbit_counter + num_clbits]

            composed_qc.compose(qc, qubits=qubits, clbits=clbits)
        else:
            composed_qc.compose(qc, qubits=qubits)

        qubit_counter += num_qubits
        clbit_counter += num_clbits
    return composed_qc, layout_dict
