from typing import List, Dict, Union
import numpy as np


def marge_list(*lists) -> List:
    extended_list = []
    for list_i in lists: 
        extended_list.extend(list_i)
    marged = list(set(extended_list))
    return marged

def normalize_dist(distribution: Union[List, Dict]) -> Union[List, Dict]: 
    
    if isinstance(distribution, Dict): 
        values = list(distribution.values())
        total = sum(values)
        new_dist = {}
        for key, value in distribution.items():
            new_dist[key] = value / total
        return new_dist

    elif isinstance(distribution, List):
        total = sum(distribution)
        return [value/total for value in distribution]
    else: 
        raise NormalizationError("distribution is not List or Dict type")


class NormalizationError(Exception): 
    pass
