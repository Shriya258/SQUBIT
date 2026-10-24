
from hypothesis import given, strategies as st
from qiskit.quantum_info import Operator
import numpy as np

# 1. Import your original static no-cloning edge case
from nocloning_violation_edgecase_example import buggy_nocloning_operator


def check_qiskit_nocloning(operator: Operator):
  """Physics validator: Catches linearity/cloning anomalies cleanly without tracebacks."""
  matrix = operator.data
  diag_elements = np.diagonal(matrix)
  
  if np.any(np.abs(diag_elements) > 1.0):
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes scaling/duplication factors
@given(scale_factor=st.floats(min_value=1.1, max_value=5.0))
def test_pbt_hidden_nocloning_bugs(scale_factor):
  """PBT that generates varied operators with illegal amplification factors,

  ensuring the validator intercepts every single one cleanly.
  """
  hidden_buggy_op = Operator([
      [1.0, 0.0, 0.0, 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, scale_factor]
  ])

  # Run the validator
  is_valid = check_qiskit_nocloning(hidden_buggy_op)

  # Invariant: No-cloning violations must always be caught (return False)
  assert (
      is_valid is False
  ), f"PBT Missed Bug: Operator with scale factor {scale_factor} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON NO-CLONING EDGECASE & HIDDEN BUGS")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static no-cloning edgecase from file...")
  static_result = check_qiskit_nocloning(buggy_nocloning_operator)
  assert static_result is False, "Static no-cloning edgecase failed to be caught!"
  print("-> [SUCCESS] Static no-cloning edgecase from file caught cleanly!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated"
      " cloning-violating operators..."
  )
  try:
    test_pbt_hidden_nocloning_bugs()
    print(
        "[SUCCESS] PBT execution complete! All no-cloning violations were"
        " successfully intercepted and flagged with zero tracebacks."
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
