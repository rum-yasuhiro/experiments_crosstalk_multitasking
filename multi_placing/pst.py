def pst(emp_count, sim_count):
    # probability of success trial
    emp_c_sum = 0
    count_sum = 0
    for label, count in sim_count.items():
        # label, count
        _success_rate = 0
        if count != 0:
            emp_c_sum += emp_count.get(label, 0)
            count_sum += count
        pst = emp_c_sum / count_sum
    return pst