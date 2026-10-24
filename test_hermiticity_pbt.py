from hypothesis import given, strategies as st
import numpy as np

# 1. Import your original static hermiticity edge case
from hermiticity_violation_edgecase_example import buggy_non_hermitian_matrix


def check_hermiticity(matrix: np.ndarray):
  """Physics validator: Catches non-Hermitian operators cleanly without tracebacks."""
  dagger = matrix.conjugate().T
  if not np.allclose(matrix, dagger, atol=1e-5):
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes off-diagonal imaginary asymmetry
@given(imag_val=st.floats(min_value=0.1, max_value=2.0))
def test_pbt_hidden_hermiticity_bugs(imag_val):
  """PBT that generates asymmetric non-Hermitian matrices,

  ensuring the validator intercepts every single violation cleanly.
  """
  fuzz_matrix = np.array([
      [1.0, 2.0 + imag_val * 1.0j],
      [2.0, 3.0]  # Asymmetric imaginary term breaks Hermiticity
  ])
  
  is_valid = check_hermiticity(fuzz_matrix)
  assert (
      is_valid is False
  ), f"PBT Missed Bug: Non-Hermitian matrix with imag offset {imag_val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON HERMITICITY OF OBSERVABLES")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static hermiticity edgecase from file...")
  static_result = check_hermiticity(buggy_non_hermitian_matrix)
  assert static_result is False, "Static hermiticity edgecase failed to be caught!"
  print("-> [SUCCESS] Static hermiticity edgecase caught successfully!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated matrices..."
  )
  try:
    test_pbt_hidden_hermiticity_bugs()
    print("Executed successfully, no bugs found.")
  except AssertionError as e:
    print(f"[FAILED] {e}")
