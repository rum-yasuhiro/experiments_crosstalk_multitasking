import numpy as np
import matplotlib.pyplot as plt

from qiskit import IBMQ
from qiskit.ignis.mitigation.measurement import (complete_meas_cal, tensored_meas_cal,
                                                 CompleteMeasFitter, TensoredMeasFitter)

from experiments.pickle_tools import pickle_dump, pickle_load


def get_result(jobfile_path, backend, provider=None):

    # define backend if backend is just a name of device
    if isinstance(backend, str) and provider is not None:
        backend = provider.get_backend(backend)
    elif isinstance(backend, str) and provider is None:
        raise ProviderUndefinedError('provider is undefined')

    # open job datum
    job_dictdict = pickle_load(jobfile_path)

    # qiskit transpiler
    qiskit_job_dict = job_dictdict['qiskit']
    qiskit_counts, qiskit_each_counts = _get_roe_mitigated_counts(
        qiskit_job_dict, backend)

    # xtalk adaptive transpiler
    xa_job_dict = job_dictdict['xtalk_aware']
    xa_counts, xa_each_counts = _get_roe_mitigated_counts(xa_job_dict, backend)

    # simulator
    # IBMQ.load_account()
    # sim_provider = IBMQ.get_provider(
    #     hub='ibm-q-keio', group='keio-internal', project='keio-students')
    # simulator = sim_provider.get_backend('ibmq_qasm_simulator')
    sim_job_dict = job_dictdict['simulator']
    sim_job = sim_job_dict['job']
    sim_counts, sim_each_counts = _count_each(sim_job.result().get_counts(0))

    res_dict = {
        'qiskit': {
            'counts': qiskit_counts,
            'each_counts': qiskit_each_counts,
        },
        'xtalk_aware': {
            'counts': xa_counts,
            'each_counts': xa_each_counts,
        },
        'simulator': {
            'counts': sim_counts,
            'each_counts': sim_each_counts,
            'circuit': sim_job_dict['circuit']
        },
    }

    return res_dict


def analyse(counts1, counts2, base_counts, shots=8192,  mode='js'):
    """
    mode:
        'kl' : Kullback-Leibler divergence
        'js': Jensen-Shannon divergence

    """
    uniform = [shots/len(base_counts)] * len(base_counts)

    if mode == 'kl':
        # counts1
        metric_1 = kl_divergence(counts1, base_counts)
        # counts2
        metric_2 = kl_divergence(counts2, base_counts)
        # uniform
        metric_uniform = kl_divergence(uniform, base_counts)

    elif mode == 'js':
        # counts1
        metric_1 = js_divergence(counts1, base_counts)
        # counts2
        metric_2 = js_divergence(counts2, base_counts)
        # uniform
        metric_uniform = js_divergence(uniform, base_counts)

    return metric_1, metric_2, metric_uniform


def kl_divergence(p, q):
    kl = 0
    for p_i, q_i in zip(p, q):
        kl_i = p_i * np.log(p_i / q_i) if q_i != 0 else 0
        kl += kl_i
    return kl


def js_divergence(p, q):
    m = [(p_i + q_i)/2 for p_i, q_i in zip(p, q)]
    js = 0
    # for p_i, q_i, m_i in zip(p, q, m):
    js_p = kl_divergence(p, m)
    js_q = kl_divergence(q, m)
    js = js_p / 2 + js_q / 2
    return js


def plot(listlist, output_path, xlabels=None):
    x_label_pos = []
    label_y = ['Uniform', 'qiskit_transpiler', 'Crosstalk_aware']
    colors = ['b', 'r', 'g']
    for i, _list in enumerate(listlist):
        x_pos = [i+0.8, i+1, i+1.2]
        for j in range(3):
            plt.bar(x_pos[j], _list[j], color=colors[j], width=0.2,
                    label=label_y[j], align="center")
        x_label_pos.append(i+1)
    if isinstance(xlabels, list):
        plt.xticks(x_label_pos, xlabels)
    plt.savefig(output_path)


def _get_roe_mitigated_counts(job_dict, backend):
    """
    Get Readout Error mitigated counts of each task in multi-programming
    """
    job = job_dict['job']
    job_cal = job_dict['job_cal']
    state_labels = job_dict['state_labels']

    # get the result of job
    results = job.result()

    # generate measurement caliburation fitter
    cal_results = job_cal.result()
    meas_fitter = CompleteMeasFitter(
        cal_results, state_labels, circlabel='mcal')
    meas_filter = meas_fitter.filter
    mitigated_results = meas_filter.apply(results)

    # get mitigated counts
    mitigated_counts = mitigated_results.get_counts(0)

    # divide each counts
    each_count = _count_each(mitigated_counts)

    return mitigated_counts, each_count


def _count_each(multi_count):
    bit_keys = list(multi_count.keys())
    regs = bit_keys[0].split()
    print(regs)
    each_count = []
    offset = 0
    limit = 0
    for register in regs[::-1]:
        num_bit = len(register)
        bin_list = [format(i, '0'+str(num_bit)+'b') for i in range(num_bit**2)]
        count = {}
        # initialize count dictionay
        for bin_key in bin_list:
            count[bin_key] = 0
        limit += num_bit
        for key, value in multi_count.items():
            key = key.replace(" ", "")
            for bin_key in bin_list:
                if offset == 0:
                    v = value if bin_key == key[-limit:] else 0
                    print(bin_key, key[-limit:], value, v)
                else:
                    v = value if bin_key == key[-limit:-offset] else 0
                    print(bin_key, key[-limit:-offset], value, v)
                count[bin_key] += v
        offset += num_bit
        each_count.append(count)
    return each_count


class ProviderUndefinedError(Exception):
    pass

# each_count = _count_each(d)


# for count in each_count:
#     print(count)
#     print(sum(list(count.values())))
