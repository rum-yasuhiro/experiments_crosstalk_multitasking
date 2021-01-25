import os
from datetime import date
from pprint import pprint
from experiments.scheduling import load_gspread, execute_sched
from experiments.utils import PrepQASMBench, get_IBM_backend, pickle_load

from qiskit.test.mock import *

def execute_set3(today):
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_3', num_set=7, num_qc=3, shift=3)
    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_sydney')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            # xtalk_prop = pickle_load('/Users/Yasuhiro/Documents/aqua/gp/errors_information/sydney_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            xtalk_prop={} 

            ###############################
            pointer=3
            ###############################

            save_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/ibmq_sydney/job_id/'+str(today)+'_set3/'+  str(label+pointer) +'.pickle'
            data = execute_sched(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        
        except: 
            print('Failed: set3 label:', label, ' ', name_list)

def execute_set4(today):
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_4', num_set=10, num_qc=4, shift=4)
    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_sydney')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            # xtalk_prop = pickle_load('/Users/Yasuhiro/Documents/aqua/gp/errors_information/sydney_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            xtalk_prop={} 

            ###############################
            pointer=1
            ###############################            
            save_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/ibmq_sydney/job_id/'+str(today)+'_set4/'+  str(label+pointer) +'.pickle'

            data = execute_sched(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set4 label:', label, ' ', name_list)

def execute_set5(today):
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_5', num_set=7, num_qc=5, shift=5)
    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        try: 
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_sydney')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            # xtalk_prop = pickle_load('/Users/Yasuhiro/Documents/aqua/gp/errors_information/sydney_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            xtalk_prop={}
            save_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/ibmq_sydney/job_id/'+str(today)+'_set5/'+  str(label) +'.pickle'

            data = execute_sched(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set5 label:', label, ' ', name_list)

def execute_set6(today):
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_6', num_set=4, num_qc=6, shift=6)
    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/benchmark_qc/qasmbench.pickle'
    
    #################
    pointer = 0

    #################

    for label, name_list in enumerate(name_list_set): 
        try:
            qasmbench = PrepQASMBench(name_list, qc_path)
            qc_list = qasmbench.qc_list()

            # prepare execution environment
            backend = get_IBM_backend('ibmq_sydney')
            simulator = get_IBM_backend('ibmq_qasm_simulator')
            shots_single=8192
            shots_multi=8192
            # xtalk_prop = pickle_load('/Users/Yasuhiro/Documents/aqua/gp/errors_information/sydney_from20201224/xtalk_data_daily/ratio/'+str(today)+'.pickle')
            xtalk_prop={}
            save_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/scheduling/ibmq_sydney/job_id/'+str(today)+'_set6/'+  str(label+pointer) +'.pickle'

            data = execute_sched(qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

            pprint(data)
        except: 
            print('Failed: set6 label:', label, ' ', name_list)

if __name__ == '__main__':
    today = date.today()
    execute_set3(today)
    execute_set4(today)
    execute_set5(today)
    execute_set6(today)