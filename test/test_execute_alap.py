import os
import pathlib

from qiskit.transpiler import InstructionDurations
from qiskit.test.mock import FakeParis

from experiments.alap_scheduling import execute_alap
from experiments.utils import get_IBM_backend

def test_execute_alap(): 
    simulator = get_IBM_backend('ibmq_qasm_simulator')
    backend = get_IBM_backend('ibmq_paris')
    instruction_durations = InstructionDurations.from_backend(backend)
    path = str(os.getcwd()) + '/test_jobfile/test_alap_job.pickle'
    execute_alap(
        size='small', 
        names=['toffoli_n3', 'adder_n4 '], 
        backend=backend, 
        simulator=simulator,
        shots = 1000, 
        nseed=1,
        save_path=path,
        instruction_durations=instruction_durations
        )

    
