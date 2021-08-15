from typing import Union, Optional
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_box(
    data: Union[DataFrame, str],
    fig_title: Optional[str] = None,
    save_path: Optional[str] = None,
):
    """
    Args:
        data: DataFrame or the path to the csv file contains DataFrame
        fig_title: Title of figure
        save_path: path to plot figure file to save
    """
    if isinstance(data, str):
        data = pd.read_csv(data, index_col=0)

    plt.figure(dpi=600)
    sns.set_theme(style="darkgrid")
    # sns.set_style("whitegrid")
    # sns.set(palette="Blues", font_scale=2)

    plot = sns.pointplot(x="Hop Count", y="PST", hue="Num CX", data=data, capsize=0.1)
    plot.set(ylim=(0, 1))

    # Put the legend out of the figure
    plt.legend(
        # bbox_to_anchor=(1, 1),
        # loc=2,
        # borderaxespad=0.0,
        title="Number of CX gate",
    )

    plt.tight_layout()

    if fig_title:
        plt.title(fig_title)

    if save_path:
        fig = plot.get_figure()
        fig.savefig(save_path)


if __name__ == "__main__":

    manhattan_10cx = pd.read_csv(
        "/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/results/2021-05-13_manhattan_toffoli10CX.csv"
    )
    manhattan_10cx["Num CX"] = 10
    manhattan_20cx = pd.read_csv(
        "/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/results/2021-05-13_manhattan_toffoli20CX.csv"
    )
    manhattan_20cx["Num CX"] = 20
    manhattan_30cx = pd.read_csv(
        "/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/results/2021-05-13_manhattan_toffoli30CX.csv"
    )
    manhattan_30cx["Num CX"] = 30

    manhattan = pd.concat([manhattan_10cx, manhattan_20cx, manhattan_30cx])
    print(manhattan)
    save_path = (
        "/Users/rum/Documents/aqua/gp/experiments/multi_placing/data/plot/manhattan.png"
    )
    plot_box(
        data=manhattan,
        save_path=save_path,
    )
