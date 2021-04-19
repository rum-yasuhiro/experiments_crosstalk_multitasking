import os
from datetime import date
from experiments.xtalk_compiler.result_xtalk import result_xtalk
from experiments.xtalk_compiler.plot_xtalk import plot_xtalk


def result_set3(day): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = '/Users/rum/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_toronto/job_id/'+str(day)+'_set3'

    backend_name = 'ibmq_toronto'
    eval_path = dir_path + '/evaluations/'+str(day)+'_set3.pickle'

    result_xtalk(job_dir, backend_name, eval_path)

    plot_path = dir_path + '/plot/'+str(day)+'_set3'
    plot_xtalk(eval_path, plot_path)

def result_set4(day): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = '/Users/rum/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_toronto/job_id/'+str(day)+'_set4'

    backend_name = 'ibmq_toronto'
    eval_path = dir_path + '/evaluations/'+str(day)+'_set4.pickle'

    # result_xtalk(job_dir, backend_name, eval_path)

    plot_path = dir_path + '/plot/'+str(day)+'_set4'
    plot_xtalk(eval_path, plot_path)

def result_set5(day): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = '/Users/rum/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_toronto/job_id/'+str(day)+'_set5'

    backend_name = 'ibmq_toronto'
    eval_path = dir_path + '/evaluations/'+str(day)+'_set5.pickle'

    # result_xtalk(job_dir, backend_name, eval_path)

    plot_path = dir_path + '/plot/'+str(day)+'_set5'
    plot_xtalk(eval_path, plot_path)

def result_set6(day): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = '/Users/rum/Documents/aqua/gp/experiments/xtalk_compiler/ibmq_toronto/job_id/'+str(day)+'_set6'

    backend_name = 'ibmq_toronto'
    eval_path = dir_path + '/evaluations/'+str(day)+'_set6.pickle'

    result_xtalk(job_dir, backend_name, eval_path)

    plot_path = dir_path + '/plot/'+str(day)+'_set6'
    plot_xtalk(eval_path, plot_path)


if __name__ == '__main__':
    # day = date.day()
    day = '2021-01-27'
    result_set3(day)
    result_set4(day)
    result_set5(day)
    result_set6(day)