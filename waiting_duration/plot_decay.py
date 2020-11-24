
from matplotlib import pyplot as plt
from pathlib import Path


def plot_decay(data, delay_duration, save_plot_path, xmin=None, xmax=None, ymin=None, ymax=None):
    duration = data["delay_duration"]
    jsd_bef = data["before_op"]["jsd_mean"]
    sem_bef = data["before_op"]["jsd_sem"]
    jsd_aft = data["after_op"]["jsd_mean"]
    sem_aft = data["after_op"]["jsd_sem"]

    sigma = 3
    # y軸方向にのみerrorbarを表示
    plt.figure(figsize=(10,7))
    bef = plt.errorbar(delay_duration, jsd_bef, yerr = [sigma*sem for sem in sem_bef], capsize=3, fmt='.', markersize=10, color='#648fff')
    aft = plt.errorbar(delay_duration, jsd_aft, yerr = [sigma*sem for sem in sem_aft], capsize=3, fmt='.', markersize=10, color='#dc267f')
    
    plt.xticks(duration, rotation=45, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Delay duration', fontsize=20)
    plt.ylabel('JSD', fontsize=20)

    plt.xlim(xmin=xmin, xmax=xmax)
    plt.ylim(ymin=ymin, ymax=ymax)


    plt.legend([aft, bef], ["Duration after operation", "Duration before operation"], fontsize=16)
    plt.savefig(save_plot_path, bbox_inches='tight')


def save_plot_path(date, duration_label, initial_state=None, initial_layout=None):
    root = Path(".")
    file_name = date
    if initial_state: 
        file_name += "_"+ initial_state
    
    if initial_layout: 
        file_name += "_"+ duration_label +"_"+ str(initial_layout) +".png" 
    else: 
        file_name += "_"+ duration_label +".png"
    
    path = root / "data/plot" / file_name
    return path
    