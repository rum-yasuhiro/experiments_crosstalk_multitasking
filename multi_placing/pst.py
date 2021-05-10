def pst(emp_count, sim_count):
    # probability of success trial
    emp_sum = 0
    sim_sum = 0
    for label, count in sim_count.items():
        # label, count
        if count > 0:
            emp_sum += emp_count.get(label, 0)
            sim_sum += count
        pst = emp_sum / sim_sum
    return pst
