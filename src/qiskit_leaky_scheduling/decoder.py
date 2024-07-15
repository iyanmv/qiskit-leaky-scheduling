import struct

from qiskit.circuit import QuantumCircuit
from qiskit.converters import circuit_to_dag


def recover_data(qc: QuantumCircuit, bytes_per_gate=6) -> bytes:
    data = b""
    dag = circuit_to_dag(qc)
    rotations = sorted([op for op in dag.op_nodes() if op.name == "rz"])
    for rz in rotations:
        num = rz.op.params[0]
        data += struct.pack("!d", num)[-bytes_per_gate:]
    return data
