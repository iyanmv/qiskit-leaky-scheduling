# qiskit-leaky-scheduling

A transpilation scheduling plugin that can be used with Qiskit to leak private information from the computer running the
transpilation step to the cloud receiving the jobs for the quantum computers.

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
#TODO
```
