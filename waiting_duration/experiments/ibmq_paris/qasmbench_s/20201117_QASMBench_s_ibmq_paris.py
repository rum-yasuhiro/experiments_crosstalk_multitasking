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

# # QASMBench circuit (small) decaying with delay insertion

# +
# import python tools
from pprint import pprint
from datetime import date

# import original packages
from experiments.utils import get_IBM_backend, pickle_load, pickle_dump
from experiments.waiting_duration import EvaluateDelay
from experiments.waiting_duration.benchmarks import prepare_QASMBench
from experiments.waiting_duration import execute_bench
# -


# user input
backend_name = "ibmq_paris"
nseed = 1

# prepare backend devices
backend = get_IBM_backend(backend_name)
simulator = get_IBM_backend("ibmq_qasm_simulator")

# ## Prepare benchmark circuits

circs = prepare_QASMBench("small")

# show circuit image
for circ in circs:
    print("################################ "+ str(circ.name) +" ################################")
    print(circ)

# ## Send job

# max(dt) = 1E6
qc = prepare_pulsestateBench("e6") 
delay_duration_e6 = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000, 950000, 1000000]
execute_bench(
            qc, 
            backend=backend, 
            simulator=simulator, 
            initial_layout=initial_layout, 
            delay_duration_list=delay_duration_e6,
            nseed=nseed, 
)

# max(dt) = 1E5
qc = prepare_pulsestateBench("e5") 
delay_duration_e5 = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000]
execute_bench(
            qc, 
            backend=backend, 
            simulator=simulator, 
            initial_layout=initial_layout, 
            delay_duration_list=delay_duration_e5,
            nseed=nseed, 
)

# max(dt) = 1E4
qc = prepare_pulsestateBench("e4") 
delay_duration_e4 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
execute_bench(
            qc, 
            backend=backend, 
            simulator=simulator, 
            initial_layout=initial_layout, 
            delay_duration_list=delay_duration_e4,
            nseed=nseed, 
)

# ## calculate results

# +
path_= "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/job_id/"+backend_name+"/"+str(date.today())+"_pulse state_e6_"+ backend_name +"_["
_path= "].pickle"
experiments_data_path = path_+ str(0) +_path

exp_data = pickle_load(experiments_data_path)
job_sim = simulator.retrieve_job(exp_data["simulator"]["job_id"])
job_delay_before = [backend.retrieve_job(job_id) for job_id in exp_data["delay_before"]["job_id"]]
job_delay_after = [backend.retrieve_job(job_id) for job_id in exp_data["delay_after"]["job_id"]]
delay_duration_list = exp_data["delay_duration_list"]

eval_delay = EvaluateDelay(job_sim, job_delay_before, job_delay_after, delay_duration_list, nseed=nseed, initial_layout=[0])
counts_before_list_list, counts_after_list_list = eval_delay.evaluate() # return [[seed1 counts_dict], [seed2 counts_dict], ... ]

before_jsd_all, before_jsd_mean, before_jsd_sem = eval_delay.js_divergence(counts_before_list_list)
after_jsd_all, after_jsd_mean, after_jsd_sem = eval_delay.js_divergence(counts_after_list_list)

########################################
# delay_duration_e6 = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000, 950000, 1000000]
########################################

e6 = {
    "before_op": {
        "jsd_all": before_jsd_all, 
        "jsd_mean": before_jsd_mean, 
        "jsd_sem": before_jsd_sem, 
    },  
    "after_op": {
        "jsd_all": after_jsd_all, 
        "jsd_mean": after_jsd_mean, 
        "jsd_sem": after_jsd_sem,
    }, 
    "delay_duration": delay_duration_e6,
    "nseed": nseed
}
# -

pprint(e6)
save_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/data/jsd/pulse_state_decay/"+backend_name+"/"+str(date.today())+"_pulse state_e6_[0].pickle"
pickle_dump(e6, save_path)

# +
path_= "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/job_id/"+backend_name+"/"+str(date.today())+"_pulse state_e5_"+ backend_name +"_["
_path= "].pickle"
experiments_data_path = path_+ str(0) +_path

exp_data = pickle_load(experiments_data_path)
job_sim = simulator.retrieve_job(exp_data["simulator"]["job_id"])
job_delay_before = [backend.retrieve_job(job_id) for job_id in exp_data["delay_before"]["job_id"]]
job_delay_after = [backend.retrieve_job(job_id) for job_id in exp_data["delay_after"]["job_id"]]
delay_duration_list = exp_data["delay_duration_list"]

eval_delay = EvaluateDelay(job_sim, job_delay_before, job_delay_after, delay_duration_list, nseed=nseed, initial_layout=[0])
counts_before_list_list, counts_after_list_list = eval_delay.evaluate() # return [[seed1 counts_dict], [seed2 counts_dict], ... ]

before_jsd_all, before_jsd_mean, before_jsd_sem = eval_delay.js_divergence(counts_before_list_list)
after_jsd_all, after_jsd_mean, after_jsd_sem = eval_delay.js_divergence(counts_after_list_list)

####################################
# delay_duration_e5 = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000]
####################################

