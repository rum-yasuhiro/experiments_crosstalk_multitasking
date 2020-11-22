import statistics
import numpy as np

def sem(_list):
    try: 
        std = statistics.stdev(_list)
    except: 
        return 0
    standard_error_mean = std / np.sqrt(len(_list))
    return standard_error_mean

def mean(_list): 
    try: 
        mean_value = statistics.mean(_list)
    except: 
        return 0
    return mean_value




