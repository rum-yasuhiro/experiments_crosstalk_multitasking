import os
from matplotlib import pyplot as plt

from experiments.utils import pickle_dump, pickle_load, jsd, statistics

def evaluate_alap(data_dir, save_eval_path=None): 
    """
    result_data = {
        "simulator": {
            "qc": qc_sim,
            "result": result_sim,
            "count": count_sim,
        }, 
        "non_scheduling": {
            "qc": qc,
            "result": result_list,
            "count": count_list,
        }, 
        "alap": {
            "qc": qc_alap,
            "result": result_alap_list,
            "count": count_alap_list, 
        }, 
        "qc_names": qc_names,
        "date": date, 
    }
    """
    result_list = [pickle_load(data_dir + "/" + f) for f in os.listdir(data_dir)]
    jsd_dict = convert_to_jsd(result_list)

    if save_eval_path: 
        pickle_dump(jsd_dict, save_eval_path)
    
    return jsd_dict
    

def convert_to_jsd(resilt_list):
    eval_dict = {}

    for result_data in resilt_list: 
        qc_names = sorted(result_data["qc_names"])
        num_clbits = [qreg.size for qreg in result_data["simulator"]["qc"].qregs][::-1]
        
        print(qc_names)
        name = ""
        for _name in qc_names: 
            name += _name
            if _name == qc_names[-1]: 
                break
            name += " + "
        eval_dict[name] = {}

        # calculate mean and sem of jsd for each experimental results
        count_sim = result_data["simulator"]["count"]
        
        # results of non_scheduling
        count_list = result_data["non_scheduling"]["count"]
        jsd_mean, jsd_sem = _stat_jsd(count_sim, count_list, num_clbits)
        eval_dict[name]["non_scheduling"] = {}
        eval_dict[name]["non_scheduling"]["mean"] = jsd_mean
        eval_dict[name]["non_scheduling"]["sem"] = jsd_sem

        # results of as_late_as_possible policy
        count_alap_list = result_data["alap"]["count"]
        jsd_alap_mean, jsd_alap_sem = _stat_jsd(count_sim, count_alap_list, num_clbits)
        eval_dict[name]["alap"] = {}
        eval_dict[name]["alap"]["mean"] = jsd_alap_mean
        eval_dict[name]["alap"]["sem"] = jsd_alap_sem

    return eval_dict

def _stat_jsd(count_sim, count_list, num_clbits): 
    _jsd_list = [jsd(count_sim, _count, num_clbits) for _count in count_list]
    return statistics.mean(_jsd_list), statistics.sem(_jsd_list)