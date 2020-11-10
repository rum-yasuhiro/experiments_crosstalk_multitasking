from qiskit import IBMQ

from experiments.waiting_duration import DelayBenchmark, EvaluateDelay

def test_evaluate_delay():
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q-keio', group='keio-internal', project='keio-students')
    backend = provider.get_backend("ibmq_qasm_simulator")
    simulator = provider.get_backend("ibmq_qasm_simulator")

    delay_duration_list = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    delay_benchmark = DelayBenchmark()
    delay_benchmark.compose(
        benchmark="toffoli", 
        delay_duration_list=delay_duration_list
        )
    job_id_sim, job_id_op, job_id_meas = delay_benchmark.run(backend=backend, simulator=simulator)

    eval_res = EvaluateDelay(job_id_sim=job_id_sim, job_id_delay_op=job_id_op, job_id_delay_meas=job_id_meas, backend=backend, simulator=simulator, delay_duration_list=delay_duration_list)
    eval_res.result()
    state_fidelity_list = eval_res.state_fidelity()
    print(state_fidelity_list)



if __name__ == "__main__":
    test_evaluate_delay()