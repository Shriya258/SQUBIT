from hypothesis import given, strategies as st
from qiskit.quantum_info import Operator
import numpy as np

# 1. Import your original static unitarity edge case
from unitarity_violation_edgecase_example import buggy_unitarity_operator


def check_qiskit_unitarity(operator: Operator):
  """Physics validator: Catches non-unitary operators cleanly without tracebacks."""
  matrix = operator.data
  product = np.dot(matrix.conjugate().T, matrix)
  identity = np.eye(matrix.shape[0])

  if not np.allclose(product, identity, atol=1e-7):
    # Successfully flags the unitarity violation
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes non-unitary operator scaling
@given(val=st.floats(min_value=1.1, max_value=10.0, exclude_min=True))
def test_pbt_hidden_unitarity_bugs(val):
  """PBT that generates a spectrum of hidden non-unitary operators,

  ensuring the validator intercepts every single one cleanly.
  """
  # Create a hidden non-unitary operator dynamically based on the edgecase pattern
  hidden_buggy_op = Operator([[val, 0.0], [0.0, 1.0]])

  # Run the validator
  is_valid = check_qiskit_unitarity(hidden_buggy_op)

  # Invariant: Non-unitary operators must always be caught (return False)
  assert (
      is_valid is False
  ), f"PBT Missed Bug: Operator with scaling factor {val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON UNITARITY EDGECASE & HIDDEN BUGS")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static unitarity edgecase from file...")
  static_result = check_qiskit_unitarity(buggy_unitarity_operator)
  assert static_result is False, "Static unitarity edgecase failed to be caught!"
  print("-> [SUCCESS] Static unitarity edgecase from file caught cleanly!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated"
      " non-unitary operators..."
  )
  try:
    test_pbt_hidden_unitarity_bugs()
    print(
        "[SUCCESS] PBT execution complete! All non-unitary operator violations"
        " were successfully intercepted and flagged with zero tracebacks."
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
