from experiments.utils import PrepQASMBench
from pprint import pprint

def debug_benchmark_prop(): 
    bench = PrepQASMBench(size="small")
    bp = bench.benchmark_prop()
    pprint(bp)
    return bp

def save_small_bench(): 
    path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/alap_scheduling/benchmarks/qasmbench_small.pickle'
    obj = debug_benchmark_prop()
    PrepQASMBench.save_pickle(obj, path)


def save_medium_bench(): 
    path = '/Users/Yasuhiro/Documents/aqua/gp/experiments/alap_scheduling/benchmarks/qasmbench_medium.pickle'
    bench = PrepQASMBench(size="medium")
    obj = bench.benchmark_prop()
    PrepQASMBench.save_pickle(obj, path)


if __name__ == '__main__':
    # debug_benchmark_prop()
    save_small_bench()
    # save_medium_bench()