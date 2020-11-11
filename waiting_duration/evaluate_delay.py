from typing import Union, List, Dict

from qiskit.circuit.quantumregister import Qubit
from qiskit.transpiler.exceptions import LayoutError
from qiskit.quantum_info import state_fidelity
from qiskit.result.utils import marginal_counts
from qiskit.converters import isinstanceint, isinstancelist 
from experiments.utils import jsd, statistics


class EvaluateDelay: 
    def __init__(self, job_sim, job_delay_op, job_delay_meas, delay_duration_list, initial_layout: Union[List[List[int]], Union[List[Dict[str, int]], List[Dict[int, str]]]]):
        self.result_sim = job_sim.result()
        self.delay_duration_list = delay_duration_list
        self.initial_layout = initial_layout
        """FIXME
        initial_layoutが1重リストの場合、seed数に合わせて、2重リストにする
        """

        indices = self.parse_initial_layout()    
        self.result_delay_op = [marginal_counts(job.result(), ind) for job, ind in zip(job_delay_op, indices)]
        self.result_delay_meas = [marginal_counts(job.result(), ind) for job, ind in zip(job_delay_meas, indices)]

        self.num_clbits_list = [len(ind) for ind in indices]

    def evaluate(self):

        # simulator
        """FIXME
        get_statevectorでエラーが生じる
        self.state_sim = self.result_sim.get_statevector()
        """
        self.counts_sim = self.result_sim.get_counts()


        # delay before operations
        self.state_delay_op_list = []
        self.counts_delay_op_list = []
        for id, duration in enumerate(self.delay_duration_list):
            counts_op_seed = []
            for seed_result in self.result_delay_op:
                """FIXME
                get_statevectorでエラーが生じる
                state_op_i = self.result_delay_op.get_statevector(id)
                self.state_delay_op_list.append(state_op_i)
                """
                counts_op_i = seed_result.get_counts(id)
                counts_op_seed.append(counts_op_i)
            self.counts_delay_op_list.append(counts_op_seed)


        # delay before measurements
        self.state_delay_meas_list = []
        self.counts_delay_meas_list = []
        for id, duration in enumerate(self.delay_duration_list):
            counts_meas_seed = []
            for seed_result in self.result_delay_meas:
                """FIXME
                get_statevectorでエラーが生じる
                state_meas_i = self.result_delay_meas.get_statevector(id)
                self.state_delay_meas_list.append(state_meas_i)
                """
                counts_meas_i = seed_result.get_counts(id)
                counts_meas_seed.append(counts_meas_i)
            self.counts_delay_meas_list.append(counts_meas_seed)

        return self.counts_delay_op_list, self.counts_delay_meas_list


    def state_fidelity(self, state_list):
        state_fidelity_list = [state_fidelity(state_op_i, self.state_sim) for state_op_i in state_list]
        return state_fidelity_list


    def js_divergence(self, counts_list_list):
        jsd_list_list = []
        for counts_list in counts_list_list: 
            jsd_seed_list = [jsd(counts_i, self.counts_sim, num_clbits) for counts_i, num_clbits in zip(counts_list, self.num_clbits_list)]
            jsd_list_list.append(jsd_seed_list)

        if len(jsd_list_list[0]) > 1: 
            mean_list= []
            sem_list = []
            for jsd_list in jsd_list_list: 
                # standard mean
                mean_list.append(statistics.mean(jsd_list))
                # standard error mean
                sem_list.append(statistics.sem(jsd_list))
        else: 
            mean_list = [jsd_seed[0] for jsd_seed in jsd_list_list]
            sem_list = [0 for _ in jsd_list_list]

        return jsd_list_list, mean_list, sem_list


    def plot(self, mean_list_dict, sem_list_dict, label:list, legends:list):
        pass
        

    def parse_initial_layout(self): 
        new_il_list = []
        for il in self.initial_layout: 
            if isinstancelist(il): 
                if all(isinstanceint(elem) for elem in il): 
                    new_il_list.append(il)
                elif all(isinstance(elem, Qubit) for elem in il):
                    new_il_list.append(from_qubit_list(il))
            elif isinstance(il, dict): 
                new_il_list(from_layout_dict(il))
            else: 
                raise EvaluateDelayError("The initial_layout parameter could not be parsed")
        return new_il_list
    
    def from_qubit_list(qubit_list):
        physical_list = []
        for physical, virtual in enumerate(qubit_list):
            physical_list.append(physical)
        return physical_list

    def from_layout_dict(layout_dict):
        physical_list = []
        keys = layout_dict.keys()
        values = layout_dict.values()

        if all(isinstanceint(elem) for elem in keys): 
            return list(keys)
        elif all(isinstanceint(elem) for elem in values):
            return list(values)
        else: 
            raise EvaluateDelayError("The initial_layout keys or values should be int type")

class EvaluateDelayError(Exception): 
    pass

