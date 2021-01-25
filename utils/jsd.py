from typing import Dict

from scipy.spatial.distance import jensenshannon
from .bitstrings import bitstrings
from .normalize import marge_list

def jsd(p: Dict[str, float], q: Dict[str, float], num_clbits: int, discrete=True): 

    # bitstr_keys = bitstrings(num_clbits)
    _p = dict_to_list(p)

    if q == 'uni': 
        _len = len(_p)
        _q = [1 for _ in range(_len)]
    else: 
        _q = dict_to_list(q, bitstr_keys)

    jsd = jensenshannon(_p, _q)
    return jsd

def dict_to_list(count) -> list:
    digit = len(str(iter(count)))
    bin = [format(i, '0%db' % digit) for i in range(2**digit)]
    total = sum(count.values())
    return np.array([count.get(bitstr, 0) for bitstr in bin]) / total