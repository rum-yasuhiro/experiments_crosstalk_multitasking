from typing import Dict, Tuple, List, Union
from multi_exec import multi_exec, results
from toffoli_circuit import toffoli_circuit
from jsd import jsd
from pst import pst
from pickle_tools import pickle_dump, pickle_load
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm
from datetime import date


def run_distance(backend_name: str,
                 circuit: QuantumCircuit,
                 adj_hwqubits: Dict[Tuple, List[List[Tuple[int]]]],
                 num_trial: int = 100,
                 shots: int = 1024,
                 job_id_path: str = None,
                 hub='ibm-q-utokyo',
                 group='keio-internal',
                 project='keio-students',
                 sendjob_remote=True,
                 return_qc=False,
                 save_path=None,
                 ):
    """

    Args:
        circuit: QauntumCircuit you want to execute in parallel
        adj_hwqubits:
    """

    job_all = {}
    for targ, adj_list_list in adj_hwqubits.items():
        job_partial = []

        # prepare target circuit with measurement
        circuit.remove_final_measurements()
        qc0 = duplicate_qc(circuit)
        qc0.measure_active()

        qubits = qc0.qubits
        num_qubits = len(qubits)
        layout = {}
        for i in range(num_qubits):
            layout[qubits[i]] = targ[i]

        for adj_list in adj_list_list:
            experiments = []
            experiments.append((qc0, layout))
            for adj in adj_list:
                # prepare adjacent circuit without measurement
                qc_i = duplicate_qc(circuit)

                qubits_i = qc_i.qubits
                layout_i = {}
                for i in range(num_qubits):
                    layout_i[qubits_i[i]] = adj[i]

                experiments.append((qc_i, layout_i))

            job = multi_exec(
                backend_name,
                experiments,
                num_trial,
                shots,
                job_id_path,
                hub=hub,
                group=group,
                project=project,
            )
            job_partial.append(job.job_id())

        job_all[targ] = job_partial

    if save_path:
        pickle_dump(job_all, save_path)
    return job_all


def result_distance(backend_name: str,
                    targ_job_id: Dict[Tuple[int],
                                      List[str]],
                    counts_sim,
                    num_trial=100,
                    save_path=None,
                    ):

    print('PD on noiseless simlation: \n', counts_sim)

    columns = ['PST', 'Measured Qubits', 'Hop Count']
    df = DataFrame(columns=columns)

    for targ, job_ids in targ_job_id.items():
        print("Target qubits: ", targ)
        for hop_count, job_id in enumerate(job_ids):
            print('Hop: ', hop_count)
            counts_list = results(backend_name, job_id, num_trial)
            pst_list = [pst(_counts, counts_sim)
                        for _counts in tqdm(counts_list)]
            _df = DataFrame(
                {
                    'Trial': [i+1 for i in range(num_trial)],
                    'PST': pst_list,
                    'Measured Qubits': [targ for _ in range(num_trial)],
                    'Hop Count': [hop_count-1 if hop_count > 0 else 'Single Execution' for _ in range(num_trial)],
                    'PD on realdevice': counts_list,
                    'PD on simulator': [counts_sim for _ in range(num_trial)],
                    'Backend Name': [backend_name for _ in range(num_trial)],
                }
            )
            df = pd.concat([df, _df])

    if save_path:
        df.to_csv(save_path)
    return df


def plot_box(data: Union[DataFrame, str], save_path=None):
    """
    Args:
        data: DataFrame or the path to the csv file contains DataFrame
    """
    if isinstance(data, str):
        data = pd.read_csv(data, index_col=0)

    plt.figure(figsize=(20, 7), dpi=600)
    sns.set_style("whitegrid")
    sns.set(palette="Blues", font_scale=2)
    plot = sns.boxplot(x='Measured Qubits', y='PST',
                         hue='Hop Count', data=data)
    plot.set(ylim=(0, 1))

    plt.tight_layout()
    if save_path:
        fig = plot.get_figure()
        fig.savefig(save_path)


