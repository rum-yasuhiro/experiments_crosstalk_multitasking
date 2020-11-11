from typing import List, Union
from datetime import date

from qiskit.circuit import QuantumCircuit
from qiskit.providers import BaseJob

from experiments.utils import pickle_dump
from experiments.waiting_duration import DelayBenchmark

def execute_bench(qc: QuantumCircuit, 
        backend, simulator, initial_layout, 
        delay_duration_list: List[int],
        nseed=1,
        save_job_ids=True, 
        ): 

    delay_bench = DelayBenchmark(qc)
    delay_bench.compose(delay_duration_list)
    job_sim, job_delay_before_list, job_delay_after_list = delay_bench.run(backend, simulator, 
                                                        initial_layout=initial_layout, nseed=nseed)

    if isinstance(job_delay_before_list, BaseJob):
            job_delay_before_list = [job_delay_before_list]
    if isinstance(job_delay_after_list, BaseJob):
            job_delay_after_list = [job_delay_after_list]

    if save_job_ids:
        save_experiments(qc, backend, job_sim, job_delay_before_list, job_delay_after_list, nseed, delay_duration_list, initial_layout)



def save_experiments(qc, backend, job_sim, job_delay_before_list, job_delay_after_list, nseed, delay_duration_list, initial_layout): 
    # define path to save
    path_to_dir = "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/job_id/"+ backend.name() +"/"
    file_name = str(date.today()) + "_" + qc.name + "_" + backend.name() + "_" + str(initial_layout) + ".pickle"
    save_path = path_to_dir +  file_name
    
    # get job_id
    job_id_sim = job_sim.job_id()
    job_id_delay_before_list = [job_delay_before.job_id() for job_delay_before in job_delay_before_list]
    job_id_delay_after_list = [job_delay_after.job_id() for job_delay_after in job_delay_after_list]

    # compose experimental data
    experiments_data = {
        "simulator": {
            "job_id": job_id_sim, 
        }, 
        "delay_before": {
            "job_id": job_id_delay_before_list,
            "nseed": nseed,
        }, 
        "delay_after": {
            "job_id": job_id_delay_after_list,
            "nseed": nseed, 
        }, 
        "qc_name": qc.name,
        "delay_duration_list": delay_duration_list,
    }

    pickle_dump(experiments_data, save_path)

