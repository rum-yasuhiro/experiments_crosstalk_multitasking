from typing import List
import glob

from qiskit.circuit import QuantumCircuit


def prepare_QASMBench() -> List[QuantumCircuit]: 
    path_to_qasm = "/Users/Yasuhiro/Documents/aqua/gp/QASMBench/small/*/*.qasm"
    path_list = glob.glob(path_to_qasm)
    benchmark_qc_list = []
    for path_i in path_list:
        try: 
            qc_i = QuantumCircuit.from_qasm_file(path_i)
            qc_name = os.path.splitext(os.path.basename(path_i))[0]
            qc_i.name = qc_name
            benchmark_qc_list.append(qc_i)
        except:
            pass
    return benchmark_qc_list
