from qiskit import *
from qiskit.visualization import plot_histogram
from typing import Sequence


def build_cnot(circ: QuantumCircuit, N: int):
    """
    Build a cnot gate with N control bit on a 2N sized circuit.
    
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
    >>> build_cnot(circ, 5)
    >>> circ.draw("text")
          ░                                               ░ 
    q_0: ─░───■───────────────────────────────────────■───░─
          ░   │                                       │   ░ 
    q_1: ─░───■───────────────────────────────────────■───░─
          ░   │                                       │   ░ 
    q_2: ─░───┼────■─────────────────────────────■────┼───░─
          ░   │    │                             │    │   ░ 
    q_3: ─░───┼────┼────■───────────────────■────┼────┼───░─
          ░   │    │    │                   │    │    │   ░ 
    q_4: ─░───┼────┼────┼────■─────────■────┼────┼────┼───░─
          ░ ┌─┴─┐  │    │    │         │    │    │  ┌─┴─┐ ░ 
    q_5: ─░─┤ X ├──■────┼────┼─────────┼────┼────■──┤ X ├─░─
          ░ └───┘┌─┴─┐  │    │         │    │  ┌─┴─┐└───┘ ░ 
    q_6: ─░──────┤ X ├──■────┼─────────┼────■──┤ X ├──────░─
          ░      └───┘┌─┴─┐  │         │  ┌─┴─┐└───┘      ░ 
    q_7: ─░───────────┤ X ├──■─────────■──┤ X ├───────────░─
          ░           └───┘┌─┴─┐     ┌─┴─┐└───┘           ░ 
    q_8: ─░────────────────┤ X ├──■──┤ X ├────────────────░─
          ░                └───┘┌─┴─┐└───┘                ░ 
    q_9: ─░─────────────────────┤ X ├─────────────────────░─
          ░                     └───┘                     ░ 
    """
    circ.barrier()
    circ.ccx(0, 1, N)
    for c, t in zip(range(2, N), range(N + 1, 2 * N - 1)):
        circ.ccx(c, t - 1, t)
    circ.cx(t, t + 1)
    for c, t in zip(range(N - 1, 1, -1), range(2 * N - 2, N, -1)):
        circ.ccx(c, t - 1, t)
    circ.ccx(0, 1, N)
    circ.barrier()
    
    
def flip_zeros(circ: QuantumCircuit, bits: Sequence[int]):
    """
    Apply not unitary gate on circ's layer that match index of bits where bit is equal to zero
    """
    for i, bit in enumerate(bits):
        if bit == 0:
            circ.x(i)
            
            
def f_oracle(circ: QuantumCircuit, N: int, w: Sequence[int]):
    """
    Create an oracle circuit for the given w bit sequence to gess
    Represent the case where the targeted value is a number (represented here by a bit sequence)
    """
    circ.barrier()
    flip_zeros(circ, w)
    build_cnot(circ, N)
    flip_zeros(circ, w)
    circ.barrier()
    

def build_cz(circ: QuantumCircuit, N: int):
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


def diffuser(circ: QuantumCircuit, N: int):
    """
    Build the diffuser operator of size N
    """
    circ.h(range(N))
    circ.n(range(N))
    
    circ.n(range(N))
    circ.h(range(N))