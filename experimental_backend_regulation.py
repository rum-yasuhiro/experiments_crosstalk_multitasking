import networkx as nx
from experiments.pickle_tools import pickle_dump, pickle_load

from pprint import pprint


def xtalk_scoped_bprop(backend, xtalk_property=None, num_requird_hw_qubits=None):
    """
    クロストークコンパイラの性能評価のために、、
    クロストークを必ず含むような量子ビット, 量子ビットconnectionのセットを残して、
    実験で利用できるQPUリソースを制限する。(backend_propertyを変更する)

    pass_managerの内部で使用される、backend_prop.gates と backend_prop.qubits だけを変更する。

    Args:
        backend               : IBMQBackend
        xtalk_property        :
        num_requird_hw_qubits : 後の実験で使用したい量子ビット数
    Returns:
        backend_property scope on backend xtalk characteristics
    """

    if xtalk_property is None and num_requird_hw_qubits is None:
        return _choose_topology_byhand(backend)

    backend_prop = backend.properties()
    xtalk_ratio_graph = nx.Graph()

    # プロセッサの xtalk ratio グラフを作る
    for ginfo in backend_prop.gates:
        if ginfo.gate == "cx":
            xtalk_ratio = 1.0
            xtalk_ratio_graph.add_edge(
                ginfo.qubits[0], ginfo.qubits[1], wight=xtalk_ratio
            )
            """TODO
            xtalk_propertyに基づき、
            xtalkがcx error率に与える影響をxtalk_ratioに反映させ、
            xtalk_ratio_graphを完成させる
            """

    # xtalk_ratio_graphに基づき、
    # 実験で使いたい量子ビット、２量子ゲートを選定する
    qubits_exp = []
    gates_exp = []

    # 実験に不要な  量子ビット 、　    ２量子ゲート     を削除する
    # 　　　       bprop.qubits()   bprop.gates()

    return backend_prop


def _choose_topology_byhand(backend):
    """
    ibmq_toronto 2020 / 10 / 12 時点
    クロストークの影響が強い量子ビット、2量子ゲートを選択
    """

    selected_qubits = [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 18]
    selected_edges = [
        [1, 2],
        [2, 1],
        [1, 4],
        [4, 1],
        [3, 5],
        [5, 3],
        [4, 7],
        [7, 4],
        [5, 8],
        [8, 5],
        [7, 10],
        [10, 7],
        [8, 11],
        [11, 8],
        [10, 12],
        [12, 10],
        [11, 14],
        [14, 11],
        [12, 13],
        [13, 12],
        [12, 15],
        [15, 12],
        [13, 14],
        [14, 13],
        [15, 18],
        [18, 15],
    ]

    _backend_prop = backend.properties()
    _backend_conf = backend.configuration()

    num_hw_qubit = _backend_conf.n_qubits
    hw_qubits = [q for q in range(num_hw_qubit)]

    # eliminate unseledted qubits from _backend_prop
    for hw_qubit in reversed(hw_qubits):
        if hw_qubit not in selected_qubits:
            del _backend_prop.qubits[hw_qubit]

    # eliminate unselected gates from _backend_prop
    gates = []
    for gate in _backend_prop.gates:
        if gate.qubits[0] in selected_qubits or gate.qubits in selected_edges:
            gates.append(gate)

    _backend_prop.gates = gates

    return _backend_prop
