import os
from experiments.xtalk_compiler.result_xtalk import result_xtalk
from experiments.xtalk_compiler.plot_xtalk import plot_xtalk


def result_set5(): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = '/Users/Yasuhiro/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_toronto/job_id/2021-01-19_set5'

    backend_name = 'ibmq_toronto'
    eval_path = dir_path + '/evaluations/2021-01-19_set5.pickle'

    # result_xtalk(job_dir, backend_name, eval_path)

    plot_path = dir_path + '/plot/2021-01-19_set5'
    plot_xtalk(eval_path, plot_path)


if __name__ == '__main__':
    result_set5()