from qiskit.quantum_info import Statevector

# Probability violation: sum of squared amplitudes equals 4.0 instead of 1.0
buggy_probability_state = Statevector([2.0, 0.0])
