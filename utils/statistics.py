import statistics
import numpy as np

def sem(quad_list):
    length = len(quad_list[0])
    sem_list = []
    for i in range(length):
        xth = [list_seed[i] for list_seed in quad_list]
        std = statistics.stdev(xth)
        sem_list.append(std / np.sqrt(len(xth)))
    return sem_list

def mean(quad_list): 
    length = len(quad_list[0])
    mean_list = []
    for i in range(length):
        xth = [list_seed[i] for list_seed in quad_list]
        mean = statistics.mean(xth)
        mean_list.append(mean)
    return mean_list




