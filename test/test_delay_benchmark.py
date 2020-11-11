from qiskit import IBMQ, QuantumCircuit
from experiments.waiting_duration import DelayBenchmark


def test_delay_benchmark():
    # IBMQ.load_account()
    # provider = IBMQ.get_provider(hub='ibm-q-keio', group='keio-internal', project='keio-students')
    # backend = provider.get_backend("ibmq_qasm_simulator")
    # simulator = provider.get_backend("ibmq_qasm_simulator")

    path = "/Users/Yasuhiro/Documents/aqua/gp/QASMBench/small/fredkin_n3/fredkin_n3.qasm"
    qc = QuantumCircuit.from_qasm_file(path)

    delay_duration_list = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    delay_benchmark = DelayBenchmark(qc)
    delay_benchmark.compose()
    job_id_sim, job_id_op, job_id_meas = delay_benchmark.run(backend=backend, simulator=simulator)

    print(job_id_op, job_id_meas)



if __name__ == "__main__":
    test_delay_benchmark()