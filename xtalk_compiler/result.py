import os
import glob

from experiments.utils import pickle_load, pickle_dump, get_IBM_backend, separate_multi_counts
from pprint import pprint


def result(dir_path, backend_name, save_path=None): 
    # get path to this file and parent dir
    job_files = glob.glob(dir_path+'/*.pickle')
    # job_files = job_dir

    # open job files
    job_id_set = []
    bench_name_list = []
    for job_file in job_files:
        job_data = pickle_load(job_file)
        job_id_set.append(job_data["job"])
        bench_name_list.append(job_data["bench_names"])

    # load ibmq backend
    backend = get_IBM_backend(backend_name)
    simulator = get_IBM_backend('ibmq_qasm_simulator')

    # retrieve jobs and  results
    # simulator
    counts_sim_set = _retrieve_result(job_id_set, bench_name_list, device=simulator, type='simulator')

    # Dense layout
    counts_dense_set = _retrieve_result(job_id_set, bench_name_list, device=backend, type='dense')

    # noise-adaptive layout
    counts_noise_set = _retrieve_result(job_id_set, bench_name_list, device=backend, type='noise')

    # sabre layout
    counts_sabre_set = _retrieve_result(job_id_set, bench_name_list, device=backend, type='sabre')

    # xtalk adaptive transpiler
    counts_xtalk_set = _retrieve_result(job_id_set, bench_name_list, device=backend, type='xtalk')
    
    if save_path: 
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path): 
            print('make directory: ', dir_path)
            os.mkdir(dir_path)
        _save_results(counts_sim_set, counts_dense_set, counts_noise_set, counts_sabre_set, counts_xtalk_set, save_path)

def _retrieve_result(job_id_set, bench_name_list, device, type):
    counts_set = []
    for job_ids, name_list in zip(job_id_set, bench_name_list): 
        try: 
            job_s = device.retrieve_job(job_ids[type]['job_id']['single'])
        except: 
            print('failed: ', job_ids[type]['job_id']['single'])
        try: 
            job_m = device.retrieve_job(job_ids[type]['job_id']['multi'])
        except: 
            print('failed: ', job_ids[type]['job_id']['multi'])
        counts_s_dict = {}
        counts_m_dict = {}

        try: 
            for i, qc in enumerate(job_ids[type]['qc']['single']):
                counts_s_dict[qc.name] = job_s.result().get_counts(i)
            counts_m = job_m.result().get_counts()
            counts_m_list, num_clbits = separate_multi_counts(counts_m)
            for qc_name, _counts_m, _bits in zip(name_list, counts_m_list[::-1], num_clbits[::-1]):
                counts_m_dict[qc_name] = _counts_m

            counts_set.append((counts_s_dict, counts_m_dict, name_list))
        except: 
            pass

    return counts_set

def _save_results(counts_sim_set, counts_dense_set, counts_noise_set, counts_sabre_set, counts_xtalk_set, save_path):
    result_dict = {
        'sim': counts_sim_set,
        'dense': counts_dense_set,
        'noise': counts_noise_set,
        'sabre': counts_sabre_set,
        'xtalk': counts_xtalk_set,
    }
    pickle_dump(result_dict, save_path)