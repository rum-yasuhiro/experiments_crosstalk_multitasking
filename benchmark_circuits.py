from typing import List, Union, Dict, Callable, Any, Optional, Tuple
import numpy as np
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.circuit.library import QFT


def make_benckmarks(circ_components: Optional[Union[Dict[str, int], List[Dict[str, int]]]]) -> Optional[Union[List[QuantumCircuit], List[List[QuantumCircuit]]]]:
    """
    QAOA circuit from: https://qiskit.org/textbook/ch-applications/qaoa.html
    Variational form circuit from: https://qiskit.org/textbook/ch-applications/vqe-molecules.html
    """
    if not isinstance(circ_components, List):
        circ_components = [circ_components]

    circuits_list = _compose_circuit_list(circ_components)

    if len(circuits_list) == 1 and not isinstance(circuits_list[0], QuantumCircuit):
        return circuits_list[0]
    return circuits_list


def _compose_circuit_list(circ_components):
    circuits_list_list = []
    for components in circ_components:
        _circuits_list = []
        for circ_name, num_circ in components.items():
            _components = _get_circuit(circ_name, num_circ)
            _circuits_list.extend(_components)
        circuits_list_list.append(_circuits_list)
    return circuits_list_list


def _get_circuit(circ_name, num_circ):
    circ_list = []
    for i in range(num_circ):
        if circ_name == 'Toffoli':
            _circ = toffoli_circuit(i)
        elif circ_name == 'Toffoli_SWAP':
            _circ = toffoli_circuit_SWAP(i)
        elif circ_name == 'Fredkin':
            _circ = fredkin_circuit(i)
        elif circ_name == 'QAOA_3':
            _circ = qaoa_circuit(3, i)
        elif circ_name == 'QAOA_4':
            _circ = qaoa_circuit(4, i)
        elif circ_name == 'QFT_2':
            _circ = qft_circuit(2, i)
        elif circ_name == 'QFT_3':
            _circ = qft_circuit(3, i)
        else:
            raise ValueError(
                "You can use only 'Toffli', 'Fredkin', 'QAOA_3', 'QAOA_4'.")

        circ_list.append(_circ)
    return circ_list


def toffoli_circuit(id, measure=True):
    name = "Toffoli_"+str(id)
    _toffoli_circ = QuantumCircuit(3, 3, name=name)
    _toffoli_circ.toffoli(0, 1, 2)
    if measure:
        _toffoli_circ.measure((0, 1, 2), (0, 1, 2))
    return _toffoli_circ


def toffoli_circuit_SWAP(id, measure=True):
    """
    c1, c2, t => c1, t, c2
    bacause it only needs linear hw topology
    """
    name = "Toffoli_"+str(id)
    _toffoli_circ = QuantumCircuit(3, 3, name=name)
    _toffoli_circ.h(2)
    _toffoli_circ.cx(0, 2)
    _toffoli_circ.tdg(2)
    _toffoli_circ.cx(1, 2)
    _toffoli_circ.t(2)
    _toffoli_circ.cx(0, 2)
    _toffoli_circ.tdg(2)
    _toffoli_circ.cx(2, 1)  # SWAP
    _toffoli_circ.cx(1, 2)  # SWAP
    _toffoli_circ.t(0)
    _toffoli_circ.t(1)
    _toffoli_circ.cx(2, 0)
    _toffoli_circ.tdg(0)
    _toffoli_circ.h(1)
    _toffoli_circ.t(2)
    _toffoli_circ.cx(2, 0)
    if measure:
        _toffoli_circ.measure((0, 1, 2), (0, 2, 1))
    return _toffoli_circ


def fredkin_circuit(id, measure=True):
    """
    Fig.3 from 
    https://dl.acm.org/doi/10.1145/2629525
    """
    name = "Fredkin_"+str(id)
    _fredkin_circ = QuantumCircuit(3, 3, name=name)
    _fredkin_circ.fredkin(0, 1, 2)

    if measure:
        _fredkin_circ.measure((0, 1, 2), (0, 1, 2))
    return _fredkin_circ


def qaoa_circuit(size, id, measure=True):
    """
    This QAOA code origin from: https://qiskit.org/textbook/ch-applications/qaoa.html#implementation
    """
    # Evaluate the function
    step_size = 0.1
    a_gamma = np.arange(0, np.pi, step_size)
    a_beta = np.arange(0, np.pi, step_size)
    a_gamma, a_beta = np.meshgrid(a_gamma, a_beta)
    F1 = 3-(np.sin(2*a_beta)**2*np.sin(2*a_gamma)**2-0.5 *
            np.sin(4*a_beta)*np.sin(4*a_gamma))*(1+np.cos(4*a_gamma)**2)
    # Grid search for the minimizing variables
    result = np.where(F1 == np.amax(F1))
    a = list(zip(result[0], result[1]))[0]
    gamma = a[0]*step_size
    beta = a[1]*step_size

    # prepare the quantum and classical resisters
    _qaoa_circ = QuantumCircuit(size, size)
    # apply the layer of Hadamard gates to all qubits
    _qaoa_circ.h(range(size))
    # _qaoa_circ.barrier()
    # apply the Ising type gates with angle gamma along the edges in E
    for e in range(size-1):
        k = e
        l = e+1
        _qaoa_circ.cu1(-2*gamma, k, l)
        _qaoa_circ.u1(gamma, k)
        _qaoa_circ.u1(gamma, l)
    # then apply the single qubit X - rotations with angle beta to all qubits
    # _qaoa_circ.barrier()
    _qaoa_circ.rx(2*beta, range(size))
    # Finally measure the result in the computational basis

    if measure:
        _qaoa_circ.measure(range(size), range(size))
    return _qaoa_circ


def _variational(size, id, measure=True):
    name = 'Variational'+str(size)+'_'+str(id)
    _var_circ = EfficientSU2(num_qubits=size, entanglement="linear")
    _var_circ.name = name
    if measure:
        _var_circ.measure_all()
    return _var_circ


def qft_circuit(size, id, measure=True):
    name = 'QFT'+str(size)+'_'+str(id)
    _qft_circ = QFT(size)
    _qft_circ.name = name
    if measure:
        _qft_circ.measure_all()
    return _qft_circ
