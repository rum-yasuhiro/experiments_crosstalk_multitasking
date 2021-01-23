import os
from datetime import date
from pprint import pprint
from xtalk_compiler import load_gspread, execute_xtalk, result_xtalk, plot_xtalk
from experiments.utils import PrepQASMBench, get_IBM_backend, pickle_load

from qiskit.test.mock import *

def execute_set3():
    # prepare benchmark qc
    name_list_set = load_gspread(worksheet_name='set_3', num_set=10, num_qc=3)
    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    
    for label, name_list in enumerate(name_list_set): 
        qasmbench = PrepQASMBench(name_list, qc_path)
        qc_list = qasmbench.qc_list()

        # prepare execution environment
        backend = get_IBM_backend('ibmq_sydney')
        simulator = get_IBM_backend('ibmq_qasm_simulator')
        shots_single=8192
        shots_multi=8192
        xtalk_prop = pickle_load('/Users/Yasuhiro/Documents/aqua/gp/errors_information/sydney_from20201224/xtalk_data_daily/ratio/2021-01-12.pickle')
        save_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_sydney/job_id/2021-01-12_set3_'+  str(label) +'.pickle'

        data = execute_xtalk(name_list, qc_list, backend, simulator, shots_single, shots_multi, xtalk_prop, save_path)

        pprint(data)

if __name__ == '__main__':
    execute_set3()