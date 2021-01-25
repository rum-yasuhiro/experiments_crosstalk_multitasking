from typing import List
import os

from qiskit.compiler import transpile, assemble
from qiskit.circuit import QuantumCircuit

from experiments.utils import get_IBM_backend, pickle_dump
from multitasking_transpiler.palloq.compiler import multi_transpile
from experiments.scheduling.single_parallel_transpile import single_parallel_transpile
from qiskit.transpiler import InstructionDurations

import logging
logger = logging.getLogger(__name__)

def execute_sched(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path=None):
    
    instruction_durations = InstructionDurations.from_backend(backend)

    ## transpile each experiments
    # simulator
    multi_sim = multi_transpile(qc_list, backend=simulator)
    # non Scheduled
    single_nonsched, multi_nonsched = single_parallel_transpile(qc_list, backend=backend, layout_method='xtalk_adaptive',  instruction_durations=instruction_durations, xtalk_prop=xtalk_prop)
    # ALAP Scheduled
    single_alap, multi_alap = single_parallel_transpile(qc_list, backend=backend, layout_method='xtalk_adaptive', scheduling_method='as_late_as_possible', instruction_durations=instruction_durations, xtalk_prop=xtalk_prop)
    

    # execute each experiments
    job_sim = _execute(sigle_exp=qc_list, multi_exp=multi_sim, backend=simulator, shots_single=shots_single, shots_multi=shots_multi)
    job_nonsched = _execute(sigle_exp=single_nonsched, multi_exp=multi_nonsched, backend=backend, shots_single=shots_single, shots_multi=shots_multi)
    job_alap = _execute(sigle_exp=single_alap, multi_exp=multi_alap, backend=backend, shots_single=shots_single, shots_multi=shots_multi)
    

    if save_path: 
        _save_experiments( 
            qc_list, multi_sim, job_sim, 
            single_nonsched, multi_nonsched, job_nonsched, 
            single_alap, multi_alap, job_alap, 
            backend, shots_single, shots_multi, save_path)

    return job_sim, job_nonsched, job_alap

def _execute(sigle_exp, multi_exp, backend, shots_single, shots_multi):
    
    # run single qc jobs
    qobj_single = assemble(experiments=sigle_exp, backend=backend, shots=shots_single)
    job_single = backend.run(qobj_single)

    # run combined qc job
    qobj_multi = assemble(experiments=multi_exp, backend=backend, shots=shots_multi)
    job_multi = backend.run(qobj_multi)

    return job_single, job_multi


def _save_experiments( 
        qc_list, multi_sim, job_sim, 
        single_nonsched, multi_nonsched, job_nonsched, 
        single_alap, multi_alap, job_alap, 
        backend, shots_single, shots_multi, save_path):

    job_sim_s, job_sim_m = job_sim
    job_non_s, job_non_m = job_nonsched
    job_alap_s, job_alap_m = job_alap

    name_list = [qc.name for qc in qc_list]
    # compose experimental data
    experiments_data = {
        "job": {
            "simulator": {
                "qc": {
                    'single': qc_list, 
                    'multi': multi_sim
                },
                "job_id": {
                    'single': job_sim_s.job_id(),
                    'multi': job_sim_m.job_id(),
                },  
            }, 
            "nonsched": {
                "qc": {
                    'single': single_nonsched, 
                    'multi': multi_nonsched
                },
                "job_id": {
                    'single': job_non_s.job_id(),
                    'multi': job_non_m.job_id()
                },  
            }, 
            "alap": {
                "qc": {
                    'single': single_alap, 
                    'multi': multi_alap
                },
                "job_id": {
                    'single': job_alap_s.job_id(),
                    'multi': job_alap_m.job_id()
                },  
            }, 
        },
        "bench_names": name_list,
        "backend": backend.name(), 
        'shots': {
            'single': shots_single, 
            'multi': shots_multi
        }
    }

    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path): 
        print('make directory: ', dir_path)
        os.mkdir(dir_path)
    pickle_dump(experiments_data, save_path)

    return experiments_data