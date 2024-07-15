import struct

from qiskit.circuit import QuantumCircuit


def recover_data(qc: QuantumCircuit, bytes_per_gate=6) -> bytes:
    data = b""
    for op in qc.data:
        if op.operation.name != "rz":
            continue
        num = op.operation.params[0]
        data += struct.pack("!d", num)[-bytes_per_gate:]
    return data
