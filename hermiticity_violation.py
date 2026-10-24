import numpy as np

# Import the static hermiticity edgecase from your file
from hermiticity_violation_edgecase_example import buggy_non_hermitian_matrix


def check_hermiticity(matrix: np.ndarray):
  """Checks if an operator/Hamiltonian is Hermitian (H == H^dagger)."""
  # Compute conjugate transpose (dagger)
  dagger = matrix.conjugate().T

  # Check if the matrix is equal to its conjugate transpose within tolerance
  if not np.allclose(matrix, dagger, atol=1e-5):
    print(
        "[FLAGGED] Hermiticity Violation: Operator is not Hermitian "
        f"(differs from its conjugate transpose)!"
    )
    return False

  print("[PASSED] Operator is Hermitian.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Hermiticity Check on Edgecase...")
check_hermiticity(buggy_non_hermitian_matrix)
