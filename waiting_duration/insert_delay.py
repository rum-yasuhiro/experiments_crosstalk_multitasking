from typing import List, Union
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import IGate


class InsertDelay:
    def __init__(
        self,
        duration: int,
        circuits: Union[QuantumCircuit, List[QuantumCircuit]],
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
        # self.qarg = qarg
        self.unit = unit

    def before_operation(self):
        delayed_circ = []
        for qc_i in self.circuits:
            qr = QuantumRegister(qc_i.num_qubits)
            cr = ClassicalRegister(qc_i.num_qubits)
            delayed_qc = QuantumCircuit(qr, cr)
            # for qarg in delayed_qc.qubits(): 
            delayed_qc.delay(duration=self.duration, qarg=qr, unit=self.unit)
            delayed_qc.compose(qc_i, inplace=True)    
            delayed_qc.measure(delayed_qc.qubits, delayed_qc.clbits)
            delayed_circ.append(delayed_qc)

        if len(delayed_circ) == 1:
            return delayed_circ[0]
        return delayed_circ

    def before_measurement(self):
        delayed_circ = []
        for qc_i in self.circuits:
            qr = QuantumRegister(qc_i.num_qubits)
            cr = ClassicalRegister(qc_i.num_qubits)
            delayed_qc = QuantumCircuit(qr, cr)
            delayed_qc.compose(qc_i, inplace=True)
            delayed_qc.barrier()
            # for qarg in delayed_qc.qubits(): 
            delayed_qc.delay(duration=self.duration, qarg=qr, unit=self.unit)
            delayed_qc.measure(delayed_qc.qubits, delayed_qc.clbits)
            delayed_circ.append(delayed_qc)
        if len(delayed_circ) == 1:
            return delayed_circ[0]
        return delayed_circ


def _fixing_compose(delayed_qc, qc_i): 
    """FIXME
    otherとnum_qubits, num_clbitsを同じにしているつもりでも以下のエラーが生じる: 

    quantumcircuit.py l.634
    if other.num_qubits > self.num_qubits or \
           other.num_clbits > self.num_clbits:
            raise CircuitError("Trying to compose with another QuantumCircuit "
                               "which has more 'in' edges.")

    応急処置として、この関数で代用する
    """

    for operation in qc_i.data: 
        delayed_qc.data.append(operation)

    return delayed_qc