from typing import Union, List
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
                end = counter+num_bits_in_reg 
                reg_bits = bits[counter:end]
                spaced_bits += reg_bits
                if num_bits_in_reg == num_clbits[-1]:
                    break
                spaced_bits += " "
                counter += end
            spaced_bitstrings.append(spaced_bits)
        return spaced_bitstrings
