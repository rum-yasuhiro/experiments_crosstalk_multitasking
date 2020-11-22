from typing import Union, Optional, List, Dict

from qiskit.circuit.quantumregister import Qubit
from qiskit.transpiler.exceptions import LayoutError
from qiskit.quantum_info import state_fidelity
from qiskit.result.utils import marginal_counts
from qiskit.converters import isinstanceint, isinstancelist
from experiments.utils import counts_stat, jsd, statistics


class EvaluateDelay:
    def __init__(
        self,
        job_sim,
        job_delay_before,
        job_delay_after,
        delay_duration_list,
        nseed,
        initial_layout: Union[List[int], Union[Dict[str, int], Dict[int, str]]],
    ):
        self.result_sim = job_sim.result()
        self.delay_duration_list = delay_duration_list

        self.nseed = nseed
        self.initial_layout = [initial_layout for _ in range(self.nseed)]

        indices = self.parse_initial_layout()
        self.result_delay_before = [
            marginal_counts(job.result(), ind)
            for job, ind in zip(job_delay_before, indices)
        ]
        self.result_delay_after = [
            marginal_counts(job.result(), ind)
            for job, ind in zip(job_delay_after, indices)
        ]

        self.num_clbits_list = [len(ind) for ind in indices]

    def evaluate(self):

        # simulator
        """FIXME
        get_statevectorでエラーが生じる
        self.state_sim = self.result_sim.get_statevector()
        """
        self.counts_sim = self.result_sim.get_counts()
        # self.counts_sim = {"0":4096, "1":4096}

        # delay before operations
        self.state_delay_before_list = []
        self.counts_delay_before_list = []
        for id, duration in enumerate(self.delay_duration_list):
            counts_before_seed = []
            for seed_result in self.result_delay_before:
                """FIXME
                get_statevectorでエラーが生じる
                state_before_i = self.result_delay_before.get_statevector(id)
                self.state_delay_before_list.append(state_before_i)
                """
                counts_before_i = seed_result.get_counts(id)
                counts_before_seed.append(counts_before_i)
            self.counts_delay_before_list.append(counts_before_seed)

        # delay after operation
        self.state_delay_after_list = []
        self.counts_delay_after_list = []
        for id, duration in enumerate(self.delay_duration_list):
            counts_after_seed = []
            for seed_result in self.result_delay_after:
                """FIXME
                get_statevectorでエラーが生じる
                state_after_i = self.result_delay_after.get_statevector(id)
                self.state_delay_after_list.append(state_after_i)
                """
                counts_after_i = seed_result.get_counts(id)
                counts_after_seed.append(counts_after_i)
            self.counts_delay_after_list.append(counts_after_seed)

        return self.counts_delay_before_list, self.counts_delay_after_list

    def stat(self, counts_list_list):
        if len(counts_list_list[0]) > 1:
            mean_list = []
            sem_list = []
            for counts_seed, num_clbits in zip(counts_list_list, self.num_clbits_list):
                counts_mean, counts_sem = counts_stat(counts_seed, num_clbits)
                # standard mean
                mean_list.append(counts_mean)
                # standard error mean
                sem_list.append(counts_sem)
        else:
            mean_list = [counts_seed[0] for counts_seed in counts_list_list]
            sem_list = [{} for _ in counts_list_list]

        return mean_list, sem_list

    def state_fidelity(self, state_list):
        state_fidelity_list = [
            state_fidelity(state_before_i, self.state_sim)
            for state_before_i in state_list
        ]
        return state_fidelity_list

    def js_divergence(self, counts_list_list):
        jsd_list_list = []
        for counts_list in counts_list_list:
            jsd_seed_list = [
                jsd(counts_i, self.counts_sim, num_clbits)
                for counts_i, num_clbits in zip(counts_list, self.num_clbits_list)
            ]
            jsd_list_list.append(jsd_seed_list)

        if len(jsd_list_list[0]) > 1:
            mean_list = []
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

    def plot(self, mean_list_dict, sem_list_dict, label: list, legends: list):
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
                raise EvaluateDelayError(
                    "The initial_layout parameter could not be parsed"
                )
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
            raise EvaluateDelayError(
                "The initial_layout keys or values should be int type"
            )


class EvaluateDelayError(Exception):
    pass
