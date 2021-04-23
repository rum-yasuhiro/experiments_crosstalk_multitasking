from typing import List, Dict
from allocate_qc_manually import allocate_qc_manually
from subdivided_phase_oracle_grover import spo_grover
# from utils.pickle_tools import pickle_dump

from qiskit import IBMQ, Aer, QuantumCircuit
from qiskit.compiler import assemble
from qiskit.circuit import Qubit
# from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor


def multi_exec(backend_name: str,
               #    initial_layout_list: List[Dict[Qubit, int]],
               experiments: Dict[QuantumCircuit, Dict[Qubit, int]],
               num_trial: int = 10,
               shots: int = 8192,
               job_id_path: str = None
               ):
    """
    単一実行と並列実行で測定量子ビット数は同じなので
    理論的な解空間は同じだが、
    実験ごとのサンプリング回数は調整の必要がありそう

    Args:
        job_id_path: save file path for job_id. The file extention is .pickle
        counts_path: save file path for counts of qc
        show_pd: wether or not to show plot of the probability distribution
    Return:
        (Job, IBMQJob)
    """
    # get IBM Q backend
    simulator, backend = get_IBMQ_backends(backend_name)

    # # prepare Grover cirrcuit with measurement
    # multi_qc = {}
    # for i, _layout in enumerate(initial_layout_list):
    #     if i == 0:
    #         grov = spo_grover(num_data=4, measure=True)
    #     else:
    #         grov = spo_grover(num_data=4, measure=False)
    #     multi_qc[grov] = _layout

    # allocate prog-qubit to hw-qubit
    qc = allocate_qc_manually(multi_qc)

    # run on simulator
    qobj = assemble(qc)
    job_sim = simulator.run(qobj, shots=shots)

    # run on real device
    qc_list = [qc for _ in range(num_trial)]
    qobj = assemble(qc_list)
    job = backend.run(qobj, shots=shots)

    if job_id_path:
        job_id = job.job_id()
        # pickle_dump(job_id, job_id_path)

    return job_sim, job


def get_IBMQ_backends(backend_name: str, hub='ibm-q-utokyo',
                      group='keio-internal', project='keio-students'):
    IBMQ.load_account()
    provider = IBMQ.get_provider(
        hub=hub, group=group, project=project)

    classicalsimulator = Aer.get_backend('qasm_simulator')
    quantumdevice = provider.get_backend(backend_name)

    return classicalsimulator, quantumdevice
