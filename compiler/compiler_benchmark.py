from qiskit import IBMQ, Aer
from experiments.compiler.execute import run_experiments
from experiments.error_info_converter import value_to_ratio
from experiments.utils import pickle_dump, pickle_load


class CompilerBenchmark:
    def __init__(self, backend_name=None, fake_device=None, reservations=False):
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
        self.simulator = provider.get_backend("ibmq_qasm_simulator")
        self.fake_device = fake_device

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
        if xtalk_prop is None and xtalk_file_path is None:
            raise XtalkNotDefinedError("Xtalk property is not defined!")

        if xtalk_prop:
            crosstalk_prop = xtalk_prop
        else:
            crosstalk_prop = pickle_load(xtalk_file_path)

        circ = run_experiments(
            path_to_save_jofile,
            multi_circuit_components=multi_circuit_components,
            backend=self.backend,
            simulator=self.simulator,
            crosstalk_prop=crosstalk_prop,
            shots=8192,
            fake_device=self.fake_device,
        )

        return circ


class XtalkNotDefinedError(Exception):
    pass
