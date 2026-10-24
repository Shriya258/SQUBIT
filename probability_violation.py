from qiskit.quantum_info import Statevector
import numpy as np

# Import the edgecase using your exact file name
from prob_violating_edgecase_example import buggy_probability_state


def check_qiskit_probability(state_vector: Statevector):
  """Uses Qiskit's Statevector class to check if probabilities sum to 1.0."""
  amplitudes = state_vector.data
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
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Qiskit Probability Check on Edgecase...")
check_qiskit_probability(buggy_probability_state)
