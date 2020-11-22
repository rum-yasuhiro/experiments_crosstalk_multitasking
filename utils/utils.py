def count_keys(num_clbits):
    """Return ordered count keys."""
    return [bin(j)[2:].zfill(num_clbits) for j in range(2 ** num_clbits)]