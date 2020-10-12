from qiskit import IBMQ
from experiments.experimental_backend_regulation import xtalk_scoped_bprop


def test_xtalk_scoped_bprop():
    # prepare ibmq api
    IBMQ.load_account()
    provider = IBMQ.get_provider(
        hub='ibm-q-keio', group='keio-internal', project='keio-students')

    backend = provider.get_backend('ibmq_toronto')

    xtalk_scoped_bprop(backend)


if __name__ == "__main__":
    test_xtalk_scoped_bprop()
