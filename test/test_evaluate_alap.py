import os
from pprint import pprint
from experiments.utils import pickle_load
from experiments.alap_scheduling.evaluate_alap import evaluate_alap, convert_to_jsd

def test_evaluate_alap(): 
    data_dir = str(os.getcwd()) + "/test_alap_results"
    save_eval_path = str(os.getcwd()) + "/test_data/alap_jsd.pickle"

    jsd_dict = evaluate_alap(data_dir, save_eval_path)

    pprint(jsd_dict)
    assert(pickle_load(save_eval_path) == jsd_dict)