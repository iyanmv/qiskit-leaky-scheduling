import unittest
import secrets
from pathlib import Path


class TestEntryPoint(unittest.TestCase):
    def test_plugin_available(self):
        from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins

        scheduling_plugins = list_stage_plugins("scheduling")
        self.assertTrue("leaky_rotations" in scheduling_plugins)


class TestExample(unittest.TestCase):
    def test_example_readme_image(self):
        from qiskit.circuit.random import random_circuit
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
        from qiskit_ibm_runtime.fake_provider import FakeKyoto
        from qiskit_leaky_scheduling import recover_data

        with open(Path(__file__).parent / "../HSLU_Logo_small.png", "rb") as file:
            hslu_logo = file.read()

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

        isa_qc = pm.run(qc)

        recovered_img = recover_data(isa_qc)[:328]
        self.assertEqual(hslu_logo, recovered_img)

    def test_example_readme_message(self):
        import builtins
        from qiskit.circuit.random import random_circuit
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
        from qiskit_ibm_runtime.fake_provider import FakeKyoto
        from qiskit_leaky_scheduling import recover_data

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

        message = b"My secret data encoded in RZ gates."
        builtins.data = message

        isa_qc = pm.run(qc)

        recovered_data = recover_data(isa_qc)[:35]
        self.assertEqual(message, recovered_data)
        del builtins.data

    def test_random_encoding_decoding_hslu_logo(self):
        from qiskit.circuit.random import random_circuit
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
        from qiskit_ibm_runtime.fake_provider import FakeKyiv
        from qiskit_leaky_scheduling import recover_data

        with open(Path(__file__).parent / "../HSLU_Logo_small.png", "rb") as file:
            hslu_logo = file.read()

        backend = FakeKyiv()

        for i in range(5):
            seed = secrets.randbelow(10**8)
            with self.subTest(seed=seed):
                qc = random_circuit(
                    num_qubits=50,
                    depth=5,
                    max_operands=2,
                    measure=True,
                    reset=False,
                )
                pm = generate_preset_pass_manager(
                    backend=backend,
                    optimization_level=3,
                    scheduling_method="leaky_rotations",
                )
                isa_qc = pm.run(qc)
                recovered_hslu_logo = recover_data(isa_qc)[:328]
                self.assertEqual(hslu_logo, recovered_hslu_logo)

    def test_random_encoding_decoding_builtins(self):
        import builtins
        from qiskit.circuit.random import random_circuit
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
        from qiskit_ibm_runtime.fake_provider import FakeKyiv
        from qiskit_leaky_scheduling import recover_data

        message = b"My secret data encoded in RZ gates."
        builtins.data = message

        backend = FakeKyiv()

        for i in range(5):
            seed = secrets.randbelow(10**8)
            with self.subTest(seed=seed):
                qc = random_circuit(
                    num_qubits=50,
                    depth=5,
                    max_operands=2,
                    measure=True,
                    reset=False,
                )
                pm = generate_preset_pass_manager(
                    backend=backend,
                    optimization_level=3,
                    scheduling_method="leaky_rotations",
                )
                isa_qc = pm.run(qc)
                recovered_message = recover_data(isa_qc)[:35]
                self.assertEqual(message, recovered_message)

        del builtins.data
