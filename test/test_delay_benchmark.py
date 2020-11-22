from qiskit import IBMQ, QuantumCircuit
from experiments.waiting_duration import DelayBenchmark
from experiments.utils import get_IBM_backend


def test_delay_benchmark():

    backend = get_IBM_backend("ibmq_paris")
    simulator = get_IBM_backend("ibmq_qasm_simulator")

    path = "/Users/Yasuhiro/Documents/aqua/gp/QASMBench/small/fredkin_n3/fredkin_n3.qasm"
    qc = QuantumCircuit.from_qasm_file(path)

    delay_duration_list = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    delay_benchmark = DelayBenchmark(qc)
    delay_benchmark.compose(delay_duration_list)
    job_id_sim, job_id_op, job_id_meas = delay_benchmark.run(backend=backend, simulator=simulator, initial_layout=[0, 1, 2])

    print(job_id_op, job_id_meas)



if __name__ == "__main__":
    test_delay_benchmark()