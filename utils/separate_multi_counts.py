from .bitstrings import bitstrings


def separate_multi_counts(counts):
    """mu"""
    keys = list(counts.keys())
    num_clbits = [len(clbit) for clbit in keys[0].split()]

    # complete bitstrings
    # keys_comp = bitstrings(num_clbits)

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
