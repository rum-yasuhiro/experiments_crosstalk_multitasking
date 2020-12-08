# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: gp-experiments
#     language: python
#     name: gp-experiments
# ---

# # $\vert 1 \rangle$ state decaying
#
# ## qubit: 0

# +
from pprint import pprint
from datetime import date

from experiments.utils import get_IBM_backend, pickle_load
from experiments.waiting_duration.benchmarks import prepare_singleBench
from experiments.waiting_duration import execute_bench, save_jobid_path
from experiments.waiting_duration import calculate_results, save_data_path
# -


# user input
backend_name = "ibmq_toronto"
nseed = 5
date = "2020-11-24"
initial_layout = [0]

# +
# define backends
backend = get_IBM_backend(backend_name, reservations=True)
simulator = get_IBM_backend("ibmq_qasm_simulator")

# type of experiments 
exp_type = "single_qubit"
initial_state="one_state"
# -

# ## backend properties

# +
print("####################### dutation time #######################")
dt = backend.configuration().dt
print("1 dt = ", dt, " sec")
print("     = ", dt * 10**10, "ns")

print()

print("####################### gate length #######################")
coupling_map = backend.configuration().coupling_map
prop = backend.properties()
cx_durations = []
for coup in coupling_map:
    length = prop.gate_length("cx", coup)
    cx_durations.append(length)
    print(coup, length)

import numpy as np
print("##################################################")
print("max: ", max(cx_durations), " (sec)")
print("min: ", min(cx_durations), " (sec)")
print("mean: ", np.mean(cx_durations), " (sec)")
# -

# ## Send job

# max(dt) = 1E6
jobid_path_e6 = save_jobid_path(date, "e6", initial_state, initial_layout)
delay_duration_e6 = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000, 950000, 1000000]

# +
# qc = prepare_singleBench(initial_state, "e6")
# execute_bench(
#             qc, 
#             backend=backend, 
#             simulator=simulator, 
#             initial_layout=initial_layout, 
#             save_path = jobid_path_e6,
#             delay_duration_list=delay_duration_e6,
#             nseed=nseed, 
# )
# -

# max(dt) = 1E5
# delay dulation label
jobid_path_e5 = save_jobid_path(date, "e5", initial_state, initial_layout)
delay_duration_e5 = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000]

# +
# qc = prepare_singleBench(initial_state, "e5")
# execute_bench(
#             qc, 
#             backend=backend, 
#             simulator=simulator, 
#             initial_layout=initial_layout, 
#             save_path = jobid_path_e5,
#             delay_duration_list=delay_duration_e5,
#             nseed=nseed, 
# )
# -

# max(dt) = 1E4
# delay dulation label
jobid_path_e4 = save_jobid_path(date, "e4", initial_state, initial_layout)
delay_duration_e4 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]

# +
# qc = prepare_singleBench(initial_state, "e4")
# execute_bench(
#             qc, 
#             backend=backend, 
#             simulator=simulator, 
#             initial_layout=initial_layout, 
#             save_path = jobid_path_e4,
#             delay_duration_list=delay_duration_e4,
#             nseed=nseed, 
# )
# -

# ## calculate results

savedata_path_e6 = save_data_path(date, "e6", initial_state, initial_layout)

# +
# e6 = calculate_results(delay_duration_e6, jobid_path_e6, savedata_path_e6, backend, simulator, nseed)
# pprint(e6)
# -

savedata_path_e5 = save_data_path(date, "e5", initial_state, initial_layout)

# +
# e5 = calculate_results(delay_duration_e5, jobid_path_e5, savedata_path_e5, backend, simulator, nseed)
# pprint(e5)
# -

savedata_path_e4 = save_data_path(date, "e4", initial_state, initial_layout)

# +
# e4 = calculate_results(delay_duration_e4, jobid_path_e4, savedata_path_e4, backend, simulator, nseed)
# pprint(e4)
# -

# ## Plot results

from experiments.waiting_duration import plot_decay, save_plot_path

save_plot_path_e6 = save_plot_path(date, "e6", initial_state, initial_layout)
e6 = pickle_load(savedata_path_e6)
plot_decay(e6, delay_duration_e6, save_plot_path_e6, ymin=0, ymax=0.8)

save_plot_path_e5 = save_plot_path(date, "e5", initial_state, initial_layout)
e5 = pickle_load(savedata_path_e5)
plot_decay(e5, delay_duration_e5, save_plot_path_e5, ymin=0, ymax=0.5)

save_plot_path_e4 = save_plot_path(date, "e4", initial_state, initial_layout)
e4 = pickle_load(savedata_path_e4)
plot_decay(e4, delay_duration_e4, save_plot_path_e4, ymin=0, ymax=0.25)


