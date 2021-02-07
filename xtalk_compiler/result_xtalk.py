import os
import glob

from experiments.utils import pickle_load, pickle_dump, get_IBM_backend, separate_multi_counts, jsd


from pprint import pprint

def result_xtalk(dir_path, backend_name, save_path=None): 
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

    # retrieve jobs and get load results
    
    # simulator
    counts_sim_set = _retrieve_load_result(job_id_set, bench_name_list, device=simulator, type='simulator')

    # Dense layout
    counts_set_dense = _retrieve_load_result(job_id_set, bench_name_list, device=backend, type='dense')
    # print(counts_set_dense)
    jsd_dense = _analyze_results(counts_sim_set, counts_set_dense)
    pprint(jsd_dense)

    # noise-adaptive layout
    counts_set_noise = _retrieve_load_result(job_id_set, bench_name_list, device=backend, type='noise')
    # print(counts_set_noise)
    jsd_noise = _analyze_results(counts_sim_set, counts_set_noise)
    pprint(jsd_noise)

    # sabre layout
    counts_set_sabre = _retrieve_load_result(job_id_set, bench_name_list, device=backend, type='sabre')
    # print(counts_set_sabre)
    jsd_sabre = _analyze_results(counts_sim_set, counts_set_sabre)
    pprint(jsd_sabre)

    # xtalk adaptive transpiler
    counts_set_xtalk = _retrieve_load_result(job_id_set, bench_name_list, device=backend, type='xtalk')
    # print(counts_set_xtalk)
    jsd_xtalk = _analyze_results(counts_sim_set, counts_set_xtalk)
    pprint(jsd_xtalk)

    eval_dict = {
        'dense': jsd_dense,
        'noise': jsd_noise,
        'sabre': jsd_sabre,
        'xtalk': jsd_xtalk
    }
    if save_path: 
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path): 
            print('make directory: ', dir_path)
            os.mkdir(dir_path)
        pickle_dump(eval_dict, save_path)

def _retrieve_load_result(job_id_set, bench_name_list, device, type): 
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

        try: 
            for i, qc in enumerate(job_ids[type]['qc']['single']):
                counts_s_dict[qc.name] = job_s.result().get_counts(i)
            counts_m = job_m.result().get_counts()
            counts_set.append((counts_s_dict, counts_m, name_list))
        except: 
            pass

    return counts_set

def _analyze_results(counts_sim_set, counts_set): 
    jsd_dict_list = []
    for sim_set, counts in zip(counts_sim_set, counts_set):
        counts_sim_s, counts_sim_m, _ = sim_set
        counts_s, counts_m, name_list = counts

        counts_m_list, num_clbits = separate_multi_counts(counts_m)
        jsd_dict = {}
        i = 0
        print(counts_sim_s)
        print(counts_s)
        for qc_name, _counts_m, _bits in zip(name_list, counts_m_list[::-1], num_clbits[::-1]):
            try: 
                jsd_s = jsd(counts_sim_s[qc_name], counts_s[qc_name], _bits)
            except: 
                jsd_s = 0
            try: 
                jsd_m = jsd(counts_sim_s[qc_name], _counts_m, _bits)
            except: 
                jsd_m = 0
            
            try: 
                jsd_u = jsd(counts_sim_s[qc_name], 'uni', _bits)
            except:
                jsd_u = 0
            jsd_dict[qc_name] = {'single': jsd_s, 'multi': jsd_m, 'uniform': jsd_u}
        jsd_dict_list.append(jsd_dict)
    return jsd_dict_list

