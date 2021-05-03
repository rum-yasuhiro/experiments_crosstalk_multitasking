from typing import List, Tuple, Dict, Union
from allocate_qc_manually import allocate_qc_manually
# from subdivided_phase_oracle_grover import spo_grover
# from utils.pickle_tools import pickle_dump

from qiskit import IBMQ, Aer, QuantumCircuit
from qiskit.compiler import transpile, assemble
from qiskit.circuit import Qubit
# from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq.ibmqfactory import IBMQProviderError

from tqdm import tqdm


def multi_exec(backend_name: str,
               #    initial_layout_list: List[Dict[Qubit, int]],
               experiments: List[Tuple[QuantumCircuit, Union[Dict[Qubit, int], List[Dict[Qubit, int]]]]],
               num_trial: int = 10,
               shots: int = 8192,
               job_id_path: str = None,
               hub='ibm-q-utokyo',
               group='keio-internal',
               project='keio-students',
               return_qc=False,
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
    backend = get_IBMQ_backends(backend_name,
                                hub=hub,
                                group=group,
                                project=project)
    # allocate prog-qubit to hw-qubit
    qc, layout = allocate_qc_manually(experiments)

    # # run on simulator
    # qobj = assemble(qc)
    # job_sim = simulator.run(qobj, shots=shots*num_trial)

    # run on real device
    transpiled = transpile(
        qc,
        initial_layout=layout,
        backend=backend,
        basis_gates=['id', 'rz', 'sx', 'x', 'cx', 'reset']
    )

    qc_list = [transpiled for _ in range(num_trial)]
    qobj = assemble(qc_list)
    job = backend.run(qobj, shots=shots)

    if job_id_path:
        job_id = job.job_id()
        # pickle_dump(job_id, job_id_path)

    if return_qc:
        return job, qc
    return job


def results(backend_name,
            job_id,
            num_trial,
            hub='ibm-q-utokyo',
            group='keio-internal',
            project='keio-students'
            ):
    backend = get_IBMQ_backends(backend_name,
                                hub=hub,
                                group=group,
                                project=project,
                                )

    ret_job = backend.retrieve_job(job_id)
    counts_list = [ret_job.result().get_counts(i)
                   for i in tqdm(range(num_trial))]
    return counts_list


def get_IBMQ_backends(backend_name: str,
                      hub='ibm-q-utokyo',
                      group='keio-internal',
                      project='keio-students'):

    try:
        provider = IBMQ.get_provider(
            hub=hub, group=group, project=project)
    except IBMQProviderError:
        IBMQ.load_account()
        provider = IBMQ.get_provider(
            hub=hub, group=group, project=project)

    quantumdevice = provider.get_backend(backend_name)

    return quantumdevice
