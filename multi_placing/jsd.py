from typing import Dict
import numpy as np
from scipy.spatial.distance import jensenshannon

def jsd(p: Dict[str, float], q: Dict[str, float]): 

    key_len = len(list(p.keys())[0])
    _p = dict_to_list(p, key_len)

    if q == 'uni': 
        _len = len(_p)
        _q = [1 for _ in range(_len)]
    else: 
        _q = dict_to_list(q, key_len)

    jsd = jensenshannon(_p, _q)
    return jsd

def dict_to_list(count, digit) -> list:
    bin = [format(i, '0%db' % digit) for i in range(2**digit)]
    total = sum(count.values())
    return np.array([count.get(bitstr, 0) for bitstr in bin]) / total