from qiskit import IBMQ
from experiments.execute import run_experiments
from experiments.convert_error_information import value_to_ratio
from experiments.pickle_tools import pickle_dump, pickle_load


def run(multi_circuit_components, xtalk_path=None, reservation=False):
    """ 
    Args: 
        multi_circuit_components : benchmarking circuits 
    """

    # define backend
    backend_name = 'ibmq_toronto'
    IBMQ.load_account()
    if reservation:
        provider = IBMQ.get_provider(
            hub='ibm-q-keio', group='keio-internal', project='reservations')
    else:
        provider = IBMQ.get_provider(
            hub='ibm-q-keio', group='keio-internal', project='keio-students')
    backend = provider.get_backend(backend_name)

    #  crosstalk prop
    if xtalk_path is None:
        epc_path = "/Users/Yasuhiro/Documents/aqua/gp/errors_information/toronto_from20200903/xtalk_data_daily/epc/2020-10-11.pickle"
        epc_dict = pickle_load(epc_path)
        crosstalk_prop = value_to_ratio(epc_dict)
    else:
        crosstalk_prop = pickle_load(xtalk_path)

    jobfile_dir = "/Users/Yasuhiro/Documents/aqua/gp/experiments/jobfiles/ibmq_toronto/2020-10-11/"
    circ = run_experiments(
        jobfile_dir, multi_circuit_components=multi_circuit_components, backend=backend, crosstalk_prop=crosstalk_prop, shots=8192)


if __name__ == "__main__":

    # 論文には11量子ビットまでの実験しか掲載しなかったが、
    # その程度の量子ビット使用率だと crosstalk の影響を受けずに済むので
    # 10--18量子ビット以降の実験を追加で行う。
    multi_circuit_components_list = [
        {'Toffoli': 2, 'QAOA_3': 2},
        {'Toffoli': 2, 'QAOA_4': 2},
        # {'Toffoli_SWAP': 2, 'QAOA_3': 1},
        # {'Toffoli_SWAP': 1, 'QAOA_4': 1},
        {'Fredkin': 2, 'Toffoli': 2},
        # {'Fredkin': 2, 'Toffoli_SWAP': 1},
        # {'QFT_2': 1, 'QAOA_3': 1},
        # {'QFT_2': 1, 'QAOA_4': 1},
        {'QFT_2': 2, 'Toffoli': 2},
        # {'QFT_2': 1, 'Toffoli_SWAP': 1},
        # {'QFT_3': 1, 'QAOA_3': 1},
        # {'QFT_3': 1, 'QAOA_4': 1},
        {'QFT_3': 2, 'Toffoli': 2},
        # {'QFT_3': 1, 'Toffoli_SWAP': 1},
        # {'QFT_2': 1, 'QAOA_3': 1, 'Fredkin': 1},
        # {'QFT_2': 1, 'QAOA_3': 1, 'Toffoli': 1},
        # {'QFT_2': 1, 'QAOA_3': 1, 'Toffoli_SWAP': 1},
        # {'QFT_2': 1, 'QAOA_4': 1, 'Fredkin': 1},
        # {'QFT_2': 1, 'QAOA_4': 1, 'Toffoli': 1},
        # {'QFT_2': 1, 'QAOA_4': 1, 'Toffoli_SWAP': 1},
        {'QFT_2': 2, 'Toffoli': 2, 'Fredkin': 2},
        {'QFT_3': 2, 'Toffoli': 2, 'Fredkin': 2},
    ]

    for multi_circuit_components in multi_circuit_components_list:
        run(multi_circuit_components)
