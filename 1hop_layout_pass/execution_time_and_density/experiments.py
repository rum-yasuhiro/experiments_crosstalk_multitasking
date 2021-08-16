from numpy import short
import pandas as pd

# import qiskit tools
from qiskit.compiler import assemble

from palloq.compiler import dynamic_multiqc_compose
from utils.get_backend import get_IBM_backend
from utils.process_counts_distribution import separate_multi_counts
from utils.pickle_tools import pickle_dump, pickle_load


def prep_experiments(backend):
    """prepare experiments multiple qcs varing hardware usage"""


def run_experiments_on_backend(backend, experiments_path):

    # define properties of experiments
    shots = 8192

    # retrieve list of quantum circuit from pickle file
    qc_list_dict = pickle_load(experiments_path)

    # define simulator
    simulator = get_IBM_backend("ibmq_qasm_simulator")

    # prepare pandas dataframe to collect data
    columns = ["Job ID", "Backend", "Hardware usage", "Quantum Circuits"]
    df = pd.DataFrame()

    # run on backends
    for qc_list, usage in qc_list_dict:
        # job_sim_id = backend.run(assemble(experiments=qc_list, backend=backend, shots=short)).job_id()
        job_id = backend.run(
            assemble(experiments=qc_list, backend=backend, shots=short)
        ).job_id()

        df = df.append(
            {
                "Job ID": job_id,
                "Backend": backend.name(),
                "Hardware usage": usage,
                "Quantum Circuits": qc_list,
            }
        )

    # save the job_ids as csv
    save_path = +""
    df.to_csv()


def results_experiments(backend, job_id_path):
