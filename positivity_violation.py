from qiskit.quantum_info import DensityMatrix
import numpy as np

# Import the static positivity edgecase from your file
from positivity_violation_edgecase_example import buggy_density_matrix


def check_qiskit_positivity(density_matrix: DensityMatrix):
  """Uses Qiskit's DensityMatrix data to check if all eigenvalues are non-negative (positivity)."""
  matrix = density_matrix.data
  
  # Compute eigenvalues of the Hermitian density matrix
  eigenvalues = np.linalg.eigvalsh(matrix)

  # Positivity requirement: All eigenvalues must be >= 0 (within numerical tolerance)
  if np.any(eigenvalues < -1e-7):
    print(
        f"[FLAGGED] Positivity Violation: Density matrix contains negative "
        f"eigenvalues ({eigenvalues}), representing an unphysical quantum state!"
    )
    return False

  print("[PASSED] Density matrix is positive semi-definite and valid.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Qiskit Positivity Check on Edgecase...")
check_qiskit_positivity(buggy_density_matrix)
