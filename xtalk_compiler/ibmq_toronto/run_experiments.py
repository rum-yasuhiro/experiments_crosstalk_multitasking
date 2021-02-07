import os
from datetime import date
from pprint import pprint
from experiments.xtalk_compiler import load_gspread, execute_xtalk, result_xtalk, plot_xtalk
from experiments.utils import PrepQASMBench, get_IBM_backend, pickle_load

from qiskit.test.mock import *

def execute_set3(xtalk_date, today):
    experiments_path = '/Users/rum/Documents/aqua/gp/experiments'
    errorinfo_path = '/Users/rum/Documents/aqua/gp/errors_information'
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_3', num_set=10, num_qc=3, shift=3)
    qc_path = experiments_path + '/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_toronto')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            xtalk_prop = pickle_load(errorinfo_path + '/toronto_from20201224/xtalk_data_daily/ratio/'+str(xtalk_date)+'.pickle')
            save_path = experiments_path + '/xtalk_compiler/ibmq_toronto/job_id/'+str(today)+'_set3/'+  str(label) +'.pickle'

            data = execute_xtalk(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        
        except: 
            print('Failed: set3 label:', label, ' ', name_list)

def execute_set4(today):
    experiments_path = '/Users/rum/Documents/aqua/gp/experiments'
    errorinfo_path = '/Users/rum/Documents/aqua/gp/errors_information'
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_4', num_set=11, num_qc=4, shift=4)
    qc_path = experiments_path + '/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_toronto')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            xtalk_prop = pickle_load(errorinfo_path + '/toronto_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            save_path = experiments_path + '/xtalk_compiler/ibmq_toronto/job_id/'+str(today)+'_set4/'+  str(label) +'.pickle'

            data = execute_xtalk(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set4 label:', label, ' ', name_list)

def execute_set5(today):
    experiments_path = '/Users/rum/Documents/aqua/gp/experiments'
    errorinfo_path = '/Users/rum/Documents/aqua/gp/errors_information'
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_5', num_set=7, num_qc=5, shift=5)
    qc_path = experiments_path + '/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_toronto')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            xtalk_prop = pickle_load(errorinfo_path + '/toronto_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            save_path = experiments_path + '/xtalk_compiler/ibmq_toronto/job_id/'+str(today)+'_set5/'+  str(label) +'.pickle'

            data = execute_xtalk(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set5 label:', label, ' ', name_list)

def execute_set6(today):
    experiments_path = '/Users/rum/Documents/aqua/gp/experiments'
    errorinfo_path = '/Users/rum/Documents/aqua/gp/errors_information'
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_6', num_set=7, num_qc=6, shift=6)
    qc_path = experiments_path + '/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    
    #################
    pointer = 0

    #################

    for label, name_list in enumerate(name_list_set): 
        try:
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_toronto')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            xtalk_prop = pickle_load(errorinfo_path + '/toronto_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            save_path = experiments_path + '/xtalk_compiler/ibmq_toronto/job_id/'+str(today)+'_set6/'+  str(label+pointer) +'.pickle'

            data = execute_xtalk(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set6 label:', label, ' ', name_list)

if __name__ == '__main__':
    today = date.today()
    xtalk_date = "2021-01-27"
    execute_set3(xtalk_date, today)
    # execute_set4(today)
    # execute_set5(today)
    # execute_set6(today)