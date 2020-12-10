import os

from experiments.utils import get_IBM_backend
from experiments.alap_scheduling.result_alap import result_alap, parse_job_files


def test_parse_job_files(): 
    job_file_path = str(os.getcwd()) + "/test_jobfile/test_alap_job.pickle"
    simulator = get_IBM_backend("ibmq_qasm_simulator")
    paris = get_IBM_backend("ibmq_paris")

    job_sim, jobs, jobs_alap, job_dict = parse_job_files(job_file_path, paris, simulator)

    assert(isinstance(job_dict, dict))

def test_result_alap(): 
    job_file_path = str(os.getcwd()) + "/test_jobfile/test_alap_job.pickle"
    save_path = str(os.getcwd()) + "/test_jobfile/test_result_alap.pickle"
    simulator = get_IBM_backend("ibmq_qasm_simulator")
    paris = get_IBM_backend("ibmq_paris")

    result_sim, result_list, result_alap_list, counts_sim, count_list, counts_alap_list, qc_names = result_alap(paris, simulator, job_file_path, save_path)