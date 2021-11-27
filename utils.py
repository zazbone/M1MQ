from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from qiskit.providers.aer import QasmSimulator
from typing import Sequence


def build_cnot(N: int):
    """
    Build and return a 2`N` sized circuit with a cnot gate of `N` control bit.
    
    [0, `N`[ :  are controls bits.
    [`N` to 2`N` - 1[ :  are Auxilaries bits.
    Last one is the target one.
    
    Two estetic barier with be added arroud the operator.
    
    Parameters
    ----------
    N : int 
        Number of control bits.
        warning:: Make sure that the `circ` Quantum circuit have at least a len of 2N.
    
    Returns
    -------
    QuantumCircuit
        circuit of 2`N` qbits with a Cnot gate of N control bits.
        
    Examples
    --------
    >>> circ = build_cnot(4)
    >>> circ.draw("text")

    q_0: ──■─────────────────────────────■──
           │                             │  
    q_1: ──■─────────────────────────────■──
           │                             │  
    q_2: ──┼────■───────────────────■────┼──
           │    │                   │    │  
    q_3: ──┼────┼────■─────────■────┼────┼──
         ┌─┴─┐  │    │         │    │  ┌─┴─┐
    q_4: ┤ X ├──■────┼─────────┼────■──┤ X ├
         └───┘┌─┴─┐  │         │  ┌─┴─┐└───┘
    q_5: ─────┤ X ├──■─────────■──┤ X ├─────
              └───┘┌─┴─┐     ┌─┴─┐└───┘     
    q_6: ──────────┤ X ├──■──┤ X ├──────────
                   └───┘┌─┴─┐└───┘          
    q_7: ───────────────┤ X ├───────────────
                        └───┘               
    """
    circ = QuantumCircuit(2 * N)
    circ.ccx(0, 1, N)
    for c, t in zip(range(2, N), range(N + 1, 2 * N - 1)):
        circ.ccx(c, t - 1, t)
    circ.cx(t, t + 1)
    for c, t in zip(range(N - 1, 1, -1), range(2 * N - 2, N, -1)):
        circ.ccx(c, t - 1, t)
    circ.ccx(0, 1, N)
    return circ
    
    
def flip_zeros(circ: QuantumCircuit, bits: Sequence[int]):
    """
    Apply not unitary gate on circ's layer that match index of bits where bit is equal to zero
    """
    for i, bit in enumerate(bits):
        if bit == 0:
            circ.x(i)
            
            
def num_oracle(w: int, bitsize: int=-1):
    """
    Create an oracle circuit for the given w bit sequence to gess
    Represent the case where the targeted value is a number (represented here by a bit sequence)
    used in groover algorithm
    """
    bitstr = f"{w:b}"
    if 0 < bitsize:
        assert len(bitstr) > bitsize, ValueError(f"{bitsize} bits is not enouth to represent w={w} value")
        bitstr = "0" * (len(bitstr) - bitsize) + bitstr
    N = len(bitstr)
    bits = map(int, bitstr)
    
    
    wflip = QuantumCircuit(N)
    flip_zeros(wflip, bits)
    barrier = QuantumCircuit(N)
    barrier.barrier()
    cnot = build_cnot(N)
    
    # Compose all the final circuit part (bitflip | cnot | bitflip)
    oracle = cnot.compose(barrier, range(N), front=True)
    oracle = oracle.compose(wflip, range(N), front=True)
    oracle = oracle.compose(wflip, range(N), front=False)
    oracle = oracle.compose(barrier, range(N), front=False)
    return oracle


def build_cz(N: int):
    """
    Build a cz gate with N control bit on a 2N sized circuit.
    
    [0, N[ :  are controls bits.
    [N to 2N - 1[ :  are Auxilaries bits.
    Last one is the target one.
    
    Two estetic barier with be added arroud the operator.
    
    Parameters
    ----------
    circ : QuantumCircuit
        circuit on witch you want to create N-cnot gate.
        note:: The circuit will be modify in place.
    N : int 
        Number of control bits.
        warning:: Make sure that the `circ` Quantum circuit have at least a len of 2N.
        
    Examples
    --------
    >>> circ = QuantumCircuit(10)
    >>> build_cz(circ, 5)
    >>> circ.draw("text")
    """
    raise NotImplementedError("It's appears that we don't need it")


def diffuser(circ: QuantumCircuit, N: int):
    """
    Build the diffuser operator of size N
    """
    circ.h(range(N))
    circ.n(range(N))
    
    circ.n(range(N))
    circ.h(range(N))
    

def simulate(circ):
    """
    https://qiskit.org/documentation/tutorials/circuits/01_circuit_basics.html?highlight=backend
    """
    aer_sim = QasmSimulator()
    qasm_circ = transpile(circ, aer_sim)
    result = aer_sim.run(qasm_circ, shots=1024).result()
    return result.get_counts(qasm_circ)