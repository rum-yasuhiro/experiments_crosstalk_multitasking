from typing import List, Union
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import IGate


class InsertDelay:
    def __init__(
        self,
        duration: int,
        circuits: Union[QuantumCircuit, List[QuantumCircuit]],
        qarg=None,
        unit="dt",
    ):
        """
        Args:
            circuits: Quantum Circuit without measurements

        """
        self.duration = duration
        self.circuits = (
            circuits if isinstance(circuits, list) else [circuits]
        )
        self.qarg = qarg
        self.unit = unit

    def before_operation(self):
        delayed_circ = []
        for qc_i in self.circuits:
            delayed_qc = QuantumCircuit(qc_i.num_qubits)
            delayed_qc.delay(duration=self.duration, qarg=self.qarg, unit=self.unit)
            delayed_qc.compose(qc_i, inplace=True)
            delayed_qc.measure_all()
            delayed_circ.append(delayed_qc)

        if len(delayed_circ) == 1:
            return delayed_circ[0]
        return delayed_circ

    def before_measurement(self):
        delayed_circ = []
        for qc_i in self.circuits:
            delayed_qc = QuantumCircuit(qc_i.num_qubits)
            delayed_qc.compose(qc_i, inplace=True)
            delayed_qc.barrier()
            delayed_qc.delay(duration=self.duration, qarg=self.qarg, unit=self.unit)
            delayed_qc.measure_all()
            delayed_circ.append(delayed_qc)
        if len(delayed_circ) == 1:
            return delayed_circ[0]
        return delayed_circ

