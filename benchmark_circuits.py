from typing import List, Union, Dict, Callable, Any, Optional, Tuple
import numpy as np
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2


def make_benckmarks(circ_components: Optional[Union[Dict[str, int], List[Dict[str, int]]]]) -> Optional[Union[List[QuantumCircuit], List[List[QuantumCircuit]]]]:
    """
    QAOA circuit from: https://qiskit.org/textbook/ch-applications/qaoa.html
    Variational form circuit from: https://qiskit.org/textbook/ch-applications/vqe-molecules.html
    """
    if not isinstance(circ_components, List):
        circ_components = [circ_components]

    circuits_list = _compose_circuit_list(circ_components)

    if len(circuits_list) == 1 and not isinstance(circuits_list[0], QuantumCircuit):
        print("it works")
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
            _circ = _toffoli(i)
        if circ_name == 'Fredkin':
            _circ = _fredkin(i)
        if circ_name == 'QAOA_3':
            _circ = _qaoa(3, i)
        if circ_name == 'QAOA_4':
            _circ = _qaoa(4, i)
        if circ_name == 'VAR_3':
            _circ = _variational(3, i)
        if circ_name == 'VAR_4':
            _circ = _variational(4, i)
        circ_list.append(_circ)
    return circ_list


def _toffoli(index):
    name = "Toffoli_"+str(index)
    _toffoli_circ = QuantumCircuit(3, name=name)
    _toffoli_circ.toffoli(0, 1, 2)
    _toffoli_circ.measure_all()
    return _toffoli_circ


def _fredkin(index):
    name = "Fredkin_"+str(index)
    _fredkin_circ = QuantumCircuit(3, name=name)
    _fredkin_circ.fredkin(0, 1, 2)
    _fredkin_circ.measure_all()
    return _fredkin_circ


def _qaoa(size, index):
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
    _qaoa_circ = QuantumCircuit(size)
    # apply the layer of Hadamard gates to all qubits
    _qaoa_circ.h(range(size))
    _qaoa_circ.barrier()
    # apply the Ising type gates with angle gamma along the edges in E
    for e in range(size-1):
        k = e
        l = e+1
        _qaoa_circ.cu1(-2*gamma, k, l)
        _qaoa_circ.u1(gamma, k)
        _qaoa_circ.u1(gamma, l)
    # then apply the single qubit X - rotations with angle beta to all qubits
    _qaoa_circ.barrier()
    _qaoa_circ.rx(2*beta, range(size))
    # Finally measure the result in the computational basis
    _qaoa_circ.measure_all()
    return _qaoa_circ


def _variational(size, index):
    name = 'Variational'+str(size)+'_'+str(index)
    _var_circ = EfficientSU2(num_qubits=size, entanglement="linear")
    _var_circ.name = name
    _var_circ.measure_all()
    return _var_circ


if __name__ == "__main__":
    d = {'VAR_4': 1}
    circ = make_benckmarks(d)
    for c in circ:
        print(c)
