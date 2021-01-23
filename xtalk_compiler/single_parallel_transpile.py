from typing import List, Tuple
from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from multitasking_transpiler.palloq.compiler import multi_transpile



def single_parallel_transpile(experiments: List[QuantumCircuit], backend, mode: str, instruction_durations=None, xtalk_prop=None): 
    
    qc_list = experiments

    if mode == 'dense': 
        qc_multi = multi_transpile(
            qc_list, backend=backend, optimization_level=3, 
            basis_gates=['id', 'rz', 'sx', 'x', 'cx'],
            layout_method='dense', xtalk_prop={},
            )
        sigle_qc = _allocate_same_hwq(qc_list, qc_multi, backend)

    elif mode == 'noise_adaptive': 
        qc_multi = multi_transpile(
            qc_list, backend=backend, optimization_level=3, 
            basis_gates=['id', 'rz', 'sx', 'x', 'cx'],
            layout_method='noise_adaptive', xtalk_prop={},
            )
        sigle_qc = _allocate_same_hwq(qc_list, qc_multi, backend)

    elif mode == 'sabre': 
        qc_multi = multi_transpile(
            qc_list, backend=backend, optimization_level=3, 
            basis_gates=['id', 'rz', 'sx', 'x', 'cx'],
            layout_method='sabre', xtalk_prop={},
            )
        sigle_qc = _allocate_same_hwq(qc_list, qc_multi, backend)

    elif mode == 'xtalk': 
        qc_multi = multi_transpile(
            qc_list, backend=backend,
            instruction_durations=instruction_durations, 
            basis_gates=['id', 'rz', 'sx', 'x', 'cx'], 
            layout_method='xtalk_adaptive', xtalk_prop={},
            )
        sigle_qc = _allocate_same_hwq(qc_list, qc_multi, backend)

    return sigle_qc, qc_multi

def _allocate_same_hwq(qc_list, multi_qc, backend): 
    layout = multi_qc._layout._v2p
    sigle_qc = []
    for _qc in qc_list:
        _init_layout = {}
        for _qubit in _qc.qubits:
            _init_layout[_qubit] = layout.get(_qubit)
        transpiled_qc = transpile(_qc, backend=backend, initial_layout=_init_layout)
        sigle_qc.append(transpiled_qc)

    return sigle_qc
