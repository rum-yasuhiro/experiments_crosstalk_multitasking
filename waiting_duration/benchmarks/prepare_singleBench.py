from .prepare_zerostateBench import prepare_zerostateBench
from .prepare_onestateBench import prepare_onestateBench
from .prepare_plusstateBench import prepare_plusstateBench


def prepare_singleBench(initial_state, label):
    if initial_state == "plus_state": 
        return prepare_plusstateBench(label)

    if initial_state == "zero_state": 
        return prepare_zerostateBench(label)

    if initial_state == "one_state": 
        return prepare_onestateBench(label)
    
    else:
        raise Exception("not prepared such a initial state")
