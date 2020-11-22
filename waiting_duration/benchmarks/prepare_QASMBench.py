from typing import List
import os
import glob
import logging
from qiskit.circuit import QuantumCircuit


def prepare_QASMBench(size: str):
    logger = logging.getLogger(__name__)
    """
    Args: 
        size: "small", "medium", "large"
    """
    path_to_qasm = "/Users/Yasuhiro/Documents/aqua/gp/QASMBench/"+ str(size) +"/*/*.qasm"
    path_list = glob.glob(path_to_qasm)
    
    benchmark_qc_list = []
    for path_i in path_list:
        try:
            qc_i = QuantumCircuit.from_qasm_file(path_i)
            qc_name = os.path.splitext(os.path.basename(path_i))[0]
            qc_i.name = qc_name
            benchmark_qc_list.append(qc_i)
        except Exception as e:
            logger.info("We can't utilize qasm file: ", str(e))
            
    return benchmark_qc_list

if __name__ == "__main__":
    from pprint import pprint
    benchmark_qc_list = prepare_QASMBench()
    pprint(benchmark_qc_list)