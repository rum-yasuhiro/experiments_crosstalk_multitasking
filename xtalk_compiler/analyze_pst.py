import os
import glob

from experiments.utils import pickle_load, pickle_dump, get_IBM_backend, separate_multi_counts, pst


from pprint import pprint

def analyze_pst(result_path, save_path=None): 

    result_dict = pickle_load(result_path)
    counts_sim_set = result_dict['sim']
    counts_dense_set = result_dict['dense']
    counts_noise_set = result_dict['noise']
    counts_sabre_set = result_dict['sabre']
    counts_xtalk_set = result_dict['xtalk']
    
    # Dense layout
    pst_dense = _analyze_pst(counts_sim_set, counts_dense_set)

    # noise-adaptive layout
    pst_noise = _analyze_pst(counts_sim_set, counts_noise_set)

    # sabre layout
    pst_sabre = _analyze_pst(counts_sim_set, counts_sabre_set)

    # xtalk adaptive transpiler
    pst_xtalk = _analyze_pst(counts_sim_set, counts_xtalk_set)

    eval_dict = {
        'dense': pst_dense,
        'noise': pst_noise,
        'sabre': pst_sabre,
        'xtalk': pst_xtalk
    }
    if save_path: 
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path): 
            print('make directory: ', dir_path)
            os.mkdir(dir_path)
        pickle_dump(eval_dict, save_path)


def _analyze_pst(counts_sim_set, counts_set): 
    pst_dict_dict = {}
    for sim_set, counts in zip(counts_sim_set, counts_set):
        counts_sim_s, counts_sim_m, name_list_sim = sim_set
        counts_s, counts_m, name_list = counts
        pst_dict = {}

        for qc_name in name_list:
            try: 
                pst_s = pst(counts_s[qc_name], counts_sim_s[qc_name])
            except: 
                pst_s = None
            try: 
                pst_m = pst(counts_m[qc_name], counts_sim_s[qc_name])
            except:
                pst_m = None
            pst_dict[qc_name] = {'single': pst_s, 'multi': pst_m}
        pst_dict_dict[tuple(name_list)] = pst_dict
    return pst_dict_dict