from hypothesis import given, strategies as st
from qiskit.quantum_info import DensityMatrix
import numpy as np

# 1. Import your original static positivity edge case
from positivity_violation_edgecase_example import buggy_density_matrix


def check_qiskit_positivity(density_matrix: DensityMatrix):
  """Physics validator: Catches negative eigenvalues/unphysical states cleanly without tracebacks."""
  matrix = density_matrix.data
  eigenvalues = np.linalg.eigvalsh(matrix)
  
  if np.any(eigenvalues < -1e-7):
    return False
  return True


# 2. Property-Based Test: Dynamically fuzzes negative eigenvalue variations
@given(neg_val=st.floats(min_value=-5.0, max_value=-0.1))
def test_pbt_hidden_positivity_bugs(neg_val):
  """PBT that generates varied density matrices with unphysical negative eigenvalues,

  ensuring the validator intercepts every single one cleanly.
  """
  hidden_buggy_dm = DensityMatrix([[1.0 - neg_val, 0.0], [0.0, neg_val]])

  # Run the validator
  is_valid = check_qiskit_positivity(hidden_buggy_dm)

  # Invariant: Positivity violations must always be caught (return False)
  assert (
      is_valid is False
  ), f"PBT Missed Bug: Density matrix with negative eigenvalue {neg_val} passed validation!"


if __name__ == "__main__":
  print("==================================================")
  print("RUNNING PBT ON POSITIVITY EDGECASE & HIDDEN BUGS")
  print("==================================================")

  # First, verify it catches your specific static edgecase file
  print("[Test 1] Checking static positivity edgecase from file...")
  static_result = check_qiskit_positivity(buggy_density_matrix)
  assert static_result is False, "Static positivity edgecase failed to be caught!"
  print("-> [SUCCESS] Static positivity edgecase from file caught cleanly!")

  # Second, run the full property-based test suite
  print(
      "\n[Test 2] Running Hypothesis PBT across multiple generated"
      " positivity-violating density matrices..."
  )
  try:
    test_pbt_hidden_positivity_bugs()
    print(
        "[SUCCESS] PBT execution complete! All positivity violations were"
        " successfully intercepted and flagged with zero tracebacks."
    )
  except AssertionError as e:
    print(f"[FAILED] {e}")
