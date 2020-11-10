from qiskit.quantum_info import state_fidelity
from experiments.utils import jsd


class EvaluateDelay: 
    def __init__(self, job_sim, job_delay_op, job_delay_meas, delay_duration_list):
        self.result_sim = job_sim.result()
        self.result_delay_op = job_delay_op.result()
        self.result_delay_meas = job_delay_meas.result()
        self.delay_duration_list = delay_duration_list

    def evaluate(self):

        # simulator
        self.state_sim = self.result_sim.get_statevector()
        self.counts_sim = self.result_sim.get_counts()

        # delay before operations
        self.state_delay_op_list = []
        self.counts_delay_op_list = []
        for id, duration in enumerate(self.delay_duration_list):
            state_op_i = self.result_delay_op.get_statevector(id)
            self.state_delay_op_list.append(state_op_i)
            counts_op_i = result_delay_op.get_counts(id)
            self.counts_delay_op_list.append(counts_op_i)

        # delay before measurements
        self.state_delay_meas_list = []
        self.counts_delay_meas_list = []
        for id, duration in enumerate(self.delay_duration_list):
            state_meas_i = self.result_delay_meas.get_statevector(id)
            self.state_delay_meas_list.append(state_meas_i)
            counts_meas_i = result_delay_meas.get_counts(id)
            self.counts_delay_meas_list.append(counts_meas_i)


    def state_fidelity(self, state_list):
        state_fidelity_list = [state_fidelity(state_op_i, self.state_sim) for state_op_i in state_list]
        return state_fidelity_list


    def js_divergence(self, counts_list):
        jsd_list = [jsd(counts_i, self.state_sim) for counts_i in counts_list]
        return jsd_list


    def plot(self):
        pass


