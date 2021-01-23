from .bitstrings import bitstrings
from .statistics import mean, sem


def counts_stat(counts_list, num_clbits):
    counts_mean={}
    counts_sem={}

    bitstr_keys = bitstrings(num_clbits)
    for bitstr in bitstr_keys: 
        values=[]
        for counts in counts_list:
            try: 
                values.append(counts[bitstr])
            except: 
                values.append(0)
        counts_mean[bitstr] = mean(values)
        counts_sem[bitstr] = sem(values)
    return counts_mean, counts_sem