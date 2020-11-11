from typing import Dict

from scipy.spatial.distance import jensenshannon
from qiskit.result.utils import count_keys
from .normalize import marge_list



def jsd(p: Dict[str, float], q: Dict[str, float], num_clbits: int, discrete=True): 
    bitstr_keys = count_keys(num_clbits)
    _p = dict_to_list(p, bitstr_keys)
    _q = dict_to_list(q, bitstr_keys)
    
    jsd = jensenshannon(_p, _q)
    return jsd

def dict_to_list(count, bitstr_keys) -> list:
    dist_list = []
    for bitstr in bitstr_keys:
        try: 
            dist_list.append(count[bitstr])
        except: 
            dist_list.append(0)
    total = sum(dist_list)
    dist_list = [elem/total for elem in dist_list]
    return dist_list