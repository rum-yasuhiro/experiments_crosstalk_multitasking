import os

from physical_distance_layout_pass.execution_time_and_density.exp_tools import prep_experiments
from utils.prep_QASMBench import PrepQASMBench, save_QuantumCircuit_data
from qiskit.test.mock import FakeManhattan


def case1_1():

    bench_qc_names = [
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        # "linearsovler_n3",
        # "ipn_n5",
        # "pec_en_n5",
    ]
    qasm_bench_path = os.getcwd() + "/qiskit_qasmbench.pickle"
    queued_qasmbench = PrepQASMBench(qasm_bench_path).qc_list(bench_names=bench_qc_names)
    file_path = os.getcwd() + "/physical_distance_layout_pass/execution_time_and_density/experiments_circuit/case1_1.csv"
    
    backend = FakeManhattan()
    
    df = prep_experiments(
        qc_list=queued_qasmbench,
        backend = backend,
        physical_dist_list=[0, 1],
        save_path=file_path,
        output=True,
    )

    print(df)

def case1_2():

    bench_qc_names = [
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2","wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "wstate_n3", 
        "adder_n4", 
        "basis_change_n3",
        "cat_state_n4",
        "deutsch_n2",
        "fredkin_n3",
        "grover_n2",
        "hs4_n4",
        "inverseqft_n4",
        "iswap_n2",
        "inverseqft_n4",
        "iswap_n2",
        "inverseqft_n4",
    ]
    
    qasm_bench_path = os.getcwd() + "/qiskit_qasmbench.pickle"
    queued_qasmbench = PrepQASMBench(qasm_bench_path).qc_list(bench_names=bench_qc_names)
    file_path = os.getcwd() + "/physical_distance_layout_pass/execution_time_and_density/experiments_circuit/case1_1.csv"
    
    backend = FakeManhattan()
    
    df = prep_experiments(
        qc_list=queued_qasmbench,
        backend = backend,
        physical_dist_list=[1],
        save_path=file_path,
        output=True,
    )

    print(df)


if __name__ == "__main__":
    # save_path = os.getcwd() + "/qiskit_qasmbench.pickle"
    # basis_gates = ['id', 'rz', 'sx', 'x', 'cx', 'reset']
    # save_QuantumCircuit_data(save_path, basis_gates)

    case1_2()