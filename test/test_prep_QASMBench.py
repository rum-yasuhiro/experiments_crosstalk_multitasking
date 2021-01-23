import os
from experiments.utils.prep_QASMBench import PrepQASMBench

def test_qc_list():
    names = ['error_correctiond3_n5', 'linearsolver_n3']
    path = os.getcwd() + '/xtalk_compiler/benchmark_qc/qasmbench.pickle'
    bench = PrepQASMBench(names, path)

    qcs = bench.qc_list()

    for _qc in qcs: 
        print(_qc.name)