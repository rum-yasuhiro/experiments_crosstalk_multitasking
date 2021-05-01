from typing import Dict, Tuple, List
from multi_exec import multi_exec, results

from qiskit import QuantumCircuit


def run_distance(backend_name: str,
                 circuit: QuantumCircuit,
                 adj_hwqubits: Dict[Tuple, List[Tuple[int]]],
                 num_trial: int = 100,
                 shots: int = 1000,
                 job_id_path: str = None,
                 hub='ibm-q-utokyo',
                 group='keio-internal',
                 project='keio-students',
                 sendjob_remote=True,
                 return_qc=False,
                 ):

    job_all = {}
    for targ, adj_list in adj_hwqubits:
        experiments = []
        job_partial = []

        # prepare target circuit with measurement
        qc0 = circuit.copy()
        qc0.remove_final_measurements()
        qc0.measure_active()

        qubits = qc0.qubit
        layout = {}
        for hw, pg in zip(qubits, targ):
            layout[hw] = pg

        experiments.append((qc0, layout))

        for adj in adj_list:
            # prepare adjacent circuit without measurement
            qc_i = circuit.copy()
            qc_i.remove_final_measurements()

            qubits_i = qc_i.qubits

            layout_i = {}
            for hw, pg in zip(qubits_i, adj):
                layout_i[hw] = pg

            experiments.append((qc_i, layout_i))

        job = multi_exec(
            backend_name,
            experiments,
            num_trial,
            shots,
            job_id_path,
            hub=hub,
            group=group,
            project=project,
        )
        job_partial.append(job.job_id())

    job_all[targ] = job_partial

    return job_all


def result_distance(targ_job_id: Dict[Tuple[int], List[str]], job_sim):

    for targ, job_ids in targ_job_id:


def run_multiple():
    pass
