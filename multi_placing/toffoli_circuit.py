from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    
def toffoli_circuit(mode=None, measure=False, repeat=1):
    """
    mode: 
        None: run original toffoli
        'swap', 'SWAP': run toffoli with one swap (7 CX) which can be run on linear topology
        'relative', 'RP': run relative phase toffoli (3 CX) which can be run on linear topology
    """
    qr = QuantumRegister(3)
    tof = QuantumCircuit(qr)

    tof.x(qr[0])
    tof.x(qr[2])
    for _ in range(repeat): 
        if mode == None: 
            tof.toffoli(qr[0], qr[1], qr[2])

        elif mode == 'swap' or mode == 'SWAP': 
            Tof_swap(tof, qr[0], qr[2], qr[1])
        
        elif mode == 'relative': 
            RTof_m(tof, qr[0], qr[2], qr[1])
    
    if measure: 
        cr = ClassicalRegister(3)
        tof.add_register(cr)
        tof.measure(qr, cr)

    return tof


def Tof_swap(circuit, c1, c2, targ, replace=False):  # Toffoli_swap
    """
    See Quirk circuit
    https://algassert.com/quirk#circuit={"cols":[[1,"H"],["•","X"],[1,"Z^-%C2%BC"],[1,"X","•"],[1,"Z^%C2%BC"],[1,"•"],["•","X"],[1,"Z^-%C2%BC"],[1,"X","•"],[1,"X","•"],[1,"•","X"],[1,"X","•"],["Z^%C2%BC",1,"Z^%C2%BC"],["X","•"],["Z^%C2%BC","Z^%C2%BC"],["X","•"],[1,1,"H"],["Chance3"]]}
    
    c1   -->   c1
    |          |
    t    -->   c2
    |          |
    c2   -->   t 
    """
    circuit.h(targ)
    circuit.cx(c1, targ)
    circuit.tdg(targ)
    circuit.cx(c2, targ)
    circuit.t(targ)
    circuit.cx(c1, targ)
    circuit.tdg(targ)
    circuit.cx(targ, c2) #SWAP here
    circuit.cx(c2, targ) #SWAP here
    circuit.t(c1)
    circuit.t(c2)
    circuit.cx(targ, c1)
    circuit.tdg(c1)
    circuit.h(c2)
    circuit.t(targ)
    circuit.cx(targ, c1)
    if replace:
        return circuit


# define Relative phase Toffoli
def RTof_m(circuit, c1, c2, t, replace=False):
    circuit.ry(np.pi/4, t)
    circuit.cx(c2, t)
    circuit.ry(np.pi/4, t)
    circuit.cx(c1, t)
    circuit.ry(-np.pi/4, t)
    circuit.cx(c2, t)
    circuit.ry(-np.pi/4, t)
    if replace:
        return circuit