def run_on_manhattan():
    backend_name = 'ibmq_manhattan'

    repeat = 3
    toffoli = toffoli_circuit(repeat=repeat)

    # save file path
    path_prefix = '/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/'
    filename = 'manhattan_toffoli10CX'

    ##########################################################################

    adj_hwqubits = {
        (4, 11, 17): [
            [],
            [(1, 2, 3), (5, 6, 7), (14, 15, 16), (18, 19, 20)],
            [(0, 1, 2), (6, 7, 8), (13, 14, 15), (19, 20, 21)],
            [(10, 1, 0), (7, 8, 12), (24, 29, 28), (25, 33, 34)],
            [(0, 10, 13), (8, 12, 21), (28, 29, 30), (32, 33, 34)],
        ],
        (19, 25, 33): [
            [],
            [(16, 17, 18), (20, 21, 22), (30, 31, 32), (34, 35, 36)],
            [(4, 11, 17), (8, 12, 21), (31, 39, 45), (35, 40, 49)],
            [(3, 4, 11), (12, 8, 9), (39, 45, 44), (40, 49, 50)],
            [(3, 4, 5), (7, 8, 9), (44, 45, 46), (48, 49, 50)],
        ],
        (31, 39, 45): [
            [],
            [(28, 29, 30), (32, 33, 34), (42, 43, 44), (46, 47, 48)],
            [(15, 24, 29), (19, 25, 33), (43, 52, 56), (47, 53, 60)],
            [(14, 15, 24), (25, 19, 20), (52, 56, 55), (53, 60, 61)],
            [(14, 15, 16), (18, 19, 20), (55, 56, 57), (59, 60, 61)],
        ],
        (47, 53, 60): [
            [],
            [(44, 45, 46), (48, 49, 50), (57, 58, 59), (61, 62, 63)],
            [(31, 39, 45), (35, 40, 49), (56, 57, 58), (62, 63, 64)],
            [(30, 31, 39), (36, 35, 40), (52, 56, 57), (54, 64, 63)],
            [(30, 31, 32), (34, 35, 36), (43, 52, 56), (51, 54, 64)],
        ],
    }

    jobid_path = path_prefix + 'job_id/' + \
        str(date.today()) + '_' + filename + '_' + str(repeat)+'.pickle'

    #####################################################################
    hwq_jobs = run_distance(backend_name, toffoli,
                            adj_hwqubits, save_path=jobid_path)
    print(hwq_jobs)
    ####################################################################

    # # run on simulator
    # toffoli = toffoli_circuit(measure=True)
    # simulator = Aer.get_backend('qasm_simulator')
    # job_sim = execute(toffoli, backend=simulator, shots=1024)
    # counts_sim = job_sim.result().get_counts()
    # print(counts_sim)

    # # get the result
    # hwq_jobs = pickle_load(jobid_path)
    # data_path = path_prefix + 'results/' + str(date.today())+ '_' + filename + '_' + \
    #     str(repeat)+'.csv'
    # result_data = result_distance(
    #     backend_name, hwq_jobs, counts_sim, save_path=data_path)
    # print(result_data)

    # fig_path = path_prefix + 'plot/' + str(date.today())+ '_' + filename + '_' + \
    #     str(repeat)+'.png'
    # plot_box(data_path, fig_path)


def run_on_toronto():
    backend_name = 'ibmq_toronto'
    repeat = 1

    path_prefix = '/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/'
    filename = 'toronto_toffoli10CX'
    toffoli = toffoli_circuit(repeat=repeat)

    adj_hwqubits = {
        (12, 13, 14): [
            [],
            [(4, 7, 10), (15, 18, 21), (5, 8, 11), (16, 19, 22)],
            [(1, 4, 7), (18, 21, 23), (3, 5, 8), (19, 22, 25)],
            [(0, 1, 4), (21, 23, 24), (2, 3, 5), (22, 25, 26)],
        ],
        (1, 2, 3): [
            [],
            [(4, 7, 10), (5, 8, 11)],
            [(7, 10, 12), (8, 11, 14)],
            [(10, 12, 15), (11, 14, 16)],
            [(12, 15, 18), (14, 16, 19)],
            [(15, 18, 21), (16, 19, 22)],
            [(18, 21, 23), (19, 22, 25)],
            [(21, 23, 24), (22, 25, 26)],
        ],
        (23, 24, 25): [
            [],
            [(15, 18, 21), (16, 19, 22)],
            [(12, 15, 18), (14, 16, 19)],
            [(10, 12, 15), (11, 14, 16)],
            [(7, 10, 12), (8, 11, 14)],
            [(4, 7, 10), (5, 8, 11)],
            [(1, 4, 7), (3, 5, 8)],
            [(0, 1, 4), (2, 3, 5)],
        ],
    }

    jobid_path = path_prefix + 'job_id/' + str(date.today()) + '_' + filename + '_' + \
        str(repeat)+'.pickle'

    ####################################################################
    # hwq_jobs = run_distance(backend_name, toffoli,
    #                         adj_hwqubits, save_path=jobid_path)
    # print(hwq_jobs)
    ####################################################################

    # run on simulator
    toffoli = toffoli_circuit(measure=True)
    simulator = Aer.get_backend('qasm_simulator')
    job_sim = execute(toffoli, backend=simulator, shots=1024)
    counts_sim = job_sim.result().get_counts()
    print(counts_sim)

    # get the result
    hwq_jobs = pickle_load(jobid_path)
    data_path = path_prefix + 'results/' + \
        str(date.today()) + '_' + filename+'.csv'
    result_data = result_distance(
        backend_name, hwq_jobs, counts_sim, save_path=data_path)
    print(result_data)

    #####################################################################
    fig_path = path_prefix + 'plot/' + str(date.today()) + '_' + filename + '_' + \
        str(repeat)+'.png'
    plot_box(data_path, fig_path)


def duplicate_qc(orig: QuantumCircuit) -> QuantumCircuit:
    num_qubits = orig.num_qubits
    qr = QuantumRegister(num_qubits)
    dest = QuantumCircuit(qr)

    for instr, qarg, carg in orig:
        q_dest = [dest.qubits[q.index] for q in qarg]
        # c_dest = [dest.qubits[c.index] for c in carg]
        dest.append(instr, q_dest, [])

    return dest


if __name__ == '__main__':
    # run_on_manhattan()
    run_on_toronto()
