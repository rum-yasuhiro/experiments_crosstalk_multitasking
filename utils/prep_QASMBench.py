from typing import List, Union
import os
import pathlib
import logging
from glob import glob
from copy import deepcopy

from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile

from experiments.utils import pickle_dump, pickle_load

_log = logging.getLogger(__name__)
class PrepQASMBench():     
    def __init__(self, bench_names: List[str], path):
        """
        This function loads qasm files
        Arguments:
            size: (str) circuit size (small, medium, large)
        """
        self.bench_names = bench_names
        self.benchmarks = {}
        qasmbench = pickle_load(path)

        for name in self.bench_names: 
            self.benchmarks[name] = qasmbench[name]
        
    def qc_list(self):
        qc_list = []
        for i, name in enumerate(self.bench_names):
            qc = deepcopy(self.benchmarks[name]['qc'])
            qc.name = name + "_" +str(i)
            for qreg in qc.qregs: 
                qreg.name = qc.name
            qc_list.append(qc)
        return qc_list

    def to_dict(self): 
        return self.benchmarks

    @classmethod
    def latex_table(cls, size: str, names: List[str]):
        """
        size: 'small', 'medium', 'large'
        names: List of names of the benchmark circuits
        """
        pass

def save_QuantumCircuit_data(save_dir):
    # search qasm files
    QASMBENCH = str(pathlib.Path(os.getcwd()).parent) + '/QASMBench'
    files = glob(str(QASMBENCH) + '/**/*.qasm', recursive=True)
    # convert qasm to QauntumCircuit and add properties
    bench_dict = {}
    for file in files: 
        qc = qasm_to_qc(file)
        name = path_to_filename(file)
        if qc: 
            bench_dict[name] = qc_properties(qc)
    # save
    path = save_dir + 'qasmbench.pickle'
    pickle_dump(bench_dict, path)
    return bench_dict

def qasm_to_qc(qasmfile):
    try:
        qc = QuantumCircuit.from_qasm_file(qasmfile)
        qc.remove_final_measurements()
        qc.measure_active()
    except Exception:
        _log.warning(f"Parsing Qasm Failed at {qasmfile}")
        qc = None
    return qc

def path_to_filename(filepath: str):
        return os.path.splitext(os.path.basename(filepath))[0]

def qc_properties(qc):
    properties = {}
    properties["qc"] = qc
    qp = qc_prop(qc)
    properties['num_qubits'] = qp['num_qubits']
    properties['num_clbits'] = qp['num_clbits']
    properties['ops'] = qp['ops']
    properties['num_cx'] = qp['num_cx']
    properties['depth'] = qp['depth']

    return properties

def qc_prop(qc, basis_gates): 
    qp = {}
    qp['num_qubits'] = qc.num_qubits
    qp['num_clbits'] = qc.num_clbits
    try: 
        transpiled = transpile(qc, basis_gates)
    except: 
        transpiled = transpile(qc)
    ops = transpiled.count_ops()
    qp['ops'] = ops
    try: 
        qp['num_cx'] = ops['cx']
    except:
        qp['num_cx'] = 0
    qp['depth'] = transpiled.depth()
    return qp

if __name__ == '__main__':
    this_path = os.path.abspath(__file__)
    par_dir = os.path.dirname(this_path)
    save_dir = par_dir + '/xtalk_compiler/benchmark_qc/'
    save_QuantumCircuit_data(save_dir)