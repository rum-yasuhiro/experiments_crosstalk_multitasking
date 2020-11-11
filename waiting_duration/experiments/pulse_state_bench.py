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
            job_delay_before = self.backend.retrieve_job(exp_data["delay_before"]["job_id"])
            job_delay_after = self.backend.retrieve_job(exp_data["delay_after"]["job_id"])
            delay_duration_list = exp_data["delay_duration_list"]
            
            eval_delay = EvaluateDelay(job_sim, job_delay_before, job_delay_after, delay_duration_list, initial_layout=self.initial_layout_list)
            counts_before_list_list, counts_after_list_list = eval_delay.evaluate() # return [[seed1 counts_dict], [seed2 counts_dict], ... ]

            before_jsd_all, before_jsd_mean, before_jsd_sem = eval_delay.js_divergence(counts_before_list_list)
            after_jsd_all, after_jsd_mean, after_jsd_sem = eval_delay.js_divergence(counts_mean_list_list)

            obj = {
                "before_op": 
                "after_op: "
            }

    def plot(): 
        pass