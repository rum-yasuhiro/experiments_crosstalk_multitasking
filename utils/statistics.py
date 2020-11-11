import statistics
import numpy as np

def sem(_list):
    std = statistics.stdev(_list)
    standard_error_mean = std / np.sqrt(len(_list))
    return standard_error_mean

def mean(_list): 
    mean_value = statistics.mean(_list)
    return mean_value




