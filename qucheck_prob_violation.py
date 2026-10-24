from hypothesis import given, strategies as st
from qiskit.quantum_info import Statevector
import numpy as np

# 1. Import your original edge case to verify it's caught
from prob_violation_edgecase_example import buggy_probability_state


def check_qiskit_probability(state_vector: Statevector):
  """Physics validator: Catches unnormalized states cleanly without tracebacks."""
  amplitudes = state_vector.data
  total_prob = np.sum(np.abs(amplitudes) ** 2)

  if not np.isclose(total_prob, 1.0, atol=1e-7):
    # Successfully flags the hidden bug instead of crashing
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes your edgecase pattern
@given(amplitude_val=st.floats(min_value=1.1, max_value=10.0, exclude_min=True))
def test_pbt_hidden_probability_bugs(amplitude_val):
  """PBT that generates a spectrum of hidden buggy quantum states

  violating physics laws (similar to your edgecase), ensuring the
  validator catches every single one cleanly.
  """
  # Create a hidden bug dynamically using variations of your edgecase structure
  hidden_buggy_state = Statevector([amplitude_val, 0.0])

  # Run the validator
  is_valid = check_qiskit_probability(hidden_buggy_state)

  # Invariant: Physics-violating code must always be caught (return False)
  assert (
      is_valid is False
  ), f- "PBT Missed Bug: State with amplitude {amplitude_val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON EDGECASE & GENERATED HIDDEN BUGS")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static edgecase from file...")
  static_result = check_qiskit_probability(buggy_probability_state)
  assert (
      static_result is False
  ), "Static edgecase failed to be caught!"
  print("-> [SUCCESS] Static edgecase from file caught cleanly!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated edge"
      " cases..."
  )
  try:
    test_pbt_hidden_probability_bugs()
    print(
        "[SUCCESS] PBT execution complete! All hidden probability-violating"
        " edge cases were successfully intercepted and flagged with zero"
        " tracebacks."
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
