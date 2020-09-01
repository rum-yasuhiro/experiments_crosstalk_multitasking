from typing import List, Union, Dict, Callable, Any, Optional, Tuple
import datetime
import logging
from time import time
from qiskit import IBMQ
from qiskit.compiler import assemble
from qiskit.qobj.utils import MeasLevel, MeasReturnType
from docs.multi_tasking import multitasking_transpile
from benchmark_circuits import make_benckmarks

logger = logging.getLogger(__name__)


def _log_submission_time(start_time, end_time):
    log_msg = ("Total Job Submission Time - %.5f (ms)"
               % ((end_time - start_time) * 1000))
    logger.info(log_msg)


def run_experiments(multi_circuit_components=None, backend=None, crosstalk_info_filepath=None, crosstalk_prop=None, returnCircuit=False):

    job = _run_experiments(multi_circuit_components,
                           backend, optimization_level=3, returnCircuit=returnCircuit)
    job_xtalk = _run_experiments(multi_circuit_components, backend,
                                 crosstalk_info_filepath, crosstalk_prop, returnCircuit=returnCircuit)
    job_sim = _run_experiments(multi_circuit_components)

    job_id = job.job_id()
    job_id_xtalk = job_xtalk.job_id()
    job_id_sim = job_sim.job_id()
    '''
    Readout error mitigation用のjobも用意する
    '''
    execution_datetime = datetime.datetime.now().isoformat(timespec='seconds')

    benchmarking_circuits = ''
    for circ, num for multi_circuit_components.items():
        benchmarking_circuits = benchmarking_circuits + \
            '_' + str(circ) + '-' + str(num)


def _run_experiments(multi_circuit_components=None, backend=None, crosstalk_prop=None, crosstalk_info_filepath=None, optimization_level=None, returnCircuit=False,
                     basis_gates=None, coupling_map=None,  # circuit transpile options
                     backend_properties=None, initial_layout=None,
                     seed_transpiler=None, optimization_level=None, pass_manager=None,
                     qobj_id=None, qobj_header=None, shots=1024,  # common run options
                     memory=False, max_credits=10, seed_simulator=None,
                     default_qubit_los=None, default_meas_los=None,  # schedule run options
                     schedule_los=None, meas_level=MeasLevel.CLASSIFIED,
                     meas_return=MeasReturnType.AVERAGE,
                     memory_slots=None, memory_slot_size=100, rep_time=None, rep_delay=None,
                     parameter_binds=None, schedule_circuit=False, inst_map=None, meas_map=None,
                     scheduling_method=None, init_qubits=None,
                     **run_config
                     ):

    if not isinstance(multi_circuit_components, (List, Dict)):
        multi_circuit_components = {'Toffoli': 2,
                                    'Fredkin': 2,
                                    'QAOA_3': 2,
                                    'QAOA_4': 1,
                                    }

    circuit_list = make_benckmarks(multi_circuit_components)
    if crosstalk_prop is None and crosstalk_info_filepath is not None:
        cprop = _pickle_load(crosstalk_info_filepath)
    else:
        cprop = crosstalk_prop
    if backend is None:
        try:
            provider = IBMQ.get_provider(
                hub='ibm-q-keio', group='keio-internal', project='keio-students')
        except:
            IBMQ.load_account()
            provider = IBMQ.get_provider(
                hub='ibm-q-keio', group='keio-internal', project='keio-students')
        backend = provider.get_backend('ibmq_qasm_simulator')
        crosstalk_prop = None
        optimization_level = None
    else:
        try:
            bprop = backend.properties()
        except:
            bprop = None
            crosstalk_prop = None
            optimization_level = None

    experiments = multitasking_transpile(multi_circuits=circuit_list,
                                         backend=backend,
                                         backend_properties=bprop,
                                         crosstalk_prop=cprop,
                                         optimization_level=optimization_level,
                                         )

    qobj = assemble(experiments,
                    qobj_id=qobj_id,
                    qobj_header=qobj_header,
                    shots=shots,
                    memory=memory,
                    max_credits=max_credits,
                    seed_simulator=seed_simulator,
                    default_qubit_los=default_qubit_los,
                    default_meas_los=default_meas_los,
                    schedule_los=schedule_los,
                    meas_level=meas_level,
                    meas_return=meas_return,
                    memory_slots=memory_slots,
                    memory_slot_size=memory_slot_size,
                    rep_time=rep_time,
                    rep_delay=rep_delay,
                    parameter_binds=parameter_binds,
                    backend=backend,
                    init_qubits=init_qubits,
                    **run_config)

    # executing the circuits on the backend and returning the job
    start_time = time()
    job = backend.run(qobj, **run_config)
    end_time = time()
    _log_submission_time(start_time, end_time)

    if returnCircuit:
        return job, experiments
    return job


def _pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj, f)


def _pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data


if __name__ == "__main__":
    multi_circuit_components = {'Toffoli': 1,
                                'Fredkin': 1,
                                'QAOA_3': 0,
                                'QAOA_4': 1,
                                }

    job, circ = _run_experiments(
        multi_circuit_components=multi_circuit_components, shots=8192, returnCircuit=True)
    counts = job.result().get_counts()
    print(counts)
    if isinstance(circ, list):
        print(circ[0])
    else:
        print(circ)
