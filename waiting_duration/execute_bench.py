from typing import List, Union
from datetime import date

from qiskit.circuit import QuantumCircuit
from qiskit.providers import BaseJob

from experiments.utils import pickle_dump
from experiments.waiting_duration import DelayBenchmark

def execute_bench(experiments: Union[QuantumCircuit, List[QuantumCircuit]], 
        backend, simulator, initial_layout, 
        nseed=1, 
        delay_duration_list: List[int] = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000],
        save_job_ids=True, 
        ): 
    
    if isinstance(experiments, QuantumCircuit):
        experiments = [experiments]
    
    for qc, il in zip(experiments, initial_layout): 
        delay_bench = DelayBenchmark(qc)
        delay_bench.compose(delay_duration_list)
        job_sim, job_delay_op_list, job_delay_meas_list = delay_bench.run(backend, simulator, 
                                                            initial_layout=il, nseed=nseed)

        if isinstance(job_delay_op_list, BaseJob):
             job_delay_op_list = [job_delay_op_list]
        if isinstance(job_delay_meas_list, BaseJob):
             job_delay_meas_list = [job_delay_meas_list]

        if save_job_ids:
            save_experiments(qc, backend, job_sim, job_delay_op_list, job_delay_meas_list, nseed, delay_duration_list, initial_layout)



def save_experiments(qc, backend, job_sim, job_delay_op_list, job_delay_meas_list, nseed, delay_duration_list, initial_layout): 
    # define path to save
    path_to_dir = "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/job_id/"
    file_name = str(date.today()) + "_" + qc.name + "_" + backend.name() + "_" + str(initial_layout) + ".pickle"
    save_path = path_to_dir +  file_name
    
    # get job_id
    job_id_sim = job_sim.job_id()
    job_id_delay_op_list = [job_delay_op.job_id() for job_delay_op in job_delay_op_list]
    job_id_delay_meas_list = [job_delay_meas.job_id() for job_delay_meas in job_delay_meas_list]

    # compose experimental data
    experiments_data = {
        "simulator": {
            "job_id": job_id_sim, 
        }, 
        "delay_op": {
            "job_id": job_id_delay_op_list,
            "nseed": nseed,
        }, 
        "delay_meas": {
            "job_id": job_id_delay_meas_list,
            "nseed": nseed, 
        }, 
        "qc_name": qc.name,
        "delay_duration_list": delay_duration_list,
    }

    pickle_dump(experiments_data, save_path)

