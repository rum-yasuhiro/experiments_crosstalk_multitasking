import os

from experiments.physical_distance_layout_pass.execution_time_and_density.experiments import prep_experiments
from utils.prep_QASMBench import PrepQASMBench, save_QuantumCircuit_data



def case1_1():

    bench_qc_names= []
    qasmb = PrepQASMBench()
    queued_qc = 
    file_path = os.getcwd() + "/experiments_circuit/case1_1.csv"
    prep_experiments(output=True)


if __name__ == "__main__":
    save_path = os.getcwd() + "/qiskit_qasmbench.pickle"
    save_QuantumCircuit_data(save_path)

    case1_1()