from typing import List
from numpy import short
from numpy.lib.function_base import average
from numpy.lib.npyio import save
from palloq import compiler
import pandas as pd
from qiskit.circuit.quantumcircuit import QuantumCircuit

# import qiskit tools
from qiskit.compiler import assemble, transpile, schedule
from qiskit.providers.ibmq import IBMQBackend


from palloq.compiler import dynamic_multiqc_compose
from utils.get_backend import get_IBM_backend
from utils.process_counts_distribution import separate_multi_counts
from utils.pickle_tools import pickle_dump, pickle_load


def prep_experiments(qc_list: List[QuantumCircuit], backend: IBMQBackend, physical_dist_list:List[int], save_path,):
    """prepare experiments multiple qcs varing hardware usage"""

    # prepare pandas dataframe
    columns = ["Backend", "Physical distance", "Hardware Usage (%)", "Total Circuit Duration Time","Quantum Circuits", "Scheduled Pulse"]
    df = pd.DataFrame(columns=columns)

    # backend info
    num_qubits = backend.configuration().num_qubits


    for physical_dist in physical_dist_list:
        transpiled = dynamic_multiqc_compose(
            queued_qc = qc_list,
            backend= backend,
            routing_method="sabre",
            scheduling_method="alap",
            num_hw_dist=physical_dist,
        )

        scheduled = schedule(transpiled, backend = backend)
        usage = "{:.2%}".format(average([_qc.num_qubits/num_qubits for _qc in transpiled]))
        tdt = sum([_sched._duration for _sched in scheduled])
        df.append(
            {
                "Backend": backend.name, 
                "Physical distance": physical_dist, 
                "Hardware Usage (%)": usage, 
                "Total Circuit Duration Time": tdt,
                "Quantum Circuits": transpiled, 
                "Scheduled Pulse": scheduled,    
            }
        )
    df.to_csv(save_path)

def run_experiments_on_backend(backend, experiments_path, save_path, output=False):
    """run the experiments you prepared and save the job information as csv file

    Args:
        backend (IBMQBackend): [description]
        experiments_path ([type]): [description]
        save_path ([type]): [description]
        output (bool, optional): If output = True, return dataframe. Defaults to False.

    Returns:
        DataFrame: if output = True return dataframe
    """
    # define properties of experiments
    shots = 8192

    # retrieve list of quantum circuit from pickle file
    qc_list_dict = pickle_load(experiments_path)

    # define simulator
    simulator = get_IBM_backend("ibmq_qasm_simulator")

    # prepare pandas dataframe to collect data
    columns = ["Job ID", "Backend", "Physical distance", "Hardware Usage (%)", "Quantum Circuits"]
    df = pd.DataFrame(columns=columns)

    # run on backends
    for qc_list, dist in qc_list_dict:
        # job_sim_id = backend.run(assemble(experiments=qc_list, backend=backend, shots=short)).job_id()
        job_id = backend.run(
            assemble(experiments=qc_list, backend=backend, shots=short)
        ).job_id()

        df = df.append(
            {
                "Job ID": job_id,
                "Backend": backend.name(),
                "Physical distance": dist,
                "Quantum Circuits": qc_list,
            }
        )

    # save the job_ids as csv
    df.to_csv(save_path)

    if output: 
        return df


def results_experiments(backend, job_id_path):
    pass