from typing import List, Union
import os 
import pathlib
import logging

from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile

from experiments.utils import pickle_dump, pickle_load

_log = logging.getLogger(__name__)
class PrepQASMBench():     
    def __init__(self, size: str):
        """
        This function loads qasm files
        Arguments:
            size: (str) circuit size (small, medium, large)
        """
        pos = os.path.abspath(os.path.dirname(__file__))
        test_files = str(pathlib.Path(pos).parent)
        QASM_BENCH = pathlib.Path(test_files + "/QASMBench")
        if not QASM_BENCH.exists():
            raise Exception("Something wrong with path settings for test")

        if size == "small":
            self.path = QASM_BENCH.joinpath("small")
        elif size == "medium":
            self.path = QASM_BENCH.joinpath("medium")
        elif size == "large":
            self.path = QASM_BENCH.joinpath("large")
        else:
            raise ValueError("size must be small, medium or large")

    def benchmark_prop(self):
        qasmfile_list = [str(i) for qc in self.path.iterdir() for i in qc.glob("[a-z]*.qasm")]

        self.bp = {}
        for qasmfile in qasmfile_list:
            qc = self.qasm_to_qc(qasmfile)
            if qc: 
                name = self.filename(qasmfile)
                self.bp[name] = {}
                self.bp[name]["name"] = name
                self.bp[name]["qc"] = qc
                qp = self.qc_prop(qc)
                self.bp[name]['num_qubits'] = qp['num_qubits']
                self.bp[name]['num_clbits'] = qp['num_clbits']
                self.bp[name]['ops'] = qp['ops']
                self.bp[name]['num_cx'] = qp['num_cx']
                self.bp[name]['depth'] = qp['depth']
            else: 
                continue

        return self.bp

    def qasm_to_qc(self, qasmfile):
        try:
            qc = QuantumCircuit.from_qasm_file(qasmfile)
            qc.remove_final_measurements()
            qc.measure_active()
        except Exception:
            _log.warning(f"Parsing Qasm Failed at {qasmfile}")
            qc = None
        return qc
    
    def filename(self, filepath: str):
        return os.path.splitext(os.path.basename(filepath))[0]

    def qc_prop(self, qc: QuantumCircuit): 
        qp = {}
        qp['num_qubits'] = qc.num_qubits
        qp['num_clbits'] = qc.num_clbits
        try: 
            transpiled = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx', 'delay', 'u3cx', 'barrier', 'snapshot', 'measure', 'reset'])
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

    @classmethod
    def multi_circuits(cls, size, names: List[str]):
        """
        size: 'small', 'medium', 'large'
        names: List of names of the benchmark circuits
        """
        qc_list = []
        path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/alap_scheduling/benchmarks/qasmbench_'+str(size)+'.pickle'
        bp = pickle_load(path)
        for name in names: 
            qc_list.append(bp[name]['qc'])
        return qc_list

    @classmethod
    def save_pickle(cls, obj, path): 
        pickle_dump(obj, path)
        _log.info(obj)

    @classmethod
    def latex_table(cls, size: str, names: List[str]):
        """
        size: 'small', 'medium', 'large'
        names: List of names of the benchmark circuits
        """
        pass