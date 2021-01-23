from qiskit.compiler import transpile, assemble

from experiments.xtalk_compiler import load_gspread
from experiments.utils import PrepQASMBench, get_IBM_backend
from multitasking_transpiler.palloq.compiler import multi_transpile

def test_xtalkadaptivelayout(): 
    name_list_set = load_gspread(worksheet_name='set_3', num_set=10, num_qc=3, shift=3)
    name_list = name_list_set[9]
    print(name_list)

    qc_path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    qasmbench = PrepQASMBench(name_list, qc_path)
    qc_list = qasmbench.qc_list()

    backend = get_IBM_backend('ibmq_toronto')
    shots_multi = 1000

    xtalk_prop = {(16, 19): {}, (1, 4): {(7, 10): 1.5523922159364776, (1, 4): 1.0}, (22, 25): {(4, 7): 1.373897836294811, (10, 12): 1.24005278534089, (12, 15): 1.2650717924862478, (14, 13): 1.2295727510296106, (22, 25): 1.0}, (11, 14): {}, (0, 1): {}, (1, 2): {}, (2, 3): {(5, 8): 1.9828579923816556, (19, 20): 1.187980385590695, (2, 3): 1.0}, (4, 7): {(10, 12): 1.4782839452414733, (4, 7): 1.0}, (3, 5): {(8, 11): 1.1101731182299803, (3, 5): 1.0}, (5, 8): {(2, 3): 3.8982912112371535, (5, 8): 1.0}, (7, 6): {}, (7, 10): {(1, 4): 1.384978600658456, (12, 15): 3.716655801629963, (16, 19): 1.0479045105542835, (7, 10): 1.0}, (8, 9): {}, (8, 11): {}, (10, 12): {(4, 7): 4.584756718619288, (14, 13): 3.3950730369059334, (15, 18): 3.7004301070979504, (10, 12): 1.0}, (12, 13): {(11, 14): 1.6664397082756501, (12, 13): 1.0}, (12, 15): {(7, 10): 3.399583065550418, (14, 13): 3.2251935324570224, (12, 15): 1.0}, (14, 13): {(8, 11): 3.704876525263742, (10, 12): 4.890490951462605, (12, 15): 7.076589040196085, (14, 13): 1.0}, (14, 16): {(8, 11): 1.0959863890724943, (14, 16): 1.0}, (15, 18): {(10, 12): 1.7782238443072769, (15, 18): 1.0}, (18, 17): {}, (18, 21): {(18, 21): 1.0}}
    # transpile
    qc_multi = multi_transpile(
            qc_list, backend=backend,
            instruction_durations=None, 
            basis_gates=['id', 'rz', 'sx', 'x', 'cx'], 
            layout_method='xtalk_adaptive', xtalk_prop=xtalk_prop,
            )

    # run combined qc job
    # qobj_multi = assemble(experiments=qc_multi, backend=backend, shots=shots_multi)
    # job_multi = backend.run(qobj_multi)

    # print(job_multi.job_id())