from qiskit import IBMQ
from docs.multi_tasking import multitasking_transpile
from benchmark_circuits import make_benckmarks
from typing import List, Union, Dict, Callable, Any, Optional, Tuple


def run_experiments(data_file_path=None, multi_circuit_components=None):

    if not isinstance(multi_circuit_components, (List, Dict)):
        multi_circuit_components = {'Toffoli': 2,
                                    'Fredkin': 2,
                                    'QAOA_3': 2,
                                    'QAOA_4': 1,
                                    }

    circuit_list = make_benckmarks(multi_circuit_components)
    try:
        provider = IBMQ.get_provider(
            hub='ibm-q-keio', group='keio-internal', project='keio-students')
    except:
        IBMQ.load_account()
        provider = IBMQ.get_provider(
            hub='ibm-q-keio', group='keio-internal', project='keio-students')
    backend = provider.get_backend('ibmq_toronto')
    bprop = backend.properties()
    crosstalk_prop = _pickle_load(
        data_file_path) if data_file_path is not None else None

    transpiled_circ = multitasking_transpile(multi_circuits=circuit_list,
                                             backend=backend,
                                             backend_properties=bprop,
                                             crosstalk_prop=crosstalk_prop,
                                             )
    print(transpiled_circ)


def _pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj, f)


def _pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data


if __name__ == "__main__":
    run_experiments()
