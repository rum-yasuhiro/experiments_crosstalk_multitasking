from datetime import date

from experiments.waiting_duration.benchmarks import prepare_pulsestateBench
from experiments.waiting_duration import execute_bench
from experiments.waiting_duration import EvaluateDelay
from experiments.utils import get_IBM_backend, pickle_load, pickle_dump

class PulseStateBench:
    def __init__(self, backend_name, nseed, reservations=False): 
        self.backend_name = backend_name
        self.backend = get_IBM_backend(backend_name)
        self.simulator = get_IBM_backend("ibmq_qasm_simulator")
        self.nseed = nseed

    def run(self):
        self.delay_duration_list = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000, 950000, 1000000]
        num_qubits = self.backend.configuration().num_qubits

        self.initial_layout_list = []
        for i in range(num_qubits):
            qc_i = prepare_pulsestateBench(i)
            il = [i]
            print("experiments: ", i)
            execute_bench(qc_i, 
                          backend=self.backend, 
                          simulator=self.simulator, 
                          initial_layout=il, 
                          delay_duration_list=self.delay_duration_list,
                          nseed=self.nseed, 
                          )
            self.initial_layout_list.append(il)
            print("### successfuly ran exp "+ str(i) +" ###")

    def evaluate(self, experiments_data_path_list: list):
        obj_list = []
        for experiments_data_path in experiments_data_path_list:
            
            exp_data = pickle_load(experiments_data_path)
            job_sim = self.simulator.retrieve_job(exp_data["simulator"]["job_id"])
            job_delay_before = [self.backend.retrieve_job(job_id) for job_id in exp_data["delay_before"]["job_id"]]
            job_delay_after = [self.backend.retrieve_job(job_id) for job_id in exp_data["delay_after"]["job_id"]]
            delay_duration_list = exp_data["delay_duration_list"]
            
            eval_delay = EvaluateDelay(job_sim, job_delay_before, job_delay_after, delay_duration_list, nseed=self.nseed, initial_layout=self.initial_layout_list)
            counts_before_list_list, counts_after_list_list = eval_delay.evaluate() # return [[seed1 counts_dict], [seed2 counts_dict], ... ]

            before_jsd_all, before_jsd_mean, before_jsd_sem = eval_delay.js_divergence(counts_before_list_list)
            after_jsd_all, after_jsd_mean, after_jsd_sem = eval_delay.js_divergence(counts_mean_list_list)

            obj = {
                "before_op": {
                    "jsd_add": before_jsd_all, 
                    "jsd_mean": before_jsd_mean, 
                    "jsd_sem": before_jsd_sem, 
                },  
                "after_op": {
                    "jsd_add": after_jsd_all, 
                    "jsd_mean": after_jsd_mean, 
                    "jsd_sem": after_jsd_sem,
                }, 
                "nseed": self.nseed
            }
            obj_list.append(obj)

            # save as pickle file
            path_to_dir = "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/data/jsd/pulse_state_decay/"
            file_name = self.backend_name + "_" + str(date.today()) + "_qubit-" + str(i) + ".pickle"
            save_path = path_to_dir + file_name
            pickle_dump(obj, save_path)
        
        return obj_list

    def plot(self):
        pass
        