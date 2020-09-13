from qiskit import IBMQ
from experiments.result_analysis import (get_result, analyse, plot)

from experiments.pickle_tools import pickle_dump, pickle_load


def run():
    name = "Toffoli_QAOA4"
    IBMQ.load_account()
    provider = IBMQ.get_provider(
        hub='ibm-q-keio', group='keio-internal', project='reservations')
    backend = provider.get_backend('ibmq_toronto')
    jobfile_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/jobfiles/ibmq_toronto/2020-09-13T12:39:32_Toffoli-1_QAOA_4-1.pickle"

    # result_dict = get_result(jobfile_path, backend)
    ################################################################
    job_dictdict = pickle_load(jobfile_path)
    jobfile_dict = {
        'qiskit': {
            'job': "5f5d945c0c8a97001bd9e444",
            'circuit': job_dictdict['qiskit']['circuit'],
            'job_cal': job_dictdict['qiskit']['job_cal'],
            'state_labels': job_dictdict['qiskit']['state_labels'],
        },
        'xtalk_aware': {
            'job': "5f5d9463ac2d220019fdd974",
            'circuit': job_dictdict['xtalk_aware']['circuit'],
            'job_cal': job_dictdict['xtalk_aware']['job_cal'],
            'state_labels': job_dictdict['xtalk_aware']['state_labels'],
        },
        'simulator': {
            'job': job_dictdict['simulator']['job'],
            'circuit': job_dictdict['simulator']['circuit']
        }
    }
    result_dict = get_result(jobfile_path, backend, jobfile_dict=jobfile_dict)

    ################################################################
    qiskit_dict = result_dict['qiskit']
    xa_dict = result_dict['xtalk_aware']
    sim_dict = result_dict['simulator']

    # analyse whole result
    print("################################################################")
    print(qiskit_dict['counts'])
    print(xa_dict['counts'])
    print(sim_dict['counts'])
    print("################################################################")
    js1_total, js2_total, js_uni_total = analyse(
        _sort_by_key(qiskit_dict['counts']), _sort_by_key(xa_dict['counts']), _sort_by_key(sim_dict['counts']), num_bit=6)
    output_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/plot/" + name + ".png"
    plot([[js_uni_total, js1_total, js2_total]], output_path)

    # analyse each results in multi-programming
    js_list = []
    num_bit_list = [4, 3]
    for qis, xa, sim, num_bit in zip(qiskit_dict['each_counts'], xa_dict['each_counts'], sim_dict['each_counts'], num_bit_list):
        js1_i, js2_i, js_uni_i = analyse(_sort_by_key(
            qis), _sort_by_key(xa), _sort_by_key(sim), num_bit=num_bit)
        js_list.append([js1_i, js2_i, js_uni_i])
    output_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/plot/" + name + "_each.png"
    plot(listlist=js_list, output_path=output_path)

    res_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/jsd.pickle"
    try:
        res = pickle_load(res_path)
    except:
        res = {}
    res[name] = [js_uni_total, js1_total, js2_total]
    pickle_dump(res, res_path)


def _sort_by_key(_dict):
    new_dict = {}
    for key in list(_dict.keys()):
        new_dict[key.replace(" ", "")] = _dict[key]

    keys = list(new_dict.keys())
    num_bit = len(keys[0])
    bin_list = [format(i, '0'+str(num_bit)+'b') for i in range(2**num_bit)]
    for _bin in bin_list:
        if _bin not in keys:
            new_dict[_bin] = 0

    val_list = [item[1]
                for item in sorted(new_dict.items(), key=lambda x: x[0])]
    return val_list


if __name__ == "__main__":
    run()
