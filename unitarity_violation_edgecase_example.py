from qiskit.quantum_info import Operator

# Unitarity violation: A matrix that is not unitary (scaling matrix instead of a unitary gate)
buggy_unitarity_operator = Operator([[2.0, 0.0], [0.0, 1.0]])
