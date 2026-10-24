from qiskit.quantum_info import Operator

# No-Cloning Violation concept: A non-linear or multi-input copying operation
# that attempts to map a single arbitrary state to two identical output states.
# In matrix form, a universal cloner is non-linear and cannot be represented as a valid linear Operator.
buggy_nocloning_operator = Operator(
    [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 2.0]] # Flawed scaling/cloning map
)
