from experiments.waiting_duration.benchmarks import prepare_pulsestateBench
from experiments.waiting_duration import execute_bench
from experiments.waiting_duration import EvaluateDelay
from experiments.utils import get_IBM_backend, pickle_load

class PulseStateBench:
    def __init__(self, backend_name, nseed, reservations=False): 
        self.backend = get_IBM_backend(backend_name)
        self.simulator = get_IBM_backend("ibmq_qasm_simulator")
        self.nseed = nseed

    def run(self):
        self.delay_duration_list = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 10000]
        num_qubits = backend.configuration().num_qubits

        self.initial_layout_list = []
        for i in range(num_qubits): 
            qc_list.append(prepare_pulsestateBench())
            self.initial_layout_list.append([i])
        
        execute_bench(qc_list, self.backend, self.simulator, initial_layout=self.initial_layout_list nseed=5, delay_duration_list=delay_duration_list)


    def evaluate(self, experiments_data_path_list: list):
        for experiments_data_path in experiments_data_path_list:
            
            exp_data = pickle_load(experiments_data_path)
            job_sim = self.simulator.retrieve_job(exp_data["simulator"]["job_id"])
            job_delay_op = self.backend.retrieve_job(exp_data["delay_op"]["job_id"])
            job_delay_meas = self.backend.retrieve_job(exp_data["delay_meas"]["job_id"])
            delay_duration_list = exp_data["delay_duration_list"]
            
            eval_delay = EvaluateDelay(job_sim, job_delay_op, job_delay_meas, delay_duration_list, initial_layout=self.initial_layout_list)
            counts_delay_op_list, counts_delay_meas_list = eval_delay.evaluate()