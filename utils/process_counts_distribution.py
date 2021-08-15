from typing import Union, List
from .statistics import mean, sem


def separate_multi_counts(counts: dict) -> List[dict]:
    """Separate the distribution counts of multiple qc combined circuit

    Args:
        counts (dictionary): counts distribution of result of multi-programming

    Returns:
        List[dictionary]: list of each counts distribution of quantum computation
    """
    keys = list(counts.keys())
    num_clbits = [len(clbit) for clbit in keys[0].split()]

    # partial complete bitstrings
    keys_each = [bitstrings(_clbits) for _clbits in num_clbits]

    # separate counts
    pointer = 0
    separated_counts = []
    for p_clbit_list, num_p_clbit in zip(keys_each, num_clbits):
        p_counts = {}
        for p_clbit in p_clbit_list:
            p_counts[p_clbit] = 0
            for bitstr, value in counts.items():
                if bitstr[pointer : pointer + num_p_clbit] == p_clbit:
                    p_counts[p_clbit] += value
        separated_counts.append(p_counts)
        pointer += num_p_clbit + 1

    return separated_counts, num_clbits


def mean_counts_distribution(counts_list):
    """Take multiple distribution then return its mean

    Args:
        counts_list (List[dictionary]): list of counts distribution of result of quantum computation

    Returns:
        dictrionary: counts distribution composed by mean of each value in counts distribution
    """
    counts_mean = {}

    _keys = list(counts_list.keys())
    num_clbit = len(_keys[0])

    bitstr_keys = bitstrings(num_clbit)
    for bitstr in bitstr_keys:
        values = []
        for counts in counts_list:
            try:
                values.append(counts[bitstr])
            except:
                values.append(0)
        counts_mean[bitstr] = mean(values)
    return counts_mean


def sem_counts_distribution(counts_list):
    """Take multiple distributions then return distribution composed each standard error of the mean.

    Args:
        counts_list (List[dictionary]): list of counts distribution of result of quantum computation

    Returns:
        dictrionary: counts distribution composed by sem of each value in counts distribution
    """
    counts_sem = {}

    _keys = list(counts_list.keys())
    num_clbit = len(_keys[0])

    bitstr_keys = bitstrings(num_clbit)
    for bitstr in bitstr_keys:
        values = []
        for counts in counts_list:
            try:
                values.append(counts[bitstr])
            except:
                values.append(0)
        counts_sem[bitstr] = sem(values)
    return counts_sem


def bitstrings(num_clbits: Union[int, List[int]]):
    """Return ordered count keys."""
    if isinstance(num_clbits, int):
        return [bin(j)[2:].zfill(num_clbits) for j in range(2 ** num_clbits)]

    elif isinstance(num_clbits, list):
        sum_clbits = int(sum(num_clbits))
        _bitstrings = [bin(j)[2:].zfill(sum_clbits) for j in range(2 ** sum_clbits)]
        spaced_bitstrings = []
        for bits in _bitstrings:
            counter = 0
            spaced_bits = ""
            bits = str(bits)
            for num_bits_in_reg in num_clbits:
                end = counter + num_bits_in_reg
                reg_bits = bits[counter:end]
                spaced_bits += reg_bits
                if num_bits_in_reg == num_clbits[-1]:
                    break
                spaced_bits += " "
                counter += end
            spaced_bitstrings.append(spaced_bits)
        return spaced_bitstrings