e5 = {
    "before_op": {
        "jsd_all": before_jsd_all, 
        "jsd_mean": before_jsd_mean, 
        "jsd_sem": before_jsd_sem, 
    },  
    "after_op": {
        "jsd_all": after_jsd_all, 
        "jsd_mean": after_jsd_mean, 
        "jsd_sem": after_jsd_sem,
    }, 
    "delay_duration": delay_duration_e5,
    "nseed": nseed
}
# -

pprint(e5)
save_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/data/jsd/pulse_state_decay/"+backend_name+"/"+str(date.today())+"_pulse state_e5_[0].pickle"
pickle_dump(e5, save_path)

# +
path_= "/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/job_id/"+backend_name+"/"+str(date.today())+"_pulse state_e4_"+ backend_name +"_["
_path= "].pickle"
experiments_data_path = path_+ str(0) +_path

exp_data = pickle_load(experiments_data_path)
job_sim = simulator.retrieve_job(exp_data["simulator"]["job_id"])
job_delay_before = [backend.retrieve_job(job_id) for job_id in exp_data["delay_before"]["job_id"]]
job_delay_after = [backend.retrieve_job(job_id) for job_id in exp_data["delay_after"]["job_id"]]
delay_duration_list = exp_data["delay_duration_list"]

eval_delay = EvaluateDelay(job_sim, job_delay_before, job_delay_after, delay_duration_list, nseed=nseed, initial_layout=[0])
counts_before_list_list, counts_after_list_list = eval_delay.evaluate() # return [[seed1 counts_dict], [seed2 counts_dict], ... ]

before_jsd_all, before_jsd_mean, before_jsd_sem = eval_delay.js_divergence(counts_before_list_list)
after_jsd_all, after_jsd_mean, after_jsd_sem = eval_delay.js_divergence(counts_after_list_list)

############################################
delay_duration_e4 = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
############################################

e4 = {
    "before_op": {
        "jsd_add": before_jsd_all, 
        "jsd_mean": before_jsd_mean, 
        "jsd_sem": before_jsd_sem, 
    },  
    "after_op": {
        "jsd_add": after_jsd_all, 
        "jsd_mean": after_jsd_mean, 
        "jsd_sem": after_jsd_sem,
    }, 
    "delay_duration": delay_duration_e4,
    "nseed": nseed
}
# -

pprint(e4)

from matplotlib import pyplot as plt
import numpy as np

# +
duration = e6["delay_duration"]
jsd_bef = e6["before_op"]["jsd_mean"]
sem_bef = e6["before_op"]["jsd_sem"]
jsd_aft = e6["after_op"]["jsd_mean"]
sem_aft = e6["after_op"]["jsd_sem"]

sigma = 3
# y軸方向にのみerrorbarを表示
plt.figure(figsize=(10,7))
plt.errorbar(delay_duration_e6, jsd_bef, yerr = [sigma*sem for sem in sem_bef], capsize=3, fmt='.', markersize=10, color='#FF6E33')
plt.errorbar(delay_duration_e6, jsd_aft, yerr = [sigma*sem for sem in sem_aft], capsize=3, fmt='.', markersize=10, color='#33FF80')
plt.xticks(duration, rotation=30)
plt.xlabel('Delay duration', fontsize=20)
plt.ylabel('JSD', fontsize=20)
plt.savefig("/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/experiments/plot/"+str(date.today())+"_"+backend_name+"_qibit0_e6.png")

# +
duration = e5["delay_duration"]
jsd_bef = e5["before_op"]["jsd_mean"]
sem_bef = e5["before_op"]["jsd_sem"]
jsd_aft = e5["after_op"]["jsd_mean"]
sem_aft = e5["after_op"]["jsd_sem"]

sigma = 3
# y軸方向にのみerrorbarを表示
plt.figure(figsize=(10,7))
plt.errorbar(delay_duration_e5, jsd_bef, yerr = [sigma*sem for sem in sem_bef], capsize=3, fmt='.', markersize=10, color='#FF6E33')
plt.errorbar(delay_duration_e5, jsd_aft, yerr = [sigma*sem for sem in sem_aft], capsize=3, fmt='.', markersize=10, color='#33FF80')
plt.xticks(duration, rotation=30)
plt.xlabel('Delay duration', fontsize=20)
plt.ylabel('JSD', fontsize=20)
plt.savefig("/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/experiments/plot/"+str(date.today())+"_"+backend_name+"_qibit0_e5.png")

# +
duration = e4["delay_duration"]
jsd_bef = e4["before_op"]["jsd_mean"]
sem_bef = e4["before_op"]["jsd_sem"]
jsd_aft = e4["after_op"]["jsd_mean"]
sem_aft = e4["after_op"]["jsd_sem"]

sigma = 3
# y軸方向にのみerrorbarを表示
plt.figure(figsize=(10,7))
plt.errorbar(delay_duration_e4, jsd_bef, yerr = [sigma*sem for sem in sem_bef], capsize=3, fmt='.', markersize=10, color='#FF6E33')
plt.errorbar(delay_duration_e4, jsd_aft, yerr = [sigma*sem for sem in sem_aft], capsize=3, fmt='.', markersize=10, color='#33FF80')
plt.xticks(duration, rotation=30)
plt.xlabel('Delay duration', fontsize=20)
plt.ylabel('JSD', fontsize=20)
plt.savefig("/Users/Yasuhiro/Documents/aqua/gp/experiments/waiting_duration/experiments/plot/"+str(date.today())+"_"+backend_name+"_qibit0_e4.png")
