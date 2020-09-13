from typing import List, Union, Dict, Callable, Any, Optional, Tuple
import datetime
import logging
from time import time
from qiskit import IBMQ
from qiskit.compiler import assemble
from qiskit.qobj.utils import MeasLevel, MeasReturnType
from multitasking_transpiler.docs.multi_tasking import multitasking_transpile
from experiments.benchmark_circuits import make_benckmarks
from experiments.readout_error_mitigation import run_meas_mitigation
from experiments.notify import send_slack
import pickle

logger = logging.getLogger(__name__)


def _log_submission_time(start_time, end_time):
    log_msg = ("Total Job Submission Time - %.5f (ms)"
               % ((end_time - start_time) * 1000))
    logger.info(log_msg)


def run_experiments(jobfile_dir, multi_circuit_components=None, backend=None, shots=1024, crosstalk_info_filepath=None, crosstalk_prop=None):
    if backend is None:
        try:
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="keio-students"
            )
        except:
            IBMQ.load_account()
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="keio-students"
            )
        backend = provider.get_backend('ibmq_qasm_simulator')
        crosstalk_prop = None
        optimization_level = None
    elif isinstance(backend, str):
        try:
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="keio-students"
            )
        except:
            IBMQ.load_account()
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="keio-students"
            )
        try:
            backend = provider.get_backend(backend)
            bprop = backend.properties()
        except:
            backend = provider.get_backend('ibmq_qasm_simulator')
            crosstalk_prop = None
            optimization_level = None
    job, tranpiled_circuit = _run_experiments(multi_circuit_components,
                                              backend, shots=shots, optimization_level=3, returnCircuit=True)
    job_cal, state_labels = run_meas_mitigation(tranpiled_circuit, backend)
    job_xtalk, circuit_xtalk = _run_experiments(multi_circuit_components, backend,
                                                crosstalk_info_filepath=crosstalk_info_filepath, crosstalk_prop=crosstalk_prop, shots=shots, returnCircuit=True)
    job_xtalk_cal, state_labels_xtalk = run_meas_mitigation(
        circuit_xtalk, backend)
    IBMQ.load_account()
    provider = IBMQ.get_provider(
        hub="ibm-q-keio", group="keio-internal", project="keio-students")
    job_sim, original_circuit = _run_experiments(multi_circuit_components, backend=provider.get_backend('ibmq_qasm_simulator'),
                                                 optimization_level=3,
                                                 shots=shots, returnCircuit=True)

    # get the job id
    job_id = job.job_id()
    job_id_xtalk = job_xtalk.job_id()
    job_id_sim = job_sim.job_id()

    return_dict = {
        'qiskit': {
            'job': job,
            'circuit': tranpiled_circuit,
            'job_cal': job_cal,
            'state_labels': state_labels,
        },
        'xtalk_aware': {
            'job': job_cal,
            'circuit': circuit_xtalk,
            'job_cal': job_xtalk_cal,
            'state_labels': state_labels_xtalk,
        },
        'simulator': {
            'job': job_sim,
            'circuit': original_circuit
        }
    }

    execution_datetime = datetime.datetime.now().isoformat(timespec='seconds')

    benchmarking_circuits = ''
    for circ, num in multi_circuit_components.items():
        benchmarking_circuits = benchmarking_circuits + \
            '_' + str(circ) + '-' + str(num)
    jobfile_path = jobfile_dir + execution_datetime + \
        benchmarking_circuits + ".pickle"
    _pickle_dump(return_dict, jobfile_path)

    # url = "https://hooks.slack.com/services/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"
    # send_slack('Experiments was done.', url)


def _run_experiments(multi_circuit_components=None, backend=None, crosstalk_prop=None, crosstalk_info_filepath=None, returnCircuit=False, onlyCircuit=False,
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
        multi_circuit_components = {'QFT_2': 1,
                                    'QFT_3': 1,
                                    'Toffoli': 2,
                                    'Fredkin': 2,
                                    'QAOA_3': 2,
                                    'QAOA_4': 1,
                                    }

    circuit_list = make_benckmarks(multi_circuit_components)
    if crosstalk_prop is None and isinstance(crosstalk_info_filepath, str):
        cprop = _pickle_load(crosstalk_info_filepath)
    else:
        cprop = crosstalk_prop
    try:
        bprop = backend.properties()
    except:
        bprop = None

    print("Crosstalk", cprop)

    experiments = multitasking_transpile(multi_circuits=circuit_list,
                                         backend=backend,
                                         backend_properties=bprop,
                                         crosstalk_prop=cprop,
                                         optimization_level=optimization_level,
                                         )

    if not onlyCircuit:
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
    return experiments


def _pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj, f)


def _pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data


if __name__ == "__main__":
    backend_name = 'ibmq_toronto'
    # backend = provider.get_backend(backend)
    multi_circuit_components = {'QFT_2': 1,
                                'Toffoli_SWAP': 1,
                                'QAOA_3': 1,
                                }
    crosstalk_prop = {(1, 4): {(7, 10): 2.007855196208965},
                      (2, 3): {(5, 8): 2.2562876383458272},
                      (5, 8): {(2, 3): 4.407297774712314},
                      (7, 10): {(1, 4): 1.6495182758869775, (12, 15): 4.460931414407089},
                      (10, 12): {(4, 7): 2.3646024088589743, (13, 14): 5.158153837151825, (15, 18): 3.4005240793851117},
                      (11, 14): {(12, 13): 1.5815379245637133},
                      (12, 13): {(11, 14): 1.9429829606099185},
                      (12, 15): {(7, 10): 3.3721649065903803, (13, 14): 3.4767073109961886},
                      (13, 14): {(8, 11): 1.9294023975707386, (10, 12): 3.786805218079993, (12, 15): 6.021972074875656},
                      (15, 18): {(10, 12): 1.9467061167117026}
                      }

    circ = run_experiments(
        multi_circuit_components=multi_circuit_components, backend=backend_name, crosstalk_prop=crosstalk_prop, shots=8192)
