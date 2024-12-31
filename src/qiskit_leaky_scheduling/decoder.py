import struct

from qiskit.circuit import QuantumCircuit
from qiskit.dagcircuit import DAGOpNode
from qiskit.converters import circuit_to_dag


def recover_data(qc: QuantumCircuit, bytes_per_gate=6) -> bytes:
    data = b""
    dag = circuit_to_dag(qc, copy_operations=False)
    rotations = [node for node in dag.topological_op_nodes() if node.name == "rz"]
    for rz in rotations:
        num = rz.params[0]
        data += struct.pack("!d", num)[-bytes_per_gate:]
    return data
