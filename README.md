# qiskit-leaky-scheduling

[![Build & Test Python Wheel Package](https://github.com/cryptohslu/qiskit-leaky-scheduling/actions/workflows/build.yml/badge.svg)](https://github.com/cryptohslu/qiskit-leaky-scheduling/actions/workflows/build.yml)

A transpilation scheduling plugin that can be used with Qiskit to leak information from the computer running the
transpilation step to the cloud receiving the quantum computing jobs.

Current implementation, by default, tries to encode [the HSLU logo](https://www.hslu.ch/en/) into the transpiled circuit.
Custom data will be used if available in `builtins.data` (see [the example](#Example) below). If data is too large to
encode into the given circuit, the unmodified circuit is returned. The encoding is done by modifying the last 6 bytes of
the float numbers (double precision) representing the rotation angles of the
[`RZGate`](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.RZGate)s. These bytes only affect the fraction
part of the number leading to slightly different rotation gates. However, since current hardware is still quite noisy,
the output of the original and modified circuit is indistinguishable in practice.

This attack is harder to detect than [qiskit-leaky-layout](https://github.com/cryptohslu/qiskit-leaky-layout) and
[qiskit-leaky-init](https://github.com/cryptohslu/qiskit-leaky-init) since nothing is changed from an optimal
transpilation for the targeted backend apart from the slightly modified angles (i.e., no additional registers,
same layout, etc.).

The plugin [is implemented](src/qiskit_leaky_scheduling/leaky_scheduling_plugin.py#L43) as a subclass of
[`PassManagerStagePlugin`](https://docs.quantum.ibm.com/api/qiskit/qiskit.transpiler.preset_passmanagers.plugin.PassManagerStagePlugin),
which appends to the default scheduling pass `DefaultSchedulingPassManager` a new
[`TransformationPass`](https://docs.quantum.ibm.com/api/qiskit/qiskit.transpiler.TransformationPass), called
[`LeakyRotations`](src/qiskit_leaky_scheduling/leaky_scheduling_plugin.py#L11).

Leaked data can be recovered with `recover_data()` implemented in the [decoder module](src/qiskit_leaky_scheduling/decoder.py).
See [the example](#Example) below.

## Instalation

```shell
git clone git@github.com:cryptohslu/qiskit-leaky-scheduling.git
cd qiskit-leaky-scheduling
pip install .
```

## Example

```python
import builtins
import io

from PIL import Image
from qiskit.circuit.random import random_circuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
from qiskit_ibm_runtime.fake_provider import FakeKyoto

from qiskit_leaky_scheduling import recover_data

print(list_stage_plugins("scheduling"))

backend = FakeKyoto()
pm = generate_preset_pass_manager(
    backend=backend,
    optimization_level=3,
    scheduling_method="leaky_rotations",
    seed_transpiler=0,
)

qc = random_circuit(
    num_qubits=7, depth=3, max_operands=2, measure=True, reset=False, seed=0
)

# Uncomment to leak this custom data instead of HSLU logo
# builtins.data = b"My secret data encoded in RZ gates."
isa_qc = pm.run(qc)

recovered_img = recover_data(isa_qc)[:328]
# recovered_data = recover_data(isa_qc)[:35]

Image.open(io.BytesIO(recovered_img)).show()
# print(recovered_data)
```
