import os
from experiments.alap_scheduling.plot_alap import plot_alap

def test_plot_alap(): 

    data_path = str(os.getcwd()) + "/test_data/alap_jsd.pickle"
    save_plot_path = str(os.getcwd()) + "/test_data/alap_plot.png"
    
    plot_alap(data_path, save_plot_path)