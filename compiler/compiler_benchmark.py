from qiskit import IBMQ, Aer
from experiments.compiler import run_experiments
from experiments.convert_error_information import value_to_ratio
from experiments.pickle_tools import pickle_dump, pickle_load


class CompilerBenchmark:
    def __init__(self, backend_name=None, reservations=False, simulation=False):
        IBMQ.load_account()
        if reservations:
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="reservations"
            )
        else:
            provider = IBMQ.get_provider(
                hub="ibm-q-keio", group="keio-internal", project="keio-students"
            )
        self.backend = provider.get_backend(backend_name)

        if simulation:
            self.backend = provider.get_backend("ibmq_qasm_simulator")

    def run(
        self,
        multi_circuit_components,
        path_to_save_jofile,
        xtalk_prop=None,
        xtalk_file_path=None,
    ):
        """
        Args:
            multi_circuit_components : benchmarking circuits
        """

        #  crosstalk prop
        if xtalk_file_path is None and xtalk is None:
            raise XtalkNotDefinedError("Xtalk property is not defined!")

        if xtalk_prop:
            crosstalk_prop = xtalk_prop
        else:
            crosstalk_prop = pickle_load(xtalk_file_path)

        circ = run_experiments(
            path_to_save_jofile,
            multi_circuit_components=multi_circuit_components,
            backend=self.backend,
            crosstalk_prop=crosstalk_prop,
            shots=8192,
        )

    return circ


class XtalkNotDefinedError(Exception):
    pass
