from typing import List
from numpy.lib.function_base import average

from palloq import compiler
import pandas as pd
from pandas.core.base import DataError
from pandas.core.frame import DataFrame
from qiskit.circuit.quantumcircuit import QuantumCircuit

# import qiskit tools
from qiskit.compiler import assemble, transpile, schedule
from qiskit.providers.ibmq import IBMQBackend


from palloq.compiler.dynamic_multiqc_compose import dynamic_multiqc_compose
from utils.get_backend import get_IBM_backend
from utils.process_counts_distribution import separate_multi_counts
from utils.pickle_tools import pickle_dump, pickle_load


def prep_experiments(qc_list: List[QuantumCircuit], backend: IBMQBackend, physical_dist_list:List[int], save_path, output=False):
    """prepare experiments multiple qcs varing hardware usage"""

    # prepare pandas dataframe
    columns = ["Backend", "Physical distance", "Hardware Usage (%)", "Total Circuit Duration Time","Quantum Circuits", "Scheduled Pulse"]
    df = pd.DataFrame(columns=columns)

    # backend info
    num_hw_qubit = backend.configuration().num_qubits


    for physical_dist in physical_dist_list:
        transpiled, num_usage = dynamic_multiqc_compose(
            queued_qc = qc_list,
            backend= backend,
            routing_method="sabre",
            scheduling_method="alap",
            num_hw_dist=physical_dist,
            return_num_usage = True, 
        )

        scheduled = [schedule(_tqc, backend = backend) for _tqc in transpiled]
        usage = "{:.2%}".format(average([_usage/num_hw_qubit for _usage in num_usage[0:-1]]))
        tdt = sum([_sched._duration for _sched in scheduled])
        df = df.append(
            {
                "Backend": backend.name, 
                "Physical distance": physical_dist, 
                "Hardware Usage (%)": usage, 
                "Total Circuit Duration Time": tdt,
                "Quantum Circuits": transpiled, 
                "Scheduled Pulse": scheduled,    
            },
            ignore_index=True
        )
    
    # save the DataFrame as pickle file
    pickle_dump(obj = df, path = save_path)

    if output: 
        return df

def run_experiments_on_backend(backend, simlator, experiments_df: DataFrame, save_path: str, output=False):
    """run the experiments you prepared and save the job information as csv file

    Args:
        backend (IBMQBackend): [description]
        experiments_df ([type]): [description]
        save_path ([type]): [description]
        output (bool, optional): If output = True, return dataframe. Defaults to False.

    Returns:
        DataFrame: if output = True return dataframe
    """
    # define properties of experiments
    shots = 8192

    # define simulator
    simulator = get_IBM_backend("ibmq_qasm_simulator")

    # prepare pandas dataframe to collect data
    columns = ["Job ID", "Sim Jos ID", "Backend", "Physical distance", "Hardware Usage (%)", "Total Circuit Duration Time","Quantum Circuits", "Scheduled Pulse"]
    df = pd.DataFrame(columns=columns)

    # run on backends
    for row in experiments_df.itertuples():
        # print("0: ", type(row[0]), row[0])
        # print("1: ", type(row[1]), row[1])
        # print("2: ", type(row[2]), row[2])
        # print("3: ", type(row[3]), row[3])
        # print("4: ", type(row[4]), row[4])
        # print("5: ", type(row[5]), row[5])
        print("6: ", type(row[6][0]), row[6][1])

        # backend integrity check
        """TODO コードのテストが終わったらあとでコメント外す"""
        # if backend.name != row[1]:
        #     raise BackendIntegrityError("Backend is not the same as experiments info")
        
        job_sim_id = simlator.run(
            assemble(experiments=row[6], backend=simlator, shots=shots)
        ).job_id()
        job_id = backend.run(
            assemble(experiments=row[6], backend=backend, shots=shots)
        ).job_id()

        df = df.append(
            {
                "Job ID": job_id,
                "Sim Jos ID": job_sim_id,
                "Backend": row[1], 
                "Physical distance": row[2], 
                "Hardware Usage (%)": row[3], 
                "Total Circuit Duration Time": row[4],
                "Quantum Circuits": row[5], 
                "Scheduled Pulse":row[6],  
            }
        )

    # save the DataFrame as pickle file
    pickle_dump(obj = df, path = save_path)

    if output: 
        return df


def results_experiments(backend, job_id_path):
    pass

class BackendIntegrityError(Exception):
    """バックエンドが異なる場合のエラー"""
    pass