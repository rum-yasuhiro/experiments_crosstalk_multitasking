import os
import matplotlib.pyplot as plt
import numpy as np
from experiments.utils import pickle_load

def plot_sched(data_path, save_dir):

    data = pickle_load(data_path)

    data_nonsched = data['nonsched']
    data_alap = data['alap']

    i = 0
    for _nonsched, _alap in zip(data_nonsched, data_alap):
        save_path = save_dir +'/' + str(i) + '.png'
        _plot(_nonsched, _alap, save_path)
        i += 1


def _plot(data1, data2, save_path):
    labels = list(data1.keys())
    uniform = [data1[_name]['uniform'] for _name in labels]
    single1 = [data1[_name]['single'] for _name in labels]
    multi1 = [data1[_name]['multi'] for _name in labels]
    single2 = [data2[_name]['single'] for _name in labels]
    multi2 = [data2[_name]['multi'] for _name in labels]

    fig = plt.figure(figsize=(10, 6))
    x_position = np.arange(len(labels))
    
    bar11 = plt.barh(x_position-0.2, multi1, height=0.4, color='#FF0066')
    # bar12 = plt.barh(x_position-0.2, single1, height=0.4, color='#dc143c')

    bar21 = plt.barh(x_position+0.2, multi2, height=0.4, color='#3300FF')
    # bar22 = plt.barh(x_position+0.2, single2, height=0.4, color='#191970')
    
    
    for _x, y in zip(x_position, uniform): 
        dashed = plt.plot([y, y], [_x-0.4, _x+0.4],label='Uniform', color='red', linestyle='dashed')
    


    plt.xlim(0, 0.9)
    labels = [_label[0:4]+"_"+str(i) for i, _label in enumerate(labels)]
    plt.yticks(x_position, labels, fontsize=20)
    plt.xticks(fontsize=20)
    plt.xlabel('JSD', fontsize=36)

    # handles = [dashed[0], bar11[0], bar12[0], bar21[0], bar22[0]]
    # labels = ['Uniform', 'Non optimized(multi)', 'Non optimized(single)', 'ALAP schedule(multi)', 'ALAP schedule(single)']

    # plt.legend(handles, labels)
    
    plt.tight_layout()
    
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        print('make directory: ', dir_path)
        os.mkdir(dir_path)
    plt.savefig(save_path)

def _plot_label(): 
    pass