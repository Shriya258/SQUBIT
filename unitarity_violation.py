from qiskit.quantum_info import Operator
import numpy as np

# Import the static unitarity edgecase from your file
from unitarity_violation_edgecase_example import buggy_unitarity_operator


def check_qiskit_unitarity(operator: Operator):
  """Uses Qiskit's Operator data to check if U dagger * U equals the Identity matrix."""
  matrix = operator.data
  # Calculate U-dagger * U
  product = np.dot(matrix.conjugate().T, matrix)
  identity = np.eye(matrix.shape[0])

  # Check if it satisfies unitarity (U dagger * U == I)
  if not np.allclose(product, identity, atol=1e-7):
    print(
        f"[FLAGGED] Unitarity Violation: Operator matrix is not unitary!"
        f" U†U product differs from Identity."
    )
    return False

  print("[PASSED] Operator is valid and unitary.")
  return True


# ==========================================
# EXECUTE ON THE IMPORTED EDGECASE FILE
# ==========================================
print("Running Qiskit Unitarity Check on Edgecase...")
check_qiskit_unitarity(buggy_unitarity_operator)
