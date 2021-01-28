from typing import List

from qiskit.compiler import transpile, assemble
from qiskit.circuit import QuantumCircuit

from experiments.utils import get_IBM_backend, pickle_dump
from multitasking_transpiler.palloq.compiler import multi_transpile
from .single_parallel_transpile import single_parallel_transpile

import logging
logger = logging.getLogger(__name__)
from pprint import pprint

def execute_xtalk(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path=None, instruction_durations=None):
    ## transpile each experiments
    # simulator
    multi_sim = multi_transpile(qc_list, backend=simulator)
    # Dense layout
    # single_dense, multi_dense, layouts_dense = single_parallel_transpile(qc_list, mode='dense', backend=backend, instruction_durations=None, xtalk_prop=None)
    # print("dense")
    # Noise adaptive layout
    single_na, multi_na, layouts_na = single_parallel_transpile(qc_list, mode='noise_adaptive', backend=backend, instruction_durations=None, xtalk_prop=None)
    pprint("noise-adaptive")
    # SABRE layout
    # single_sabre, multi_sabre, layouts_sabre = single_parallel_transpile(qc_list, mode='sabre', backend=backend, instruction_durations=None, xtalk_prop=None)
    # print("sabre")
    # Crosstalk-adaptive layout
    single_xtalk, multi_xtalk, layouts_xtalk = single_parallel_transpile(qc_list, mode='xtalk', backend=backend, instruction_durations=None, xtalk_prop=xtalk_prop)
    pprint("xtalk-adaptive")
    print("##############################################")
    print()

    # # execute each experiments
    # job_sim = _execute(single_exp=qc_list, multi_exp=multi_sim, backend=simulator, shots_single=shots_single, shots_multi=shots_multi)
    # job_dense = _execute(single_exp=single_dense, multi_exp=multi_dense, backend=backend, shots_single=shots_single, shots_multi=shots_multi)
    # job_na = _execute(single_exp=single_na, multi_exp=multi_na, backend=backend, shots_single=shots_single, shots_multi=shots_multi)
    # job_sabre = _execute(single_exp=single_sabre, multi_exp=multi_sabre, backend=backend, shots_single=shots_single, shots_multi=shots_multi)
    # job_xtalk = _execute(single_exp=single_xtalk, multi_exp=multi_xtalk, backend=backend, shots_single=shots_single, shots_multi=shots_multi)

    # if save_path: 
    #     _save_experiments( 
    #         qc_list, multi_sim, job_sim, 
    #         single_dense, multi_dense, job_dense, 
    #         single_na, multi_na, job_na, 
    #         single_sabre, multi_sabre, job_sabre, 
    #         single_xtalk, multi_xtalk, job_xtalk,
    #         backend, shots_single, shots_multi, save_path)

    # return job_sim, job_dense, job_na, single_sabre, job_xtalk

def _execute(single_exp, multi_exp, backend, shots_single, shots_multi):

    # run single qc jobs
    qobj_single = assemble(experiments=single_exp, backend=backend, shots=shots_single)
    job_single = backend.run(qobj_single)

    # run combined qc job
    qobj_multi = assemble(experiments=multi_exp, backend=backend, shots=shots_multi)
    job_multi = backend.run(qobj_multi)

    return job_single, job_multi


def _save_experiments( 
        qc_list, multi_sim, job_sim, 
        single_dense, multi_dense, job_dense, 
        single_na, multi_na, job_na, 
        single_sabre, multi_sabre, job_sabre, 
        single_xtalk, multi_xtalk, job_xtalk,
        backend, shots_single, shots_multi, save_path):

    job_sim_s, job_sim_m = job_sim
    job_dense_s, job_dense_m = job_dense
    job_na_s, job_na_m = job_na
    job_sabre_s, job_sabre_m = job_sabre
    job_xtalk_s, job_xtalk_m = job_xtalk

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
            "dense": {
                "qc": {
                    'single': single_dense, 
                    'multi': multi_dense
                },
                "job_id": {
                    'single': job_dense_s.job_id(),
                    'multi': job_dense_m.job_id()
                },  
            }, 
            "noise": {
                "qc": {
                    'single': single_na, 
                    'multi': multi_na
                },
                "job_id": {
                    'single': job_na_s.job_id(),
                    'multi': job_na_m.job_id()
                },  
            }, 
            "sabre": {
                "qc": {
                    'single': single_sabre, 
                    'multi': multi_sabre
                },
                "job_id": {
                    'single': job_sabre_s.job_id(),
                    'multi': job_sabre_m.job_id()
                },  
            }, 
            "xtalk": {
                "qc": {
                    'single': single_xtalk, 
                    'multi': multi_xtalk
                },
                "job_id": {
                    'single': job_xtalk_s.job_id(),
                    'multi': job_xtalk_m.job_id()
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

    print('make directory: ', dir_path)
    dir_path = os.path.dirname(save_path)
    os.mkdir(dir_path)
    pickle_dump(experiments_data, save_path)

    return experiments_data