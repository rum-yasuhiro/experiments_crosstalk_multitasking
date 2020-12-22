from typing import List

from qiskit.compiler import transpile, assemble
from qiskit.circuit import QuantumCircuit

from experiments.utils import get_IBM_backend, pickle_dump, PrepQASMBench
from multitasking_transpiler.palloq.compiler import multi_transpile

import logging
logger = logging.getLogger(__name__)

def execute_xtalk(size: str, names: List[str], backend, simulator, shots, nseed, save_path=None, instruction_durations=None):
    """
    size: 'small', 'medium', 'large', None
        if None, search all size of directory 
    names: List of names of the benchmark circuits
    """
    # define the benchmark circuits set
    qc_list = PrepQASMBench.multi_circuits(size=size, names=names)

    ## transpile each experiments
    # simulator
    qc_sim = multi_transpile(qc_list, backend=simulator)
    
    # # Single execution
    # qcs_signle = transpile(
    #     qc_list, backend=backend, optimization_level=3, 
    #     basis_gates=['id', 'u1', 'u2', 'u3', 'cx', 'delay', 'u3cx', 'barrier', 'snapshot', 'measure', 'reset'],
    #     )

    # Parallel execution by qiskit transpiler with level3 preset Pass Manager
    qc_opt3 = multi_transpile(
        qc_list, backend=backend, optimization_level=3, 
        basis_gates=['id', 'u1', 'u2', 'u3', 'cx', 'delay', 'u3cx', 'barrier', 'snapshot', 'measure', 'reset'],
        layout_method='xtalk_adaptive', xtalk_prop={},
        )

    # Multi Pass Manager
    qc_multi = multi_transpile(
        qc_list, backend=backend,
        instruction_durations=instruction_durations, 
        basis_gates=['id', 'u1', 'u2', 'u3', 'cx', 'delay', 'u3cx', 'barrier', 'snapshot', 'measure', 'reset'], 
        layout_method='xtalk_adaptive', xtalk_prop={},
        )

    # Crosstalk-adaptive layout
    qc_xtalk = multi_transpile(
        qc_list, backend=backend,
        instruction_durations=instruction_durations, 
        basis_gates=['id', 'u1', 'u2', 'u3', 'cx', 'delay', 'u3cx', 'barrier', 'snapshot', 'measure', 'reset'], 
        layout_method='xtalk_adaptive', xtalk_prop={},
        )

    # execute all transpiled experiments
    jobs, job_ids = _execute(
                        backend, simulator, shots, 
                        qc_list, qc_sim, qc_opt3, 
                        qc_multi, qc_xtalk, nseed
                        )
    
    transpiled_qcs = ()

    if save_path: 
        _save_experiments(transpiled_qcs, job_ids, names, nseed, save_path)

    return job_sim, job, job_multi

def _execute(backend, simulator, shots, qc_list, qc_sim, qc_opt3, qc_multi, qc_xtalk, nseed):
    # execute job on simulator
    qobj_sim = assemble(experiments=qc_sim, backend=simulator, shots=shots)
    job_sim = simulator.run(qobj_sim)
    job_id_sim = job_sim.job_id()

    # execute on IBM Q Backend
    job = []
    job_multi = []
    for i in range(nseed):
        qobj = assemble(experiments=qc, backend=backend, shots=shots)
        _job = backend.run(qobj)
        job.append(_job)
        
        qobj_multi = assemble(experiments=qc_multi, backend=backend, shots=shots)
        _job_multi = backend.run(qobj_multi)
        job_multi.append(_job_multi)

    job_id = 
    return (job_sim, job, job_multi), (job_id_sim, job_id, job_id_multi)
        
def _save_experiments(transpiled_qcs, job_ids, names, nseed, save_path):
    
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
        "multi": {
            "qc": qc_multi,
            "job_id": job_id_multi,
            "nseed": nseed, 
        }, 
        "qc_names": names,
    }

    pickle_dump(experiments_data, save_path)