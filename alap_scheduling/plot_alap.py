import os
from matplotlib import pyplot as plt

from experiments.utils import pickle_dump, pickle_load

def plot_alap(data_path, save_plot_path=None, xmin=None, xmax=None, ymin=None, ymax=None): 
    eval_dict = pickle_load(data_path)
    sorted_eval = sorted(eval_dict.items(), key=lambda x:x[0])
    
    banchmarks = [_nd[0] for _nd in sorted_eval]
    jsd_mean = [_nd[1]["non_scheduling"]["mean"] for _nd in sorted_eval]
    jsd_sem = [_nd[1]["non_scheduling"]["sem"] for _nd in sorted_eval]
    jsd_alap_mean = [_nd[1]["alap"]["mean"] for _nd in sorted_eval]
    jsd_alap_sem = [_nd[1]["alap"]["sem"] for _nd in sorted_eval]

    # error bar
    sigma = 3

    # plot
    plt.figure(figsize=(10,7))
    
    errb = plt.errorbar(banchmarks, jsd_mean, yerr = [sigma*sem for sem in jsd_sem], capsize=3, markersize=10, color='#648fff')
    errb_alap = plt.errorbar(banchmarks, jsd_alap_mean, yerr = [sigma*sem for sem in jsd_alap_sem], capsize=3, markersize=10, color='#dc267f')

    bar = plt.bar(banchmarks, jsd_mean, edge_color='#648fff')
    bar_alap = plt.bar(banchmarks, jsd_alap_mean, edge_color='#dc267f')

    plt.xticks(duration, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylabel('JSD', fontsize=20)

    plt.xlim(xmin=xmin, xmax=xmax)
    plt.ylim(ymin=ymin, ymax=ymax)

    plt.legend([aft, bef], ["Duration after operation", "Duration before operation"], fontsize=16)
    
    if save_plot_path:
        plt.savefig(save_plot_path, bbox_inches='tight')
