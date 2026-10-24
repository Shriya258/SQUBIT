from qiskit.quantum_info import Statevector
import numpy as np


def check_qiskit_probability(state_vector: Statevector):
  """Uses Qiskit's Statevector class to check if probabilities sum to 1.0."""
  # Extract raw complex amplitudes from Qiskit's Statevector object
  amplitudes = state_vector.data

  # Calculate total probability
  total_prob = np.sum(np.abs(amplitudes) ** 2)

  # Check if it violates probability rules
  if not np.isclose(total_prob, 1.0, atol=1e-7):
    print(
        f"[FLAGGED] Probability Violation: Qiskit Statevector probabilities"
        f" sum to {total_prob}, violating conservation of probability!"
    )
    return False

  print("[PASSED] Qiskit Statevector is properly normalized.")
  return True


# ==========================================
# TESTING WITH A BUGGY QISKIT STATEVECTOR
# ==========================================
# Creating an unnormalized state vector where probabilities sum to 4.0
buggy_state = Statevector([2.0, 0.0])

print("Running Qiskit Probability Check...")
check_qiskit_probability(buggy_state)
