from typing import List

from qiskit.compiler import assemble
from qiskit.circuit import QuantumCircuit

from experiments.utils import get_IBM_backend, pickle_dump, PrepQASMBench
from multitasking_transpiler.palloq.compiler import multi_transpile

import logging
logger = logging.getLogger(__name__)


def execute_alap(size: str, names: List[str], backend, simulator, shots, nseed, save_path=None, instruction_durations=None):
    """
    size: 'small', 'medium', 'large'
    names: List of names of the benchmark circuits
    """
    _qc_list = PrepQASMBench.multi_circuits(size=size, names=names)

    qc_sim = multi_transpile(_qc_list, backend=simulator)
    qc = multi_transpile(
        _qc_list, backend=backend, basis_gates=['u1', 'u2', 'u3', 'cx'],
        layout_method='xtalk_adaptive', xtalk_prop={},
        )
    print("#############################################")
    print(qc)
    qc_alap = multi_transpile(
        _qc_list, backend=backend, scheduling_method='as_late_as_possible', 
        instruction_durations=instruction_durations, basis_gates=['u1', 'u2', 'u3', 'cx'], 
        layout_method='xtalk_adaptive', xtalk_prop={},
        )
    print("#############################################")
    print(qc_alap)

    job_sim, job, job_alap, job_id_sim, job_id, job_id_alap = _execute(backend, simulator, shots, qc_sim, qc, qc_alap, nseed)

    if save_path: 
        _save_experiments(qc_sim, qc, qc_alap, job_id_sim, job_id, job_id_alap, names, nseed, save_path)

    return job_sim, job, job_alap

def _execute(backend, simulator, shots, qc_sim, qc, qc_alap, nseed):
    qobj_sim = assemble(experiments=qc_sim, backend=simulator, shots=shots)
    job_sim = simulator.run(qobj_sim)
    job_id_sim = job_sim.job_id()
    job = []
    job_id = []
    job_alap = []
    job_id_alap = []
    for i in range(nseed):
        qobj = assemble(experiments=qc, backend=backend, shots=shots)
        _job = backend.run(qobj)
        job.append(_job)
        job_id.append(_job.job_id())

        
        qobj_alap = assemble(experiments=qc_alap, backend=backend, shots=shots)
        _job_alap = backend.run(qobj_alap)
        job_alap.append(_job_alap)
        job_id_alap.append(_job_alap.job_id())

    return job_sim, job, job_alap, job_id_sim, job_id, job_id_alap
        
def _save_experiments(qc_sim, qc, qc_alap, job_id_sim, job_id, job_id_alap, names, nseed, save_path):
    
    # compose experimental data
    experiments_data = {
        "simulator": {
            "qc": qc_sim,
            "job_id": job_id_sim, 
        }, 
        "non_scheduling": {
            "qc": qc,
            "job_id": job_id,
            "nseed": nseed,
        }, 
        "alap": {
            "qc": qc_alap,
            "job_id": job_id_alap,
            "nseed": nseed, 
        }, 
        "qc_names": names,
    }

    pickle_dump(experiments_data, save_path)