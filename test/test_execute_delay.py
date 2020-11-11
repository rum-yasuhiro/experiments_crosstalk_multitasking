from qiskit.circuit import QuantumCircuit

from experiments.test.utils import get_IBM_backend
from experiments.waiting_duration import execute_bench

def test_execute(): 
    backend = get_IBM_backend("ibmq_rome")
    simulator = get_IBM_backend("ibmq_qasm_simulator")

    
    qc = QuantumCircuit(3, 3, name="qc_name_is")
    qc.x(0)
    qc.x(1)
    qc.x(2)
    qc.measure_all()


    job_sim, job_delay_op_list, job_delay_meas_list = execute_bench(qc, backend, simulator, initial_layout=[0, 1, 2])


if __name__ == "__main__":
    test_execute()