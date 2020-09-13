def _count_each(multi_count):
    bit_keys = list(multi_count.keys())
    regs = bit_keys[0].split()
    print(regs)
    each_count = []
    offset = 0
    limit = 0
    for register in regs[::-1]:
        num_bit = len(register)
        bin_list = [format(i, '0'+str(num_bit)+'b') for i in range(num_bit**2)]
        count = {}
        # initialize count dictionay
        for bin_key in bin_list:
            count[bin_key] = 0
        limit += num_bit
        for key, value in multi_count.items():
            key = key.replace(" ", "")
            for bin_key in bin_list:
                if offset == 0:
                    v = value if bin_key == key[-limit:] else 0
                    print(bin_key, key[-limit:], value, v)
                else:
                    v = value if bin_key == key[-limit:-offset] else 0
                    print(bin_key, key[-limit:-offset], value, v)
                count[bin_key] += v
        offset += num_bit
        each_count.append(count)
    return each_count


each_count = _count_each(d)


for count in each_count:
    print(count)
    print(sum(list(count.values())))
