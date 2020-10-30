from qiskit.test.mock import FakeToronto
from experimental_backend_regulation import xtalk_scoped_bprop


def test_topology_selected_byhand():
    # prepare fake device as backend
    backend = FakeToronto()
    bprop = xtalk_scoped_bprop(backend)


if __name__ == "__main__":
    test_topology_selected_byhand()
