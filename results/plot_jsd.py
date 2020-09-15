import matplotlib.pyplot as plt
import numpy as np
from experiments.pickle_tools import pickle_load, pickle_dump


def plot():
    output_path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/jsd_num.png"
    path = "/Users/Yasuhiro/Documents/aqua/gp/experiments/data/ibmq_toronto/jsd.pickle"
    jsd_dict = pickle_load(path)

    xlabels = []
    uniform_jsd = []
    qiskit_jsd = []
    xtalk_jsd = []

    label_y = ['Uniform', 'Qiskit transpiler', 'Crosstalk aware']
    for name, jsd_list in jsd_dict.items():
        colors = ['#dc143c', '#87cefa', '#000080']
        xlabels.append(name)
        uniform_jsd.append(np.sqrt(jsd_list[0]))
        qiskit_jsd.append(np.sqrt(jsd_list[1]))
        xtalk_jsd.append(np.sqrt(jsd_list[2]))

    x_pos = np.arange(len(xlabels))
    w = 0.2

    uni = plt.bar(x_pos-w, uniform_jsd, align='center', width=0.2,
                  label=label_y[0], color=colors[0])
    qis = plt.bar(x_pos, qiskit_jsd, align='center', width=0.2,
                  label=label_y[1], color=colors[1])
    xa = plt.bar(x_pos+w, xtalk_jsd, align='center', width=0.2,
                 label=label_y[2], color=colors[2])

    plt.ylabel('JS-Divergence', fontsize=18)
    plt.legend(handles=[uni, qis, xa], loc='best', shadow=True, fontsize=14)
    xlabels = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ"]
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], xlabels, fontsize=16)

    plt.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0.1)


if __name__ == "__main__":
    plot()
