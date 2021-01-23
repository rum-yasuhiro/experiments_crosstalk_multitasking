from .bitstrings import bitstrings


def separate_multi_counts(counts):
    keys = list(counts.keys())
    num_clbits = [len(clbit) for clbit in keys[0].split()]
    
    # complete bitstrings
    # keys_comp = bitstrings(num_clbits)

    # patial complete bitstrings
    keys_each = [bitstrings(_clbits) for _clbits in num_clbits]

    # separate counts
    pointer=0
    separated_counts = []
    for pclbit_list, num_pclbit in zip(keys_each, num_clbits): 
        pcounts = {}
        for pclbit in pclbit_list: 
            pcounts[pclbit] = 0
            for bitstr, value in counts.items(): 
                if bitstr[pointer:pointer+num_pclbit] == pclbit: 
                    pcounts[pclbit] += value
        separated_counts.append(pcounts)
        pointer += num_pclbit+1

    return separated_counts, num_clbits