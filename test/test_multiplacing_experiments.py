from experiments.multi_placing.experiments import run_distance, result_distance, plot_box
from experiments.multi_placing.toffoli_circuit import toffoli_circuit


def test_run_distance():
    backend_name = 'ibmq_qasm_simulator'

    toffoli = toffoli_circuit()
    adj_hwqubits = {(1, 2, 3): [(4, 5, 6), (7, 8, 9)],
                    (10, 11, 12): [(13, 14, 15), (16, 17, 18)]
                    }

    jobs = run_distance(backend_name, toffoli, adj_hwqubits)

    print(jobs)
