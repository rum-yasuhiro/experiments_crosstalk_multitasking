import os
from datetime import date
from experiments.xtalk_compiler.analyze_pst import analyze_pst
from experiments.xtalk_compiler.plot_pst import plot_pst


def evaluate_pst_set3(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path) 
    result_path = dir_path + '/results/'+str(day)+'_set3.pickle'
    eval_path = dir_path + '/evaluations/pst/'+str(day)+'_set3.pickle'
    plot_path = dir_path + '/plot/pst/'+str(day)+'_set3.png'

    analyze_pst(result_path, eval_path)
    plot_pst(eval_path, plot_path)

def evaluate_pst_set4(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    result_path = dir_path + '/results/'+str(day)+'_set4.pickle'
    eval_path = dir_path + '/evaluations/pst/'+str(day)+'_set4.pickle'
    plot_path = dir_path + '/plot/pst/'+str(day)+'_set4.png'

    analyze_pst(result_path, eval_path)
    plot_pst(eval_path, plot_path)

def evaluate_pst_set5(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    result_path = dir_path + '/results/'+str(day)+'_set5.pickle'
    eval_path = dir_path + '/evaluations/pst/'+str(day)+'_set5.pickle'
    plot_path = dir_path + '/plot/pst/'+str(day)+'_set5.png'

    analyze_pst(result_path, eval_path)
    plot_pst(eval_path, plot_path)

def evaluate_pst_set6(day, backend_name): 
    here_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(here_path)
    result_path = dir_path + '/results/'+str(day)+'_set6.pickle'
    eval_path = dir_path + '/evaluations/pst/'+str(day)+'_set6.pickle'
    plot_path = dir_path + '/plot/pst/'+str(day)+'_set6.png'

    analyze_pst(result_path, eval_path)
    plot_pst(eval_path, plot_path)


if __name__ == '__main__':
    # day = date.day()
    day = '2021-01-27'
    backend_name='ibmq_toronto'
    # evaluate_pst_set3(day, backend_name)
    evaluate_pst_set4(day, backend_name)
    # evaluate_pst_set5(day, backend_name)
    # evaluate_pst_set6(day, backend_name)