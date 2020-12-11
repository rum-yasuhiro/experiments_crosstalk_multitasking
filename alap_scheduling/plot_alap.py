import os
from matplotlib import pyplot as plt
import numpy as np

from experiments.utils import pickle_dump, pickle_load

def plot_alap(data_path, save_plot_path=None, xmin=None, xmax=None, ymin=None, ymax=None): 
    eval_dict = pickle_load(data_path)
    sorted_eval = sorted(eval_dict.items(), key=lambda x:x[0])
    
    benchmarks = [_nd[0] for _nd in sorted_eval]
    jsd_mean = [_nd[1]["non_scheduling"]["mean"] for _nd in sorted_eval]
    jsd_sem = [_nd[1]["non_scheduling"]["sem"] for _nd in sorted_eval]
    jsd_alap_mean = [_nd[1]["alap"]["mean"] for _nd in sorted_eval]
    jsd_alap_sem = [_nd[1]["alap"]["sem"] for _nd in sorted_eval]

    # sigma for error bar
    sigma = 3

    # plot
    plt.figure(figsize=(10,7))
    
    w = 0.3
    ind = [i+1 for i in range(len(benchmarks))]
    bar = plt.bar([_x-w/2 for _x in ind], jsd_mean, width=w, yerr = [sigma*sem for sem in jsd_sem], color='#dc267f')
    bar_alap = plt.bar([_x+w/2 for _x in ind], jsd_alap_mean, width=w, yerr = [sigma*sem for sem in jsd_alap_sem], color='#648fff')

    plt.xticks(ticks=ind, labels=benchmarks, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylabel('JSD', fontsize=20)

    plt.xlim(xmin=xmin, xmax=xmax)
    plt.ylim(ymin=ymin, ymax=ymax)

    plt.legend([bar, bar_alap], ["Non scheduled", "As late as possible schedule"], fontsize=16)
    
    if save_plot_path:
        plt.savefig(save_plot_path, bbox_inches='tight')
