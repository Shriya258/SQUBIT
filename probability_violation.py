from qiskit.quantum_info import Statevector

# PHYSICS FAILURE: These probabilities sum to 4.0 (2^2 + 0^2), not 1.0!
bad_state = Statevector([2.0, 0.0])

print("Is valid state vector according to Qiskit class?", bad_state.is_valid())
# Note: Qiskit's Statevector class might auto-normalize or throw depending on how it's used,
# but custom manual initializations in test generators often bypass this check.
