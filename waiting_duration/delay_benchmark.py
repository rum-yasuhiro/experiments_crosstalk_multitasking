from typing import List

from qiskit import QuantumCircuit, execute
from qiskit.compiler import sequence, transpile
from qiskit.circuit import Measure

from .insert_delay import InsertDelay
from experiments import EvaluateDelay

class DelayBenchmark:
    def __init__(self, benchmark_qc: QuantumCircuit):
        self.benchmark_qc = benchmark_qc.remove_final_measurements(inplace=False)

    def compose(
        self,
        delay_duration_list: List[int] = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000],
        ):

        self.delay_op_list = []
        self.delay_meas_list = []
        self.circ_sim = self.benchmark_qc.copy(name="simulator")
        for delay_duration in delay_duration_list: 
            delayed_circ = InsertDelay(delay_duration, self.benchmark_qc)

            delayed_op = delayed_circ.before_operation()
            self.delay_op_list.append(delayed_op)
            
            delayed_meas = delayed_circ.before_measurement()
            self.delay_meas_list.append(delayed_meas)

    def run(self, backend, simulator, initial_layout, nseed=1):
        job_sim = execute(self.circ_sim, backend=simulator, shots=8192)

        job_delay_op_list = []
        job_delay_meas_list = []
        for seed in range(nseed): 
            transpiled_delay_op_list = transpile(self.delay_op_list, backend=backend, initial_layout = initial_layout, basis_gates=['u1', 'u2', 'u3', 'cx'])
            job_delay_op = execute(
                            transpiled_delay_op_list,
                            backend=backend, 
                            shots=8192, 
                            basis_gates = ['u1', 'u2', 'u3', 'cx'], 
                            initial_layout = initial_layout, 
                            schedule_circuit=True
                            )
            job_delay_op_list.append(job_delay_op)

            transpiled_delay_meas_list = transpile(self.delay_meas_list, backend=backend, basis_gates=['u1', 'u2', 'u3', 'cx'])
            job_delay_meas = execute(
                            transpiled_delay_meas_list,
                            backend=backend, 
                            shots=8192, 
                            basis_gates = ['u1', 'u2', 'u3', 'cx'], 
                            initial_layout = initial_layout, 
                            schedule_circuit=True
                            )
            job_delay_meas_list.append(job_delay_meas)

        if nseed == 1:     
            return job_sim, job_delay_op_list[0], job_delay_meas_list[0]
        return job_sim, job_delay_op_list, job_delay_meas_list
    
    def result(job_sim, job_delay_op, job_delay_meas, delay_duration_list):  
        return EvaluateDelay(job_sim, job_delay_op, job_delay_meas, delay_duration_list)