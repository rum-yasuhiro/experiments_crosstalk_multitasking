from qiskit import IBMQ
from experiments.result_analysis import (get_result, analyse, plot)


def run():
    name = "QFT_3-1_Toffoli-1"
    IBMQ.load_account()
    provider = IBMQ.get_provider(
        hub='ibm-q-keio', group='keio-internal', project='reservations')
    backend = provider.get_backend('ibmq_toronto')
    jobfile_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/jobfiles/ibmq_toronto/2020-09-13T11:54:25_QFT_3-1_Toffoli-1.pickle"

    result_dict = get_result(jobfile_path, backend)

    qiskit_dict = result_dict['qiskit']
    xa_dict = result_dict['xtalk_aware']
    sim_dict = result_dict['csimulatorounts']

    # analyse whole result
    js1, js2, js_uni = analyse(
        qiskit_dict['counts'], xa_dict['counts'], sim_dict['counts'])

    plot([[js_uni, js1, js2]])

    # analyse each results in multi-programming
    js_list = []
    for qis, xa, sim in zip(qiskit_dict['counts'], xa_dict['counts'], sim_dict['counts']):
        js1, js2, js_uni = analyse(qis, xa, sim)
        js_list.append([js_uni, js1, js2])
    output_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/plot/" + name + ".png"
    plot(js_list, output_path)


if __name__ == "__main__":
    run()
