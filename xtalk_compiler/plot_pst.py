import os
# import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from experiments.utils import pickle_load

from pprint import pprint

def plot_pst(data_path, save_path):

    data = pickle_load(data_path)
    df = _process_data(data)
    _plot(df, save_path)

    # _dense = data['dense']
    # _noise = data['noise']
    # _sabre = data['sabre']
    # _xtalk = data['xtalk']

    # _plot(_dense, _noise, _sabre, _xtalk, save_path)

def _process_data(data):

    col = ['pst', 'benchmark_set', 'circuit_name', 'exe_type', 'layout']
    data_list = []
    for layout, evals in data.items():
        i = 0
        for benchmark_set, circs in evals.items(): 
            for circuit_name, sm_set in circs.items(): 
                for exe_type, pst in sm_set.items():
                    if pst:
                        data_list.append([pst, i, circuit_name, exe_type, layout])
                    else:
                        data_list.append([0, i, circuit_name, exe_type, layout])
            i += 1
    data_array = np.array(data_list)
    df = pd.DataFrame(data_array, columns=col)
    return df
    

def _plot(df, save_path):
    df['pst'] = df['pst'].astype('float')
    df['benchmark_set'] = df['benchmark_set'].astype('int')
    drops = df.index[df['benchmark_set'] > 4]
    df = df.drop(drops)
    drops = df.index[df['exe_type'] == 'single']
    df = df.drop(drops)
    # color = ['#34A853', '#F789B2', '#F6FB72', '#4285F4']
    sns.set()
    sns.set_style(style='darkgrid')
    plot = sns.barplot(x='benchmark_set', y='pst', hue='layout', hue_order = ['dense', 'sabre', 'noise', 'xtalk'], data=df)
    figure = plot.get_figure()
    figure.savefig(save_path)

# def _plot(data1, data2, data3, data4, save_path):
#     labels = list(data2.keys())
#     uniform = [data1[_name]['uniform'] for _name in labels]
#     single1 = [data1[_name]['single'] for _name in labels]
#     multi1 = [data1[_name]['multi'] for _name in labels]
#     single2 = [data2[_name]['single'] for _name in labels]
#     multi2 = [data2[_name]['multi'] for _name in labels]
#     single3 = [data3[_name]['single'] for _name in labels]
#     multi3 = [data3[_name]['multi'] for _name in labels]
#     single4 = [data4[_name]['single'] for _name in labels]
#     multi4 = [data4[_name]['multi'] for _name in labels]

#     fig = plt.figure(figsize=(10, 5))
#     x_position = np.arange(len(labels))
    
#     bar11 = plt.bar(x_position-0.3, multi1, height=0.2, label='Dense(multi)', color='#34A853')
#     bar21 = plt.bar(x_position+0.1, multi2, height=0.2, label='Noise adaptive(multi)', color='#F789B2')
#     bar31 = plt.bar(x_position-0.1, multi3, height=0.2, label='SABRE(multi)', color='#F6FB72')
#     bar41 = plt.bar(x_position+0.3, multi4, height=0.2, label='Crosstalk adaptive(multi)', color='#4285F4') 
    
#     dashed_list = []
#     for _x, y in zip(x_position, uniform): 
#         dashed = plt.plot([y, y], [_x-0.4, _x+0.4],label='Uniform', color='red', linestyle='dashed')
#         dashed_list.append(dashed)


#     plt.xlim(0, 0.9)
#     labels = [_label[0:4] for _label in labels]
#     plt.yticks(x_position, labels, fontsize=20)
#     plt.xticks(fontsize=20)
#     plt.xlabel('JSD', fontsize=36)

#     # handles = [dashed_list[0], bar11[0], bar12[0], bar21[0], bar22[0], bar31[0], bar32[0], bar41[0], bar42[0]]
#     # labels = ['Uniform', 'Dense(multi)', 'Dense(single)', 'Noise adaptive(multi)', 'Noise adaptive(single)', 'SABRE(multi)', 'SABRE(single)', 'Crosstalk adaptive(multi)', 'Crosstalk adaptive(single)']

#     # plt.legend(handles, labels)
    
#     plt.tight_layout()
    
#     dir_path = os.path.dirname(save_path)
#     if not os.path.exists(dir_path): 
#         print('make directory: ', dir_path)
#         os.mkdir(dir_path)
#     plt.savefig(save_path)

def _plot_label(): 
    pass