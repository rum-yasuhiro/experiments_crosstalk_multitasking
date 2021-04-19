import os
from datetime import date
from experiments.xtalk_compiler.result import result


def result_set3(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = dir_path + '/job_id/'+str(day)+'_set3'
    eval_path = dir_path + '/results/'+str(day)+'_set3.pickle'

    result(job_dir, backend_name, eval_path)


def result_set4(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = dir_path + '/job_id/'+str(day)+'_set4'
    eval_path = dir_path + '/results/'+str(day)+'_set4.pickle'

    result(job_dir, backend_name, eval_path)

def result_set5(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = dir_path + '/job_id/'+str(day)+'_set5'

    eval_path = dir_path + '/results/'+str(day)+'_set5.pickle'

    result(job_dir, backend_name, eval_path)


def result_set6(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    job_dir = dir_path + '/job_id/'+str(day)+'_set6'

    eval_path = dir_path + '/results/'+str(day)+'_set6.pickle'

    result(job_dir, backend_name, eval_path)


if __name__ == '__main__':
    # day = date.day()
    day = '2021-01-27'
    backend_name = 'ibmq_toronto'
    result_set3(day, backend_name)
    result_set4(day, backend_name)
    result_set5(day, backend_name)
    result_set6(day, backend_name)