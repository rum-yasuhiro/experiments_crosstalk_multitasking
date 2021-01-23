import os
import matplotlib.pyplot as plt
import numpy as np
from experiments.utils import pickle_load

def plot_xtalk(data_path, save_dir):

    data = pickle_load(data_path)

    data_dense = data['dense']
    data_noise = data['noise']
    data_sabre = data['sabre']
    data_xtalk = data['xtalk']

    i = 0
    for _dense, _noise, _sabre, _xtalk in zip(data_dense, data_noise, data_sabre, data_xtalk):
        save_path = save_dir +'/' + str(i) + '.png'
        _plot(_dense, _noise, _sabre, _xtalk, save_path)
        i += 1


def _plot(data1, data2, data3, data4, save_path):
    labels = list(data1.keys())
    uniform = [data1[_name]['uniform'] for _name in labels]
    single1 = [data1[_name]['single'] for _name in labels]
    multi1 = [data1[_name]['multi'] for _name in labels]
    single2 = [data2[_name]['single'] for _name in labels]
    multi2 = [data2[_name]['multi'] for _name in labels]
    single3 = [data3[_name]['single'] for _name in labels]
    multi3 = [data3[_name]['multi'] for _name in labels]
    single4 = [data4[_name]['single'] for _name in labels]
    multi4 = [data4[_name]['multi'] for _name in labels]

    fig = plt.figure(figsize=(10, 6))
    x_position = np.arange(len(labels))
    
    bar11 = plt.barh(x_position-0.3, multi1, height=0.2, label='Dense(multi)', color='#34A853')
    bar12 = plt.barh(x_position-0.3, single1, height=0.2, label='Dense(single)', color='#188038')

    bar21 = plt.barh(x_position-0.1, multi2, height=0.2, label='Noise adaptive(multi)', color='#F789B2')
    bar22 = plt.barh(x_position-0.1, single2, height=0.2, label='Noise adaptive(single)', color='#F72A25')

    bar31 = plt.barh(x_position+0.1, multi3, height=0.2, label='SABRE(multi)', color='#F6FB72')
    bar32 = plt.barh(x_position+0.1, single3, height=0.2, label='SABRE(single)', color='#FBBC04')

    bar41 = plt.barh(x_position+0.3, multi4, height=0.2, label='Crosstalk adaptive(multi)', color='#4285F4')
    bar42    = plt.barh(x_position+0.3, single4, height=0.2, label='Crosstalk adaptive(single)', color='#1967D2')
    
    
    for _x, y in zip(x_position, uniform): 
        dashed = plt.plot([y, y], [_x-0.4, _x+0.4],label='Uniform', color='red', linestyle='dashed')
    


    plt.xlim(0, 0.9)
    plt.yticks(x_position, labels, fontsize=20)
    plt.xticks(fontsize=20)

    handles = [dashed[0], bar11[0], bar12[0], bar21[0], bar22[0], bar31[0], bar32[0], bar41[0], bar42[0]]
    labels = ['Uniform', 'Dense(multi)', 'Dense(single)', 'Noise adaptive(multi)', 'Noise adaptive(single)', 'SABRE(multi)', 'SABRE(single)', 'Crosstalk adaptive(multi)', 'Crosstalk adaptive(single)']

    plt.legend(handles, labels)
    
    plt.tight_layout()
    
    print('make directory: ', dir_path)
    dir_path = os.path.dirname(save_path)
    os.mkdir(dir_path)
    plt.savefig(save_path)

def _plot_label(): 
    pass